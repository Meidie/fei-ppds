import time
import asyncio
import math
import sys


async def is_prime(x):

    if x <= 1:
        return False
    elif x <= 3:
        return True
    else:
        sqrt_x = math.ceil(math.sqrt(x))
        for i in range(2, sqrt_x):
            if (x % i) == 0:
                return False
            await asyncio.sleep(0.01)
        return True


async def highest_prime_below(x):
    print('Highest prime below {x}')
    for y in range(x - 1, 0, -1):
        if await is_prime(y):
            print('→ Highest prime below {x} is {y}')
            return y
        await asyncio.sleep(0.01)
    return None


async def main():

    tasks = [
        highest_prime_below(100000),
        highest_prime_below(10000),
        highest_prime_below(1000),
        highest_prime_below(100),
        highest_prime_below(18),
        highest_prime_below(17),
    ]

    time_start = time.perf_counter()
    await asyncio.gather(*tasks)
    elapsed = time.perf_counter() - time_start
    print(f'Total elapsed time: {elapsed: .1f}')


if __name__ == "__main__":
    if sys.version_info[0] == 3 and sys.version_info[1] >= 8 \
            and sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
