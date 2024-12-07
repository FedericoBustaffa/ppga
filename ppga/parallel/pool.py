from typing import Any, Callable, Iterable, Mapping

import psutil
from joblib import Parallel, delayed

from ppga import log


class Pool:
    def __init__(self, workers_num: int = 0, logical: bool = False) -> None:
        self.cores = psutil.cpu_count(logical) if workers_num == 0 else workers_num
        assert self.cores is not None

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

        results_chunk = Parallel(n_jobs=workers_num)(
            delayed(func)(chunk, *args, **kwargs) for chunk in chunks
        )

        results = []
        for chunk in results_chunk:
            results.extend(chunk)

        return results

    def join(self, timeout: float | None = None) -> None:
        logger = log.getCoreLogger()
        logger.debug("pool joined")
