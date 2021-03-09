from time import sleep
from random import randint
from fei.ppds import Semaphore, Thread, print

PHIL_NUM = 5


class Dinner:
    def __init__(self, n_philosophers):
        self.n_philosophers = n_philosophers
        self.forks = [Semaphore(1) for _ in range(self.n_philosophers)]
        self.footman = Semaphore(self.n_philosophers - 1)

    def get_right_fork(self, phil_id):
        self.forks[phil_id].wait()

    def get_left_fork(self, phil_id):
        self.forks[(phil_id + 1) % self.n_philosophers].wait()

    def put_right_fork(self, phil_id):
        self.forks[phil_id].signal()

    def put_left_fork(self, phil_id):
        self.forks[(phil_id + 1) % self.n_philosophers].signal()


def think(phil_id):
    print("Philosopher {:2d} is thinking.".format(phil_id))
    sleep(randint(40, 50) / 1000)


def eat(phil_id):
    print("Philosopher {:2d} is eating.".format(phil_id))
    sleep(randint(40, 50) / 1000)
    print("Philosopher {:2d} has finished eating.".format(phil_id))


def get_forks(dinner: Dinner, phil_id):
    dinner.footman.wait()
    print("Philosopher {:2d} is trying to get forks.".format(phil_id))
    dinner.get_right_fork(phil_id)
    dinner.get_left_fork(phil_id)
    print("Philosopher {:2d} has both forks.".format(phil_id))


def put_forks(dinner: Dinner, phil_id):
    print("Philosopher {:2d} is putting down forks.".format(phil_id))
    dinner.forks[phil_id].signal()
    dinner.forks[(phil_id + 1) % dinner.n_philosophers].signal()
    print("Philosopher {:2d} put down forks.".format(phil_id))
    dinner.footman.signal()


def dine(dinner: Dinner, phil_id):
    sleep(randint(40, 100) / 1000)

    while True:
        think(phil_id)
        get_forks(dinner, phil_id)
        eat(phil_id)
        put_forks(dinner, phil_id)


def main():
    dinner = Dinner(PHIL_NUM)
    philosophers = list()

    for p_id in range(PHIL_NUM):
        philosophers.append(Thread(dine, dinner, p_id))

    for p in philosophers:
        p.join()


if __name__ == '__main__':
    main()
