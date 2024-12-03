from multiprocessing.shared_memory import SharedMemory

import numpy as np
import psutil

from ppga.parallel.worker import Worker


class Pool:
    def __init__(self, logical: bool = False):
        self.cores = psutil.cpu_count(logical)
        assert self.cores is not None

        self.workers = [Worker() for _ in range(self.cores)]
        for w in self.workers:
            w.start()

    def init(self, couples: np.ndarray) -> SharedMemory:
        couples_mem = SharedMemory("couples", create=True, size=couples.nbytes)
        for w in self.workers:
            w.send(couples)

        return couples_mem

    def run(self):
        pass

    def join(self, timeout: float | None = None) -> None:
        for w in self.workers:
            w.join(timeout)
