from time import sleep
from random import randint
from fei.ppds import Thread, Mutex, Semaphore, print
from barrier import Barrier

N_SAVAGES = 5
N_COOKS = 5
N_SERVINGS = 10


class Dinner(object):
    def __init__(self):
        self.servings = 0
        self.cook_counter = 0

        self.cook_mutex = Mutex()
        self.savage_mutex = Mutex()
        self.barrier = Barrier(N_COOKS)
        self.empty_pot = Semaphore(0)
        self.full_pot = Semaphore(0)

    def get_serving_from_pot(self, savage_id):
        print("divoch %2d: beriem si porciu" % savage_id)
        self.servings -= 1

    def put_servings_in_pot(self, cook_id, n):
        print(f"kuchár {cook_id}: vkladá jedlo do hrnca")
        sleep(0.5 + randint(0, 3) / 10)
        self.servings += n


def eat(savage_id):
    print(f"divoch {savage_id}: hoduje")
    sleep(0.2 + randint(0, 3) / 10)


def cooking(cook_id):
    print(f"kuchár {cook_id}: pripravuje jedlo")
    sleep((0.02 * N_SERVINGS) + randint(0, 3) / N_COOKS)


def cook(dinner: Dinner, cook_id):
    while True:
        # čakanie kým bude hrniec prázdny
        dinner.empty_pot.wait()
        # varenie
        cooking(cook_id)

        # počkanie kým všetci kuchári dokončia svoju prácu
        dinner.barrier.wait()

        dinner.cook_mutex.lock()
        dinner.cook_counter += 1
        tmp_counter = dinner.cook_counter
        dinner.cook_mutex.unlock()

        if tmp_counter == N_COOKS:
            dinner.cook_counter = 0
            # vloženie porcii do hrnca
            dinner.put_servings_in_pot(cook_id, N_SERVINGS)
            # signalizácia pre divochov, že môžu hodovať
            dinner.full_pot.signal()


def savage(dinner: Dinner, savage_id):
    sleep(randint(0, 3) / 10)

    while True:
        dinner.savage_mutex.lock()
        print(f"divoch {savage_id}: pocet porcii v hrnci je {dinner.servings}")
        if dinner.servings == 0:
            print(f"divoch {savage_id}: budim kucharov")
            # nabitie semaforu na počet kuchárov
            dinner.empty_pot.signal(N_COOKS)
            dinner.full_pot.wait()
        dinner.get_serving_from_pot(savage_id)
        dinner.savage_mutex.unlock()
        eat(savage_id)


def create_savages_and_cooks(dinner: Dinner, savages: list, cooks: list):
    for savage_id in range(N_SAVAGES):
        savages.append(Thread(savage, dinner, savage_id))

    for cook_id in range(N_COOKS):
        cooks.append(Thread(cook, dinner, cook_id))


def wait_to_finish(savages: list, cooks: list):
    for s in savages:
        s.join()

    for c in cooks:
        c.join()


def main():
    dinner = Dinner()
    savages, cooks = list(), list()

    create_savages_and_cooks(dinner, savages, cooks)
    wait_to_finish(savages, cooks)


if __name__ == '__main__':
    main()
