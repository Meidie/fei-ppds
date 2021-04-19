import time
import math


def is_prime(x):
    if x <= 1:
        return False
    elif x <= 3:
        return True
    else:
        sqrt_x = math.ceil(math.sqrt(x))
        for i in range(2, sqrt_x):
            if (x % i) == 0:
                return False
            time.sleep(0.01)
        return True


def highest_prime_below(x):
    print(f'Highest prime below {x}')
    for y in range(x - 1, 0, -1):
        if is_prime(y):
            print('→ Highest prime below {x} is {y}')
            return y
        time.sleep(0.01)
    yield


def main():
    tasks = [
        highest_prime_below(100000),
        highest_prime_below(10000),
        highest_prime_below(1000),
        highest_prime_below(100),
        highest_prime_below(18),
        highest_prime_below(17),
    ]

    done = False
    time_start = time.perf_counter()
    while not done:
        for t in tasks:
            try:
                next(t)
            except StopIteration:
                tasks.remove(t)

            if not tasks:
                done = True
    elapsed = time.perf_counter() - time_start
    print(f'Total elapsed time: {elapsed: .1f}')


if __name__ == "__main__":
    main()
