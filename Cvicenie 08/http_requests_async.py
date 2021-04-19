import time
import asyncio
import aiohttp
import sys


async def task(name, work_queue):
    if work_queue.empty():
        print(f'Task {name} nothing to do')
        return

    async with aiohttp.ClientSession() as session:
        while not work_queue.empty():
            url = await work_queue.get()
            print(f'Task {name} getting url: {url}')
            time_start = time.perf_counter()
            async with session.get(url) as response:
                await response.text()
            elapsed = time.perf_counter() - time_start
            print(f'Task {name} elapsed time: {elapsed: .1f}')


async def main():
    work_queue = asyncio.Queue()

    for url in [
        'http://google.com',
        'http://microsoft.com',
        'https://facebook.com',
        'http://twitter.com',
        'http://stuba.sk',
        'http://uim.fei.stuba.sk',
    ]:
        await work_queue.put(url)

    tasks = [
        task('One', work_queue),
        task('Two', work_queue),
    ]

    time_start = time.perf_counter()
    await asyncio.gather(*tasks)
    elapsed = time.perf_counter() - time_start
    print(f'Total elapsed time: {elapsed: .1f}s')


if __name__ == "__main__":
    if sys.version_info[0] == 3 and sys.version_info[1] >= 8 \
            and sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
