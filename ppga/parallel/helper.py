import math
import time

import psutil

from ppga import log

logger = log.getCoreLogger()


def opt_workers_num(seq, par, **kwargs):
    kwargs["max_generations"] = 2
    start = time.perf_counter()
    seq(**kwargs)
    end = time.perf_counter()
    seq_time = end - start
    logger.log(15, f"sequential time: {seq_time} seconds")

    max_cores = psutil.cpu_count(logical=False)
    assert max_cores is not None
    best = 1
    for i in range(2, max_cores + 1, 2):
        kwargs.update({"workers_num": i})
        start = time.perf_counter()
        par(**kwargs)
        end = time.perf_counter()
        par_time = end - start
        speed_up = seq_time / par_time
        logger.log(15, f"parallel time with {i} workers: {par_time} seconds")
        logger.log(15, f"speed up: {speed_up}")

        # select the best number of workers
        if math.ceil(speed_up) < i:
            return math.ceil(speed_up)

        if speed_up > best:
            best = math.ceil(speed_up)
        else:
            return best

    return best
