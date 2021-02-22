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


# V kritickej oblasti sa nachadza len zapamatanie si indexu do pomocnej
# premennej a jeho zvysenie. Vdaka tejto modifikaci si kazde vlakno seriovo vzdy
# "zoberie" jeden index a zvysi counter, co znamena, ze dalsie vlakno uz nebude
# moct pouzit ten isty index. Toto riesenie zarucuje integritu a paralelizmus
# pretoze vlakna mozu sucasne vykonvat zapis dat do pola (v priapde ak by
# python podporoval skutocny paralelizmus)
def counter(shared):
    while True:
        shared.mutex.lock()
        tmp_index = shared.counter
        shared.counter += 1
        shared.mutex.unlock()

        if tmp_index >= shared.end:
            break

        shared.array[tmp_index] += 1


for _ in range(50):
    sh = Shared(1000000)
    t1 = Thread(counter, sh)
    t2 = Thread(counter, sh)

    t1.join()
    t2.join()

    print(Counter(sh.array))
