from fei.ppds import Mutex, Semaphore


class SimpleBarrier:
    def __init__(self, N):
        self.N = N
        self.counter = 0
        self.mutex = Mutex()
        self.barrier = Semaphore(0)

    def wait(self, each=None, last=None):
        self.mutex.lock()
        if each:
            print(each)
        self.counter += 1

        if self.counter == self.N:
            if last:
                print(last)
            self.counter = 0
            self.barrier.signal(self.N)

        self.mutex.unlock()
        self.barrier.wait()
