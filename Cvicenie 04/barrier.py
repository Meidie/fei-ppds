from fei.ppds import Semaphore, Mutex


class Barrier:
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
