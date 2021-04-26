from __future__ import division
from numba import cuda
import numpy
import math


@cuda.jit
def my_kernel_2d(io_array):
    x, y = cuda.grid(2)
    if x < io_array.shape[0] and y < io_array.shape[1]:
        io_array[x][y] *= 2


def main():
    data = numpy.ones((16, 16))
    threads_per_block = (16, 16)
    blocks_per_grid_x = math.ceil(data.shape[0] / threads_per_block[0])
    blocks_per_grid_y = math.ceil(data.shape[1] / threads_per_block[1])
    blocks_per_grid = (blocks_per_grid_x, blocks_per_grid_y)
    my_kernel_2d[blocks_per_grid, threads_per_block](data)
    print(data)


if __name__ == '__main__':
    main()
