import multiprocessing as mp
from multiprocessing.shared_memory import SharedMemory

import numpy as np

from ppga import log


def compute(shape, dtype, index, offset, toolbox, cxpb, mutbp):
    logger = log.getCoreLogger()
    logger.debug("start")
    mem = SharedMemory(name="couples", create=False)
    chunk = np.ndarray(shape=shape, dtype=dtype, buffer=mem.buf)

    del chunk
    mem.close()
    logger.debug("terminated")


class Worker(mp.Process):
    def __init__(self) -> None:
        super().__init__(target=compute)

    def join(self, timeout: float | None = None) -> None:
        super().join(timeout)
