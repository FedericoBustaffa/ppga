import multiprocessing as mp
import random

import numpy.random as nprandom

from ppga import log


class Worker(mp.Process):
    def __init__(self, id: int) -> None:
        super().__init__()
        self.id = id
        self.send_q = mp.Queue()
        self.recv_q = mp.Queue()

    def run(self) -> None:
        logger = log.getCoreLogger()
        logger.debug(f"start with PID: {mp.current_process().ident}")

        random.seed(self.id)
        nprandom.seed(self.id)

        while True:
            task = self.send_q.get()
            if task is None:
                logger.debug("received termination chunk")
                break

            func, chunk, args, kwargs = task

            res = []
            for i in chunk:
                res.append(func(i, *args, **kwargs))

            self.recv_q.put(res)

        logger.debug("terminated")

    def send(self, chunk) -> None:
        self.send_q.put(chunk)

    def recv(self):
        return self.recv_q.get()

    def join(self, timeout: float | None = None) -> None:
        self.send_q.put(None)
        super().join(timeout)
