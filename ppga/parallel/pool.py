import psutil

from ppga import log
from ppga.parallel.worker import Worker


class Pool:
    def __init__(
        self, logical: bool = False, log_level: str | int = log.WARNING
    ) -> None:
        self.cores = psutil.cpu_count(logical)
        assert self.cores is not None

        self.logger = log.getCoreLogger(log_level)

        self.workers = [Worker(log_level) for _ in range(self.cores)]
        for w in self.workers:
            w.start()

    def map(self, func, iterable, *args):
        # dinamically resize the chunksize
        assert self.cores is not None
        workers_num = self.cores
        if len(iterable) < self.cores:
            workers_num = len(iterable)

        chunksize = len(iterable) // workers_num
        carry = len(iterable) % workers_num

        # mapping chunks to the workers
        for i in range(carry):
            self.workers[i].send(
                (
                    func,
                    iterable[i * chunksize : i * chunksize + chunksize + 1],
                    args,
                )
            )

        for i in range(carry, workers_num, 1):
            self.workers[i].send(
                (
                    func,
                    iterable[i * chunksize : i * chunksize + chunksize],
                    args,
                )
            )

        # get back the results
        result = []
        for w in self.workers:
            result.extend(w.recv())

        return result

    def join(self, timeout: float | None = None) -> None:
        for w in self.workers:
            w.join(timeout)
