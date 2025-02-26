import multiprocessing as mp
from typing import Any

import numpy as np
import psutil

from ppga import log, parallel

logger = log.getCoreLogger()


class Pool:
    def __init__(self, workers_num: int = -1) -> None:
        cores = psutil.cpu_count(False)
        assert cores is not None
        self.cores = cores if workers_num <= 0 or workers_num > cores else workers_num

        self.barrier = mp.Barrier(self.cores)
        self.workers = [parallel.Worker(i, self.barrier) for i in range(self.cores)]
        for w in self.workers:
            w.start()

        logger.debug(f"pool started with {self.cores} workers")

    def cx_mut_eval(self, population) -> list[Any]:
        self.barrier.wait()
        self.barrier.wait()

        parallel.copy_from_shm(population)

        return population

    def join(self, timeout: float | None = None) -> None:
        for w in self.workers:
            w.join(timeout)

        logger.debug("pool joined")
