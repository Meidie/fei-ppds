from random import randint
from time import sleep
from fei.ppds import Thread, Semaphore, Mutex
from fei.ppds import print


class SimpleBarrier:
    def __init__(self, N):
        self.N = N
        self.counter = 0
        self.mutex = Mutex()
        self.barrier = Semaphore(0)

    def wait(self):
        self.mutex.lock()
        self.counter += 1

        if self.counter == self.N:
            self.counter = 0
            self.barrier.signal(self.N)

        self.mutex.unlock()
        self.barrier.wait()


def rendezvous(thread_name):
    sleep(randint(1, 10) / 10)
    print('rendezvous: %s' % thread_name)


def ko(thread_name):
    print('ko: %s' % thread_name)
    sleep(randint(1, 10) / 10)


def reusable_barrier_test(sb1, sb2, thread_name):
    while True:
        rendezvous(thread_name)
        sb1.wait()
        ko(thread_name)
        sb2.wait()


sb1 = SimpleBarrier(5)
sb2 = SimpleBarrier(5)

threads = list()
for i in range(5):
    t = Thread(reusable_barrier_test, sb1, sb2, f'Thread {i}')
    threads.append(t)

for t in threads:
    t.join()
