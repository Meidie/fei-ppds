import numpy as np
from numba import cuda
import math


@cuda.jit
def is_prime(primes, results):
    num = primes[cuda.grid(1)]
    flag = True

    if num > 1:
        sqrt_x = math.ceil(math.sqrt(num))
        for i in range(2, sqrt_x):
            if (num % i) == 0:
                flag = False
                break

    results[num] = flag


def main():
    numbers = np.random.randint(1000000, 9999999999999, size=320,
                                dtype=np.int64)
    results = dict()

    threads_per_block = 32
    blocks_per_grid = math.ceil(len(numbers) / threads_per_block)
    is_prime[blocks_per_grid, threads_per_block](numbers, results)

    print(results)
    print(f'primes found: {sum(results.values())}')


if __name__ == '__main__':
    main()
