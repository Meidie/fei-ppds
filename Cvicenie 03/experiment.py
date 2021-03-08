from fei.ppds import Thread, Mutex, Semaphore, print, randint
from time import sleep

# Default parameters
WAREHOUSE_CAPACITY = 10
NUMBER_OF_PRODUCERS = 5
NUMBER_OF_CONSUMERS = 5
PRODUCTION_TIME = randint(0, 10) / 100
PROCESSING_TIME = randint(0, 10) / 10


class Warehouse:
    def __init__(self, capacity):
        self.end = False
        self.mutex = Mutex()
        self.items = Semaphore(0)
        self.free = Semaphore(capacity)

    def finish(self):
        self.end = True
        self.items.signal(50)
        self.free.signal(50)


def produce(warehouse: Warehouse, thread_index):
    while True:
        # produkcia
        sleep(PRODUCTION_TIME)
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

        if warehouse.end:
            break


def consume(warehouse: Warehouse, thread_index):
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
        sleep(PROCESSING_TIME)

        if warehouse.end:
            break


def main():
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


if __name__ == "__main__":
    main()
