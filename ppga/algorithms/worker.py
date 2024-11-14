import multiprocessing as mp
import multiprocessing.queues as mpq

from ppga import log
from ppga.algorithms.reproduction import reproduction
from ppga.base.toolbox import ToolBox


def task(
    rqueue: mpq.Queue,
    squeue: mpq.Queue,
    toolbox: ToolBox,
    cxpb: float,
    mutpb: float,
    log_level: str | int = log.INFO,
):
    logger = log.getCoreLogger(log_level)
    while True:
        parents = squeue.get()
        if parents is None:
            break

        if len(parents) == 0:
            logger.warning(f"{mp.current_process().name} an empty chunk")

        offsprings = reproduction(parents, toolbox, cxpb, mutpb)

        evals = 0
        for i in range(len(offsprings)):
            if offsprings[i].invalid:
                offsprings[i] = toolbox.evaluate(offsprings[i])
                evals += 1

        rqueue.put((offsprings, evals))


class Worker:
    def __init__(
        self,
        toolbox: ToolBox,
        cxpb: float,
        mutpb: float,
        log_level: str | int = log.INFO,
    ) -> None:
        self.rqueue = mp.Queue()
        self.squeue = mp.Queue()

        self.worker = mp.Process(
            target=task,
            args=[self.rqueue, self.squeue, toolbox, cxpb, mutpb, log_level],
        )

        self.worker.start()

    def send(self, chunk: list | None = None) -> None:
        self.squeue.put(chunk)

    def recv(self):
        return self.rqueue.get()

    def join(self) -> None:
        self.squeue.put(None)
        self.squeue.close()
        self.squeue.join_thread()

        self.rqueue.close()
        self.rqueue.join_thread()

        self.worker.join()
