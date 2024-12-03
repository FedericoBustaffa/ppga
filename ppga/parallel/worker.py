import multiprocessing as mp
import multiprocessing.queues as mpq
from multiprocessing.shared_memory import SharedMemory

import numpy as np

from ppga import log
from ppga.algorithms import batch


def compute(send_q: mpq.Queue):
    logger = log.getCoreLogger()
    logger.debug("start")

    # allocate couples memory
    couples = np.asarray(send_q.get())
    couples_mem = SharedMemory(name="couples", create=False)
    chunk = np.ndarray(shape=couples.shape, dtype=couples.dtype, buffer=couples_mem.buf)
    logger.debug(chunk)

    # allocate offsprings memory
    offsprings = np.empty((couples.shape[0] * 2, 1))

    while True:
        offsprings = batch.crossover(couples, toolbox, cxpb)
        offsprings = batch.mutation(offsprings, toolbox, mutpb)

        scores = batch.evaluation(offsprings, toolbox)
        offsprings = [Individual(c, s[0], s[1]) for c, s in zip(offsprings, scores)]

    mem.close()
    logger.debug("terminated")


class Worker(mp.Process):
    def __init__(self) -> None:
        self.send_q = mp.Queue()
        super().__init__(target=compute, args=[self.send_q])

    def send(self, couples: np.ndarray) -> None:
        self.send_q.put(couples)

    def join(self, timeout: float | None = None) -> None:
        super().join(timeout)
