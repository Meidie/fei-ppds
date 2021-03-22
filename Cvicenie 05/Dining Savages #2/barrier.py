from fei.ppds import Mutex, Semaphore


class Barrier:
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
