import time

import psutil

from ppga import log

logger = log.getCoreLogger()


def opt_workers_num(seq, par, **kwargs):
    kwargs["max_generations"] = 1
    start = time.perf_counter()
    seq(**kwargs)
    end = time.perf_counter()
    seq_time = end - start
    logger.log(15, f"sequential time: {seq_time} seconds")

    max_cores = psutil.cpu_count(logical=False)
    assert max_cores is not None
    for i in range(2, max_cores + 1):
        kwargs.update({"workers_num": i})
        start = time.perf_counter()
        par(**kwargs)
        end = time.perf_counter()
        logger.log(15, f"parallel time with {i} workers: {end - start} seconds")
        logger.log(15, f"speed up: {seq_time / (end - start)}")

    return 1
