from fei.ppds import Thread, Semaphore, print, randint
from light_switch import LightSwitch
from time import sleep

NUMBER_OF_READERS = 5
NUMBER_OF_WRITERS = 5


class Room:
    def __init__(self):
        self.light_switch = LightSwitch()
        self.room_empty = Semaphore(1)
        self.turnstile = Semaphore(1)  # turnstile to prevent starvation


def read(room, thread_id):
    while True:
        sleep(randint(0, 1) / 10)
        room.turnstile.wait()
        room.turnstile.signal()
        room.light_switch.lock(room.room_empty)

        (print("Thread [{0}] started reading, {1} threads reading".format(
            thread_id, room.light_switch.counter))
         if room.light_switch.counter != 1
         else print("Thread [{0}] started reading, {1} thread reading".format(
            thread_id, room.light_switch.counter)))

        sleep(randint(0, 10) / 100)
        room.light_switch.unlock(room.room_empty)

        (print("Thread [{0}] finished reading, {1} threads reading".format(
            thread_id, room.light_switch.counter))
         if room.light_switch.counter != 1
         else print("Thread [{0}] finished reading, {1} thread reading".format(
            thread_id, room.light_switch.counter)))


def write(room, thread_id):
    while True:
        sleep(randint(0, 1) / 10)
        room.turnstile.wait()
        room.room_empty.wait()
        print("Thread [%d] started writing" % thread_id)
        sleep(randint(0, 10) / 100)
        room.room_empty.signal()
        room.turnstile.signal()
        print("Thread [%d] finished writing" % thread_id)


room = Room()
readers = list()
writers = list()

for i in range(NUMBER_OF_READERS):
    readers.append(Thread(read, room, i))

for j in range(NUMBER_OF_WRITERS):
    writers.append(Thread(write, room, j))

for r in readers:
    r.join()

for w in writers:
    w.join()
