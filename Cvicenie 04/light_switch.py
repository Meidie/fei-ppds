from fei.ppds import Mutex, Semaphore


class LightSwitch:
    def __init__(self):
        self.mutex = Mutex()
        self.counter = 0

    def lock(self, semaphore: Semaphore):
        self.mutex.lock()
        prev_count = self.counter
        self.counter += 1
        if self.counter == 1:
            semaphore.wait()
        self.mutex.unlock()
        return prev_count

    def unlock(self, semaphore: Semaphore):
        self.mutex.lock()
        self.counter -= 1
        if self.counter == 0:
            semaphore.signal()
        self.mutex.unlock()
