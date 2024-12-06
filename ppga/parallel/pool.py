from typing import Any, Callable, Iterable, Mapping

import psutil

from ppga import log
from ppga.parallel.worker import Worker


class Pool:
    def __init__(self, workers_num: int = 0, logical: bool = False) -> None:
        self.cores = psutil.cpu_count(logical) if workers_num == 0 else workers_num
        assert self.cores is not None

        self.workers = [Worker() for _ in range(self.cores)]
        for w in self.workers:
            w.start()

        logger = log.getCoreLogger()
        logger.debug(f"pool started with {self.cores} workers")

    def map(
        self,
        func: Callable,
        iterable,
        args: Iterable[Any] = (),
        kwargs: Mapping[str, Any] = {},
    ) -> list[Any]:
        logger = log.getCoreLogger()

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

        for w, c in zip(self.workers, chunks):
            w.send((func, c, args, kwargs))

        # get back the results
        result = []
        for i in range(workers_num):
            result.extend(self.workers[i].recv())

        return result

    def join(self, timeout: float | None = None) -> None:
        for w in self.workers:
            w.join(timeout)

        logger = log.getCoreLogger()
        logger.debug("pool joined")
