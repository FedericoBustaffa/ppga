import multiprocessing as mp
import threading


class Worker(mp.Process):
    pass


class Pipeline:
    def __init__(self) -> None:
        pass

    def add(self, func, *args, **kwargs) -> None:
        pass

    def remove(self, idx: int) -> None:
        pass

    def clear(self) -> None:
        pass

    def run(self):
        pass

    def shutdown(self) -> None:
        pass
