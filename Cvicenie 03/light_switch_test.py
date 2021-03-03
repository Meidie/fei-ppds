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
            print("First thread [%d] entered and"
                  " turned on the light" % thread_number)
            semaphore.wait()
        else:
            (print("Thread [{0}] entered, {1} threads inside".format(
                thread_number, self.counter))
             if self.counter != 1
             else print("Thread [{0}] entered, {1} thread inside".format(
                thread_number, self.counter)))
        self.mutex.unlock()

    def unlock(self, semaphore, thread_number):
        self.mutex.lock()
        self.counter -= 1
        if self.counter == 0:
            print("Last thread [%d] left and"
                  " turned off the light" % thread_number)
            semaphore.signal()
        else:
            (print("Thread [{0}] left, {1} threads inside".format(
                thread_number, self.counter))
             if self.counter != 1
             else print("Thread [{0}] left, {1} thread inside".format(
                thread_number, self.counter)))
        self.mutex.unlock()


def test_light_switch(ls, semaphore, thread_number):
    sleep(randint(1, 10) / 10)
    ls.lock(semaphore, thread_number)
    sleep(randint(1, 10) / 10)
    ls.unlock(semaphore, thread_number)


switch = LightSwitch()
sem = Semaphore(1)
threads = list()
for i in range(5):
    t = Thread(test_light_switch, switch, sem, i)
    threads.append(t)

for t in threads:
    t.join()
