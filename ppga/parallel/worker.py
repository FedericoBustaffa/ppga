import multiprocessing as mp
import multiprocessing.synchronize as sync
import random
from multiprocessing import shared_memory as shm

import numpy as np
import numpy.random as nprandom

from ppga import algorithms, base, log


class Worker(mp.Process):
    def __init__(
        self,
        id: int,
        population: base.Population,
        toolbox: base.ToolBox,
        cxpb: float,
        mutpb: float,
        barrier: sync.Barrier,
        stop: sync.Event,
    ) -> None:
        super().__init__()
        self.id = id

        # population info
        self.chromo_shape, self.chromo_type = (
            population.chromosomes.shape,
            population.chromosomes.dtype,
        )
        self.scores_shape, self.scores_type = (
            population.scores.shape,
            population.scores.dtype,
        )

        # GA utils
        self.toolbox = toolbox
        self.cxpb = cxpb
        self.mutpb = mutpb

        self.barrier = barrier
        self.stop = stop

    def run(self) -> None:
        logger = log.getCoreLogger()
        logger.debug(f"start with PID: {mp.current_process().ident}")

        random.seed(self.id)
        nprandom.seed(self.id)

        pop_mem = shm.SharedMemory(name="chromosomes", create=False)
        chromosomes = np.ndarray(
            shape=self.chromo_shape,
            dtype=self.chromo_type,
            buffer=pop_mem.buf,
        )
        scores_mem = shm.SharedMemory(name="scores", create=False)
        scores = np.ndarray(
            shape=self.scores_shape,
            dtype=self.scores_type,
            buffer=scores_mem.buf,
        )

        chunksize = len(scores) // (self.barrier.parties - 1)

        while True:
            self.barrier.wait()
            if self.stop.is_set():
                break

            for i in range(chunksize):
                algorithms.batch.crossover(
                    chromosomes[i * chunksize : i * chunksize + chunksize],
                    self.toolbox,
                    self.cxpb,
                )
                algorithms.batch.mutation(
                    chromosomes[i * chunksize : i * chunksize + chunksize],
                    self.toolbox,
                    self.mutpb,
                )
                algorithms.batch.evaluation(
                    chromosomes[i * chunksize : i * chunksize + chunksize],
                    scores[i * chunksize : i * chunksize + chunksize],
                    self.toolbox,
                )

            self.barrier.wait()

        pop_mem.close()
        scores_mem.close()
        logger.debug("terminated")

    def join(self, timeout: float | None = None) -> None:
        super().join(timeout)
