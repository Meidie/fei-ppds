from __future__ import division
from numba import cuda
import numpy
import math


@cuda.jit
def my_kernel(io_array):
    pos = cuda.grid(1)
    if pos < io_array.size:
        io_array[pos] *= 2


def main():
    data = numpy.ones(256)
    threads_per_block = 256
    blocks_per_grid = math.ceil(data.shape[0] / threads_per_block)
    my_kernel[blocks_per_grid, threads_per_block](data)
    print(data)


if __name__ == '__main__':
    main()
