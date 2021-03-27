from time import sleep
from queue import Queue
from random import randint
from fei.ppds import Thread, Mutex, Semaphore, print

N_CHAIRS = 5


class BarberShop:
    def __init__(self, N):
        self.N = N
        self.n_customers = 0
        self.mutex = Mutex()
        self.queue = Queue()
        self.customer = Semaphore(0)
        self.customer_done = Semaphore(0)
        self.barber_done = Semaphore(0)


def cut_hair():
    print("Barber is cutting customer's hair")
    sleep(randint(1, 10) / 10)


def get_hair_cut(custom_id):
    sleep(randint(1, 10) / 10)
    print(f"Customer {custom_id} is getting haircut.")


def customer(barber_shop: BarberShop, barber_semaphore, customer_id):
    while True:
        sleep(randint(9, 10) / 10)
        barber_shop.mutex.lock()
        if barber_shop.n_customers == barber_shop.N:
            print(f"Customer {customer_id}: Barber shop is full! I'm leaving!")
            barber_shop.mutex.unlock()
            continue
        barber_shop.n_customers += 1
        print(
            f"Customer {customer_id} entered the barber shop. There are/is "
            f"[{barber_shop.N - barber_shop.n_customers}] chair/chairs left.")

        barber_shop.queue.put(barber_semaphore)
        barber_shop.mutex.unlock()

        barber_shop.customer.signal()
        barber_semaphore.wait()

        get_hair_cut(customer_id)
        barber_shop.customer_done.signal()
        barber_shop.barber_done.wait()

        barber_shop.mutex.lock()
        barber_shop.n_customers -= 1
        print(
            f"Customer {customer_id} is leaving with a new haircut. "
            f"There are/is [{barber_shop.N - barber_shop.n_customers}] "
            f"chair/chair left!")
        barber_shop.mutex.unlock()


def barber(barber_shop: BarberShop):
    while True:
        barber_shop.customer.wait()
        barber_shop.mutex.lock()
        barber_semaphore = barber_shop.queue.get()
        print("Barber is calling in a new customer.")
        barber_shop.mutex.unlock()
        barber_semaphore.signal()
        cut_hair()
        barber_shop.customer_done.wait()
        print("Haircut is finished!")
        barber_shop.barber_done.signal()


def main():
    barber_shop = BarberShop(N_CHAIRS)

    customers = list()
    b = Thread(barber, barber_shop)

    for customer_id in range(10):
        customers.append(
            Thread(customer, barber_shop, Semaphore(0), customer_id))

    b.join()
    for c in customers:
        c.join()


if __name__ == '__main__':
    main()
