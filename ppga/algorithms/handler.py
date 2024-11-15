import queue
import threading

from ppga import log
from ppga.algorithms.worker import Worker
from ppga.base.toolbox import ToolBox


def handle(
    send_q: queue.Queue,
    recv_q: queue.Queue,
    toolbox: ToolBox,
    cxpb: float,
    mutpb: float,
    log_level: str | int = log.WARNING,
):
    worker = Worker(toolbox, cxpb, mutpb, log_level)
    worker.start()

    while True:
        chunk = send_q.get()
        worker.send(chunk)

        if chunk is None:
            break

        offsprings, evals = worker.recv()

    worker.join()


class Handler(threading.Thread):
    def __init__(
        self,
        toolbox: ToolBox,
        cxpb: float,
        mutpb: float,
        log_level: str | int = log.WARNING,
    ) -> None:
        self.send_q = queue.Queue()
        self.recv_q = queue.Queue()
        super().__init__(
            target=handle,
            args=[self.send_q, self.recv_q, toolbox, cxpb, mutpb, log_level],
        )

    def send(self, chunk) -> None:
        self.send_q.put(chunk)

    def recv(self):
        result = self.recv_q.get()
        self.recv_q.task_done()

        return result

    def join(self, timeout: float | None = None) -> None:
        super().join(timeout)


if __name__ == "__main__":
    # testing

    for i in range(1000):
        print(i)
        handler = Handler(ToolBox(), 0.8, 0.2)
        handler.start()
        handler.send([i for i in range(100)])
        something = handler.recv()
        handler.join()
