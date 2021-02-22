__author__ = 'Matúš Pohančenik'
__credits__ = 'Matúš Jókay'

from fei.ppds import Thread, Mutex
from collections import Counter


class Shared:
    def __init__(self, end):
        self.counter = 0
        self.end = end
        self.array = [0] * self.end
        self.mutex = Mutex()


# While cyklus, ktory sa nachadza v kritickej oblasti bude vykonany seriovo to
# znamena, ze ho vzdy cely vykona len jedno vlakno a az potom dalsie. Taketo
# riesenie sice zarucuje integritu dat avsak kompletne eliminuje paralelizmus.
# Ked pride rad na druhe vlakno counter uz bude na konci pola a teda 
# v pripade druheho vlakna sa hned zavola break.
def counter(shared):
    shared.mutex.lock()
    while True:

        if shared.counter >= shared.end:
            break

        shared.array[shared.counter] += 1
        shared.counter += 1
    shared.mutex.unlock()


for _ in range(50):
    sh = Shared(1000000)
    thread1 = Thread(counter, sh)
    thread2 = Thread(counter, sh)

    thread1.join()
    thread2.join()

    print(Counter(sh.array))
