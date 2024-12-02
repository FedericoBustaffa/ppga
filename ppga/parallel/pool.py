from multiprocessing import shared_memory
from typing import Any, Callable, Iterable, Mapping

import numpy as np
import psutil

from ppga import log
from ppga.parallel.worker import Worker


class Pool:
    def __init__(self, logical: bool = False) -> None:
        self.cores = psutil.cpu_count(logical)
        assert self.cores is not None

        self.workers = [Worker() for _ in range(self.cores)]
        for w in self.workers:
            w.start()

        logger = log.getCoreLogger()
        logger.debug(f"pool started with {self.cores} workers")

    def map(
        self,
        func: Callable,
        iterable: np.ndarray,
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

        # create the shared memory
        input_mem = shared_memory.SharedMemory("input", True, iterable.nbytes)
        input_copy = np.ndarray(iterable.shape, iterable.dtype, input_mem.buf)
        input_copy[:] = iterable[:]

        # mapping chunks to the workers
        for i in range(carry):
            self.workers[i].send(
                (
                    func,
                    i * chunksize,
                    i * chunksize + chunksize + 1,
                    iterable.shape,
                    iterable.dtype,
                    args,
                    kwargs,
                )
            )

        for i in range(carry, workers_num, 1):
            self.workers[i].send(
                (
                    func,
                    i * chunksize,
                    i * chunksize + chunksize,
                    iterable.shape,
                    iterable.dtype,
                    args,
                    kwargs,
                )
            )

        # get back the results
        result = []
        for i in range(workers_num):
            result.extend(self.workers[i].recv())

        input_mem.close()
        input_mem.unlink()

        return result

    def join(self, timeout: float | None = None) -> None:
        for w in self.workers:
            w.join(timeout)

        logger = log.getCoreLogger()
        logger.debug("pool joined")
