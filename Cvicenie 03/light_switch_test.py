from fei.ppds import Thread, Mutex, Semaphore, print
from time import sleep
from random import randint


class LightSwitch:
    def __init__(self):
        self.mutex = Mutex()
        self.counter = 0

    def lock(self, semaphore, thread_number):
        self.mutex.lock()
        self.counter += 1
        if self.counter == 1:
            print("light up (thread: %d)" % thread_number)
            semaphore.wait()
        self.mutex.unlock()

    def unlock(self, semaphore, thread_number):
        self.mutex.lock()
        self.counter -= 1
        if self.counter == 0:
            print("turn off (thread: %d)" % thread_number)
            semaphore.signal()
        self.mutex.unlock()


def test_light_switch(ls, semaphore, thread_number):
    ls.lock(semaphore, thread_number)
    sleep(randint(1, 10) / 10)
    print("testing (thread: %d)" % thread_number)
    ls.unlock(semaphore, thread_number)


switch = LightSwitch()
sem = Semaphore(1)
threads = list()
for i in range(10):
    t = Thread(test_light_switch, switch, sem, i)
    threads.append(t)

for t in threads:
    t.join()
