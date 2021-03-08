from fei.ppds import Thread, Mutex, Semaphore, print, randint
from time import sleep
import matplotlib.pyplot as plt

# Default parameters
WAREHOUSE_CAPACITY = 10
NUMBER_OF_CONSUMERS = 5
OPERATING_TIME = 0.1
TIME_DIVIDER = 200


class Results:
    def __init__(self):
        self.data = []


class Warehouse:
    def __init__(self):
        self.closed = False
        self.mutex = Mutex()
        self.items = Semaphore(0)
        self.free = Semaphore(WAREHOUSE_CAPACITY)
        self.items_produced = 0

    def reset(self):
        self.closed = False
        self.items = Semaphore(0)
        self.free = Semaphore(WAREHOUSE_CAPACITY)
        self.items_produced = 0

    def finish(self):
        self.closed = True
        self.items.signal(100)
        self.free.signal(100)

    def add_product(self):
        self.items_produced += 1


def produce(warehouse: Warehouse, time_to_produce):
    while True:
        # produkcia
        sleep(time_to_produce)
        # kontrola volneho miesta v sklade
        warehouse.free.wait()
        # ziskanie vylucneho pristupu do skladu
        warehouse.mutex.lock()
        # ulozenie vyrobku do skladu
        warehouse.add_product()
        # sleep(randint(0, 1) / 10)
        # odidenie zo skaldu
        warehouse.mutex.unlock()
        # zvysenie poctu vyrobkov v sklade
        warehouse.items.signal()

        if warehouse.closed:
            break


def consume(warehouse: Warehouse):
    while True:
        # kontrola existencie polozky v sklade
        warehouse.items.wait()
        # ziskanie pristupu do skladu
        warehouse.mutex.lock()
        # ziskanie polozky
        # sleep(randint(0, 1) / 10)
        # odidenie zo skladu
        warehouse.mutex.unlock()
        # uvolnenie miesta v sklade
        warehouse.free.signal()
        # spracovanie polozky
        sleep(randint(0, 10) / TIME_DIVIDER)

        if warehouse.closed:
            break


def wait_to_finish(producers: list, consumers: list):
    for p in producers:
        p.join()

    for c in consumers:
        c.join()


def main():
    results = Results()
    warehouse = Warehouse()
    producers = list()
    consumers = list()

    iteration = 0
    for production_time in range(2, 12):
        for number_of_producers in range(1, 11):
            items_produced = 0
            repetitions = 10

            for rep in range(repetitions):
                warehouse.reset()
                consumers.clear()
                producers.clear()

                for i in range(number_of_producers):
                    producers.append(
                        Thread(produce, warehouse,
                               production_time / TIME_DIVIDER))

                for j in range(NUMBER_OF_CONSUMERS):
                    consumers.append(Thread(consume, warehouse))

                sleep(OPERATING_TIME)
                warehouse.finish()
                wait_to_finish(producers, consumers)

                items_produced += warehouse.items_produced / OPERATING_TIME

            items_produced_avg = items_produced / repetitions
            results.data.append((production_time / TIME_DIVIDER,
                                 number_of_producers, items_produced_avg))
            iteration += 1
            print("Iteration {0}/100".format(iteration))
    plot(results.data)


def plot(results):
    fig = plt.figure()

    ax = plt.gca(projection='3d')
    ax.set_xlabel('Produkcia [s]]')
    ax.set_ylabel('Počet producentov')
    ax.set_zlabel('Počet výrobkov za sekundu')

    x = [x[0] for x in results]
    y = [y[1] for y in results]
    z = [z[2] for z in results]

    ax.plot_trisurf(x, y, z, cmap='viridis', edgecolor='none')
    plt.show()


if __name__ == "__main__":
    main()
