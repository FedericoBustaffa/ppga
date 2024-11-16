import multiprocessing as mp
import multiprocessing.queues as mpq

from ppga import log
from ppga.algorithms.reproduction import reproduction
from ppga.base.toolbox import ToolBox


def task(
    rqueue: mpq.JoinableQueue,
    squeue: mpq.JoinableQueue,
    toolbox: ToolBox,
    cxpb: float,
    mutpb: float,
    log_level: str | int = log.INFO,
):
    logger = log.getCoreLogger(log_level)
    while True:
        parents = squeue.get()
        squeue.task_done()
        if parents is None:
            break

        if len(parents) == 0:
            logger.warning(f"{mp.current_process().name} an empty chunk")

        offsprings = reproduction(parents, toolbox, cxpb, mutpb)

        evals = 0
        for i in range(len(offsprings)):
            if not offsprings[i].valid:
                offsprings[i] = toolbox.evaluate(offsprings[i])
                evals += 1

        rqueue.put((offsprings, evals))


class Worker(mp.Process):
    def __init__(
        self,
        toolbox: ToolBox,
        cxpb: float,
        mutpb: float,
        log_level: str | int = log.INFO,
    ) -> None:
        self.rqueue = mp.JoinableQueue()
        self.squeue = mp.JoinableQueue()

        super().__init__(
            target=task,
            args=[self.rqueue, self.squeue, toolbox, cxpb, mutpb, log_level],
        )

    def send(self, chunk: list | None = None) -> None:
        self.squeue.put(chunk)

    def recv(self):
        result = self.rqueue.get()
        self.rqueue.task_done()

        return result

    def join(self, timeout: float | None = None) -> None:
        self.squeue.put(None)

        # self.squeue.close()
        # self.rqueue.close()
        # self.squeue.join_thread()
        # self.rqueue.join_thread()

        super().join(timeout)
