from typing import Any, Iterable, Mapping

import psutil
import ray
from ray.remote_function import RemoteFunction

from ppga import log


class Pool:
    def __init__(self, logical: bool = False) -> None:
        self.cores = psutil.cpu_count(logical)
        assert self.cores is not None
        ray.init()

        logger = log.getCoreLogger()
        logger.debug(f"pool started with {self.cores} workers")

    def map(
        self,
        func: RemoteFunction,
        iterable,
        args: Iterable[Any] = (),
        kwargs: Mapping[str, Any] = {},
    ) -> list[Any]:
        logger = log.getCoreLogger()

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

        func.options(num_cpus=workers_num)
        results_chunk = ray.get(
            [func.remote(chunk, *args, **kwargs) for chunk in chunks]
        )

        results = []
        for chunk in results_chunk:
            results.extend(chunk)

        return results

    def join(self, timeout: float | None = None) -> None:
        logger = log.getCoreLogger()
        logger.debug("pool joined")
