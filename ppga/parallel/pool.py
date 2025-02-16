import pickle
from typing import Any, Callable

import psutil

from ppga import log
from ppga.parallel.worker import Worker

logger = log.getCoreLogger()


class Pool:
    def __init__(self, workers_num: int = -1, logical: bool = False) -> None:
        # faster serialization/deserialization
        pickle.DEFAULT_PROTOCOL = pickle.HIGHEST_PROTOCOL

        cores = psutil.cpu_count(logical)
        assert cores is not None
        self.cores = cores if workers_num <= 0 or workers_num > cores else workers_num

        self.workers = [Worker(i) for i in range(self.cores)]
        for w in self.workers:
            w.start()

        # process monitor and timers
        self.monitors = {w.pid: psutil.Process(w.pid) for w in self.workers}
        self.timers = {w.pid: 0.0 for w in self.workers}

        logger.debug(f"pool started with {self.cores} workers")

    def map(self, func: Callable, iterable, *args, **kwargs) -> list[Any]:
        # dinamically resize the chunksize
        assert self.cores is not None
        workers_num = self.cores

        if len(iterable) < self.cores:
            workers_num = len(iterable)
            logger.warning(
                f"workers used: {workers_num} out of {self.cores} cores available"
            )

        chunksize = len(iterable) // workers_num
        carry = len(iterable) % workers_num

        # mapping chunks to the workers
        chunks = [
            iterable[i * chunksize : i * chunksize + chunksize + 1]
            for i in range(carry)
        ]

        chunks += [
            iterable[i * chunksize : i * chunksize + chunksize]
            for i in range(carry, workers_num, 1)
        ]

        for i, (w, c) in enumerate(zip(self.workers, chunks)):
            self.timers[w.pid] = (
                self.monitors[w.pid].cpu_times().user
                + self.monitors[w.pid].cpu_times().system
            )
            w.send([func, c, args, kwargs])

        # get back the results
        result = []
        for w in self.workers:
            result.extend(w.recv())
            self.timers[w.pid] = (
                self.monitors[w.pid].cpu_times().user
                + self.monitors[w.pid].cpu_times().system
            ) - self.timers[w.pid]

        return result

    def worker_time(self) -> float:
        return max([t for t in self.timers.values()])

    def join(self, timeout: float | None = None) -> None:
        for w in self.workers:
            w.join(timeout)

        logger.debug("pool joined")
