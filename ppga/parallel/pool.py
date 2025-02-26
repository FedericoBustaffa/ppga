import multiprocessing as mp

import psutil

from ppga import base, log, parallel

logger = log.getCoreLogger()


class Pool:
    def __init__(
        self,
        population: base.Population,
        toolbox: base.ToolBox,
        cxpb: float,
        mutpb: float,
        workers_num: int = -1,
    ) -> None:
        # parallelism init
        cores = psutil.cpu_count(False)
        assert cores is not None
        self.cores = cores if workers_num <= 0 or workers_num > cores else workers_num

        self.barrier = mp.Barrier(self.cores + 1)
        self.stop = mp.Event()
        self.workers = [
            parallel.Worker(
                i,
                population,
                toolbox,
                cxpb,
                mutpb,
                self.barrier,
                self.stop,
            )
            for i in range(self.cores)
        ]
        for w in self.workers:
            w.start()

        logger.debug(f"pool started with {self.cores} workers")

    def cx_mut_eval(self, population):
        self.barrier.wait()
        self.barrier.wait()

        parallel.copy_from_shm(population)

    def join(self, timeout: float | None = None) -> None:
        self.stop.set()
        self.barrier.wait()
        for w in self.workers:
            w.join(timeout)

        logger.debug("pool joined")
