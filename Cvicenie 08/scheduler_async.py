import time
import asyncio


async def task(name, work_queue):
    if work_queue.empty():
        print(f'Task {name} nothing to do')
        return

    while not work_queue.empty():
        delay = await work_queue.get()

        print(f'Task {name} running')
        time_start = time.perf_counter()
        await asyncio.sleep(delay)
        elapsed = time.perf_counter() - time_start
        print(f'Task {name} elapsed time: {elapsed: .1f}')


async def main():
    work_queue = asyncio.Queue()

    for work in [3, 1, 9, 17]:
        await work_queue.put(work)

    tasks = [
        task('One', work_queue),
        task('Two', work_queue),
    ]

    time_start = time.perf_counter()
    await asyncio.gather(*tasks)
    elapsed = time.perf_counter() - time_start
    print(f'Total elapsed time: {elapsed}')


if __name__ == "__main__":
    asyncio.run(main())
