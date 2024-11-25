import queue
import threading

from ppga import log


def compute(
    send_q: queue.Queue,
    recv_q: queue.Queue,
):
    logger = log.getCoreLogger()
    logger.debug("start")

    while True:
        task = send_q.get()
        send_q.task_done()
        if task is None:
            logger.debug("received termination chunk")
            break

        func, chunk, args, kwargs = task
        recv_q.put(func(chunk, *args, **kwargs))

    logger.debug("terminated")


class Worker(threading.Thread):
    def __init__(self) -> None:
        self.send_q = queue.Queue()
        self.recv_q = queue.Queue()

        super().__init__(
            target=compute,
            args=[self.send_q, self.recv_q],
        )

    def send(self, chunk) -> None:
        self.send_q.put(chunk)

    def recv(self):
        result = self.recv_q.get()
        self.recv_q.task_done()

        return result

    def join(self, timeout: float | None = None) -> None:
        self.send_q.put(None)
        self.send_q.join()
        self.recv_q.join()
        super().join(timeout)
