import queue
<<<<<<< HEAD
import threading
=======
import random
import threading

import numpy.random as nprandom
>>>>>>> refs/remotes/origin/thread

from ppga import log


<<<<<<< HEAD
def compute(
    send_q: queue.Queue,
    recv_q: queue.Queue,
):
    logger = log.getCoreLogger()
    logger.debug("start")
=======
class Worker(threading.Thread):
    def __init__(self, id: int) -> None:
        super().__init__()
        self.id = id
        self.send_q = queue.Queue()
        self.recv_q = queue.Queue()
>>>>>>> refs/remotes/origin/thread

    def run(self) -> None:
        logger = log.getCoreLogger()
        logger.debug(f"start with PID: {threading.current_thread().native_id}")

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

<<<<<<< HEAD
class Worker(threading.Thread):
    def __init__(self) -> None:
        self.send_q = queue.Queue()
        self.recv_q = queue.Queue()
=======
            self.recv_q.put(res)
>>>>>>> refs/remotes/origin/thread

        logger.debug("terminated")

    def send(self, chunk) -> None:
        self.send_q.put(chunk)

    def recv(self):
        return self.recv_q.get()

    def join(self, timeout: float | None = None) -> None:
        self.send_q.put(None)
        super().join(timeout)
