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


# Jedna cela iteracia vo while cykle sa nachadza v kritickej oblasti co
# znamena ze sa bude vykonana seriovo. Toto riesenie zarucuje integritu dat
# pretoze inkrementaciu countera a zapisovanie novej hodnoty do pola vykonava
# vzdy len jedno vlakno, narozdiel od predchazajuceho riesenia obe vlakna
# vykonavaju inkrementaciu a zapis, avsak kedze je cela logika inkrementacie
# v kritickej oblasti, vykonava sa seriovo a vlakna sa len striedaju
def counter(shared):
    while True:
        shared.mutex.lock()
        if shared.counter >= shared.end:
            shared.mutex.unlock()
            break

        shared.array[shared.counter] += 1
        shared.counter += 1
        shared.mutex.unlock()


for _ in range(50):
    sh = Shared(1000000)
    t1 = Thread(counter, sh)
    t2 = Thread(counter, sh)

    t1.join()
    t2.join()

    print(Counter(sh.array))
