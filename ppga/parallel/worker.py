import multiprocessing as mp
import multiprocessing.queues as mpq

from ppga import log


def compute(
    send_q: mpq.JoinableQueue,
    recv_q: mpq.JoinableQueue,
    log_level: str | int = log.INFO,
):
    logger = log.getCoreLogger(log_level)
    while True:
        task = send_q.get()
        send_q.task_done()
        if task is None:
            logger.debug("received termination object")
            break

        func, chunk, args = task
        logger.debug(f"{chunk}")
        result = []
        for i, elem in enumerate(chunk):
            result.extend(func(elem, *args))

        recv_q.put(result)


class Worker(mp.Process):
    def __init__(self, log_level: str | int = log.WARNING) -> None:
        self.send_q = mp.JoinableQueue()
        self.recv_q = mp.JoinableQueue()

        super().__init__(
            target=compute,
            args=[self.send_q, self.recv_q, log_level],
        )

    def send(self, chunk) -> None:
        self.send_q.put(chunk)

    def recv(self):
        result = self.recv_q.get()
        self.recv_q.task_done()

        return result

    def join(self, timeout: float | None = None) -> None:
        self.send_q.put(None)
        super().join(timeout)
