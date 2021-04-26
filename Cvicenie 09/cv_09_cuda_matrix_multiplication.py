from numba import cuda
import numpy
import math


@cuda.jit
def matmul(a, b, c):
    row, col = cuda.grid(2)
    if row < c.shape[0] and col < c.shape[1]:
        tmp = 0.
        for k in range(a.shape[1]):
            tmp += a[row, k] * b[k, col]
        c[row, col] = tmp


def main():
    a = numpy.full((24, 12), 3, numpy.float_)
    b = numpy.full((12, 22), 4, numpy.float_)

    a_global_mem = cuda.to_device(a)
    b_global_mem = cuda.to_device(b)
    c_global_mem = cuda.device_array((24, 22))

    threads_per_block = (16, 16)
    blocks_per_grid_x = int(math.ceil(a.shape[0] / threads_per_block[0]))
    blocks_per_grid_y = int(math.ceil(b.shape[1] / threads_per_block[1]))
    blocks_per_grid = (blocks_per_grid_x, blocks_per_grid_y)

    matmul[blocks_per_grid, threads_per_block](a_global_mem, b_global_mem,
                                               c_global_mem)

    c = c_global_mem.copy_to_host()

    print(c)


if __name__ == '__main__':
    main()
