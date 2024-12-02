import multiprocessing as mp
import multiprocessing.queues as mpq
from multiprocessing.shared_memory import SharedMemory

import numpy as np

from ppga import log


def compute(
    send_q: mpq.Queue,
    recv_q: mpq.Queue,
):
    logger = log.getCoreLogger()
    logger.debug("start")
    mem = SharedMemory(name="couples", create=False)

    while True:
        task = send_q.get()
        if task is None:
            logger.debug("received termination chunk")
            break

        func, index, offset, shape, dtype, args, kwargs = task
        chunk = np.ndarray(shape=shape, dtype=dtype, buffer=mem.buf)
        recv_q.put(func(chunk[index:offset], *args, **kwargs))
        
    mem.close()
    logger.debug("terminated")


class Worker(mp.Process):
    def __init__(self) -> None:
        self.send_q = mp.Queue()
        self.recv_q = mp.Queue()

        super().__init__(
            target=compute,
            args=[self.send_q, self.recv_q],
        )

    def send(self, chunk) -> None:
        self.send_q.put(chunk)

    def recv(self):
        result = self.recv_q.get()
        return result

    def join(self, timeout: float | None = None) -> None:
        self.send_q.put(None)
        super().join(timeout)
