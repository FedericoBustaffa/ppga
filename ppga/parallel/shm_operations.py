from multiprocessing import shared_memory as shm

import numpy as np


def create(population):
    return shm.SharedMemory(create=True, size=population.nbytes, name="population")


def copy_to_shm(population, mem: shm.SharedMemory):
    temp = np.ndarray(population.shape, dtype=population.dtype, buffer=mem.buf)
    temp[:] = population[:]


def copy_from_shm(population, mem: shm.SharedMemory):
    temp = np.ndarray(population.shape, dtype=population.dtype, buffer=mem.buf)
    population[:] = temp[:]
