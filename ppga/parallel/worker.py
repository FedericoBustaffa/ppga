import multiprocessing as mp
import multiprocessing.queues as mpq
import random

import numpy.random as nprnd

from ppga import log


def compute(send_q: mpq.Queue, recv_q: mpq.Queue):
    logger = log.getCoreLogger()
    logger.debug(f"start with PID: {mp.current_process().ident}")

    random.seed(mp.current_process().ident)
    nprnd.seed(mp.current_process().ident)

    while True:
        task = send_q.get()
        if task is None:
            logger.debug("received termination chunk")
            break

        func, chunk, args, kwargs = task

        res = []
        for i in chunk:
            res.append(func(i, *args, **kwargs))

        recv_q.put(res)

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
        return self.recv_q.get()

    def join(self, timeout: float | None = None) -> None:
        self.send_q.put(None)
        super().join(timeout)
