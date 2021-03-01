from random import randint
from time import sleep
from fei.ppds import Thread, Semaphore, Mutex
from fei.ppds import print


class Barrier:
    def __init__(self, N):
        self.N = N
        self.counter = 0
        self.mutex = Mutex()
        self.turnstile1 = Semaphore(0)
        self.turnstile2 = Semaphore(0)

    def wait_turnstile1(self):
        self.mutex.lock()
        self.counter += 1

        if self.counter == self.N:
            self.turnstile1.signal(self.N)

        self.mutex.unlock()
        self.turnstile1.wait()

    def wait_turnstile2(self):
        self.mutex.lock()
        self.counter -= 1

        if self.counter == 0:
            self.turnstile2.signal(self.N)

        self.mutex.unlock()
        self.turnstile2.wait()


def rendezvous(thread_name):
    sleep(randint(1, 10) / 10)
    print('rendezvous: %s' % thread_name)


def ko(thread_name):
    print('ko: %s' % thread_name)
    sleep(randint(1, 10) / 10)


def reusable_barrier_test(sb, thread_name):
    while True:
        rendezvous(thread_name)
        sb.wait_turnstile1()
        ko(thread_name)
        sb.wait_turnstile2()


sb = Barrier(5)

threads = list()
for i in range(5):
    t = Thread(reusable_barrier_test, sb, f'Thread {i}')
    threads.append(t)

for t in threads:
    t.join()
