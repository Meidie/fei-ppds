from random import randint
from time import sleep
from fei.ppds import Thread, Semaphore, Mutex
from fei.ppds import print


class SimpleBarrier:
    def __init__(self, N):
        self.N = N
        self.counter = 0
        self.mutex = Mutex()
        self.turnstile = Semaphore(0)

    def wait(self):
        self.mutex.lock()
        self.counter += 1

        if self.counter == self.N:
            self.counter = 0
            self.turnstile.signal()

        self.mutex.unlock()
        self.turnstile.wait()
        self.turnstile.signal()


def test(barrier, thread_id):
    sleep(randint(1, 10) / 10)
    print("vlakno %d pred barierou" % thread_id)
    barrier.wait()
    print("vlakno %d po bariere" % thread_id)


sb = SimpleBarrier(5)

threads = list()
for i in range(5):
    t = Thread(test, sb, i)
    threads.append(t)

for t in threads:
    t.join()
