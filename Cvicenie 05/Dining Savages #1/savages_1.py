from time import sleep
from random import randint
from fei.ppds import Thread, Mutex, Semaphore, print
from simple_barrier import SimpleBarrier

N_SAVAGES = 10
N_SERVINGS = 13


class Shared:
    def __init__(self, n_savages):
        self.servings = 0
        self.mutex = Mutex()
        self.empty_pot = Semaphore(0)
        self.full_pot = Semaphore(0)
        self.barrier1 = SimpleBarrier(n_savages)
        self.barrier2 = SimpleBarrier(n_savages)

    def get_serving_from_pot(self, savage_id):
        # print("divoch %2d: beriem si porciu" % savage_id)
        self.servings -= 1

    def put_servings_in_pot(self, n):
        # print("kuchar: varim")
        sleep(0.5 + randint(0, 3) / 10)
        self.servings += n


def eat(savage_id):
    print("divoch %2d: hodujem" % savage_id)
    sleep(randint(50, 200) / 100)


def cook(shared: Shared, cook_id):
    while True:
        shared.empty_pot.wait()
        shared.put_servings_in_pot(N_SERVINGS)
        shared.full_pot.signal()


def savage(shared: Shared, savage_id):
    while True:
        shared.barrier2.wait(each=f"savage {savage_id}: pred vecerou",
                             last=f"savage {savage_id}: sme vsetci, zaciname"
                                   f"hodovat")
        shared.mutex.lock()
        print("divoch %2d: pocet zostavajucich porcii v hrnci je %2d" %
              (savage_id, shared.servings))
        if shared.servings == 0:
            print("divoch %2d: budim kuchara" % savage_id)
            shared.empty_pot.signal()
            shared.full_pot.wait()
        shared.get_serving_from_pot(savage_id)
        shared.mutex.unlock()
        eat(savage_id)
        shared.barrier1.wait()


def create_savages(shared: Shared, savages: list):
    for savage_id in range(N_SAVAGES):
        savages.append(Thread(savage, shared, savage_id))


def wait_to_finish(savages: list, chef: Thread):
    for s in savages:
        s.join()

    chef.join()


def main():
    shared = Shared(N_SAVAGES)
    savages = list()
    chef = Thread(cook, shared, 0)
    create_savages(shared, savages)
    wait_to_finish(savages, chef)


if __name__ == '__main__':
    main()
