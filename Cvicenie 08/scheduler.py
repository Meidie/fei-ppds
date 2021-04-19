import queue
import time


def task(name, work_queue):
    if work_queue.empty():
        print(f'Task {name} nothing to do')
        return

    while not work_queue.empty():
        delay = work_queue.get()

        print(f'Task {name} running')
        time_start = time.perf_counter()
        time.sleep(delay)
        elapsed = time.perf_counter() - time_start
        print(f'Task {name} elapsed time: {elapsed: .1f}')
        yield


def main():
    work_queue = queue.Queue()

    for work in [3, 1, 9, 17]:
        work_queue.put(work)

    tasks = [
        task('One', work_queue),
        task('Two', work_queue),
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
    print(f'Total elapsed time: {elapsed}')


if __name__ == "__main__":
    main()
