from random import randint
from time import sleep
from fei.ppds import Thread, Event, Mutex
from fei.ppds import print


class SimpleBarrier:
    def __init__(self, N):
        self.N = N
        self.counter = 0
        self.mutex = Mutex()
        self.event = Event()

    def wait(self):
        self.mutex.lock()
        self.event.clear()
        self.counter += 1

        if self.counter == self.N:
            self.event.signal()
            self.counter = 0

        self.mutex.unlock()
        self.event.wait()


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
