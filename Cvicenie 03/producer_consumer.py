from fei.ppds import Thread, Mutex, Semaphore, print, randint
from time import sleep

WAREHOUSE_CAPACITY = 10
NUMBER_OF_PRODUCERS = 5
NUMBER_OF_CONSUMERS = 5


class Warehouse:
    def __init__(self, capacity):
        self.mutex = Mutex()
        self.items = Semaphore(0)
        self.free = Semaphore(capacity)


def produce(warehouse, thread_index):
    while True:
        # produkcia
        sleep(randint(0, 10) / 100)
        # kontrola volneho miesta v sklade
        warehouse.free.wait()
        # ziskanie vylucneho pristupu do skladu
        warehouse.mutex.lock()
        # ulozenie vyrobku do skladu
        sleep(randint(0, 1) / 10)
        # odidenie zo skaldu
        warehouse.mutex.unlock()
        # zvysenie poctu vyrobkov v sklade
        warehouse.items.signal()


def consume(warehouse, thread_index):
    while True:
        # kontrola existencie polozky v sklade
        warehouse.items.wait()
        # ziskanie pristupu do skladu
        warehouse.mutex.lock()
        # ziskanie polozky
        sleep(randint(0, 1) / 10)
        # odidenie zo skladu
        warehouse.mutex.unlock()
        # uvolnenie miesta v sklade
        warehouse.free.signal()
        # spracovanie polozky
        sleep(randint(0, 10) / 10)


warehouse = Warehouse(WAREHOUSE_CAPACITY)
producers = list()
consumers = list()

for i in range(NUMBER_OF_PRODUCERS):
    producers.append(Thread(produce, warehouse, i))

for j in range(NUMBER_OF_CONSUMERS):
    consumers.append(Thread(consume, warehouse, j))

for p in producers:
    p.join()

for c in consumers:
    c.join()
