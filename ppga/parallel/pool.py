from typing import Any, Callable, Iterable, Mapping

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
        iterable,
        args: Iterable[Any] = (),
        kwargs: Mapping[str, Any] = {},
    ) -> list[Any]:
        return []

    def join(self, timeout: float | None = None) -> None:
        for w in self.workers:
            w.join(timeout)

        logger = log.getCoreLogger()
        logger.debug("pool joined")
