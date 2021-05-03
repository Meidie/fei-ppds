import numpy as np
from numba import cuda
from time import perf_counter
import math

NUM_ARRAYS = 5


@cuda.jit
def is_prime(primes, results):
    pos = cuda.grid(1)
    num = primes[pos]
    flag = True

    if num > 3:
        sqrt_x = math.ceil(math.sqrt(num))
        for i in range(2, sqrt_x + 1):
            if (num % i) == 0:
                flag = False
                break
    elif num <= 1:
        flag = False

    results[pos] = flag


def main():
    streams = []
    data_gpu = []
    results_gpu = []
    results_gpu_out = []
    threads_per_block = 32

    for _ in range(NUM_ARRAYS):
        streams.append(cuda.stream())

    t_start = perf_counter()

    for i in range(NUM_ARRAYS):
        data_gpu.append(cuda.to_device(
            np.random.randint(1_000_000, 9_999_999_999_999, size=64,
                              dtype=np.int64), stream=streams[i]))
        results_gpu.append(
            cuda.to_device(np.empty(64, dtype=bool), stream=streams[i]))

    for i in range(NUM_ARRAYS):
        blocks_per_grid = math.ceil(len(data_gpu[i]) / threads_per_block)
        is_prime[blocks_per_grid, threads_per_block,
                 streams[i]](data_gpu[i], results_gpu[i])

    for i in range(NUM_ARRAYS):
        results_gpu_out.append(
            (results_gpu[i].copy_to_host(stream=streams[i])))

    t_end = perf_counter()

    print(f'Total time: {t_end - t_start:.2f} s')

    for i in range(0, len(data_gpu)):
        print(dict(zip(data_gpu[i], results_gpu_out[i])))


if __name__ == '__main__':
    main()
