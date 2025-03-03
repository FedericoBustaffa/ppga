from multiprocessing import shared_memory as shm

import numpy as np

from ppga import base


def create_shm(population: base.Population):
    shm.SharedMemory(
        create=True, size=population.chromosomes.nbytes, name="chromosomes"
    )
    shm.SharedMemory(create=True, size=population.scores.nbytes, name="scores")


def copy_to_shm(population: base.Population):
    mem = shm.SharedMemory(create=False, name="chromosomes")
    temp = np.ndarray(
        population.chromosomes.shape, dtype=population.chromosomes.dtype, buffer=mem.buf
    )
    for i in range(len(temp)):
        temp[i][:] = population.chromosomes[i][:]

    mem = shm.SharedMemory(create=False, name="scores")
    temp = np.ndarray(
        population.scores.shape, dtype=population.scores.dtype, buffer=mem.buf
    )
    temp[:] = population.scores[:]


def copy_from_shm(population):
    mem = shm.SharedMemory(create=False, name="chromosomes")
    temp = np.ndarray(
        population.chromosomes.shape, dtype=population.chromosomes.dtype, buffer=mem.buf
    )
    for i in range(len(temp)):
        population.chromosomes[i][:] = temp[i][:]

    mem = shm.SharedMemory(create=False, name="scores")
    temp = np.ndarray(
        population.scores.shape, dtype=population.scores.dtype, buffer=mem.buf
    )
    population.scores[:] = temp[:]


def free_shm():
    mem = shm.SharedMemory(create=False, name="chromosomes")
    mem.close()
    mem.unlink()

    mem = shm.SharedMemory(create=False, name="scores")
    mem.close()
    mem.unlink()
