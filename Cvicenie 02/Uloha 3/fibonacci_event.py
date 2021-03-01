from fei.ppds import Thread, Event, Mutex, print
from random import randint
from time import sleep

NUMBER_OF_THREADS = 10


class Fibonacci:
    def __init__(self, N):
        self.N = N
        self.counter = 0
        self.mutex = Mutex()
        self.fibonacci_array = [0, 1] + [0] * self.N
        self.event_array = [Event() for each in range(self.N + 1)]
        self.event_array[0].signal()

    def count_fibonacci_sequence(self, thread_number):
        (print("thread %d" % thread_number, end=" -> ")
         if thread_number != (self.N - 1)
         else print("thread %d" % thread_number))

        self.fibonacci_array[thread_number + 2] = \
            self.fibonacci_array[thread_number + 1] \
            + self.fibonacci_array[thread_number]


def do_fibonacci_sequence(fib, thread_number):
    sleep(randint(1, 10) / 10)

    fib.event_array[thread_number].wait()
    fib.count_fibonacci_sequence(thread_number)
    fib.event_array[thread_number + 1].signal()


fib = Fibonacci(NUMBER_OF_THREADS)
threads = list()
for i in range(NUMBER_OF_THREADS):
    t = Thread(do_fibonacci_sequence, fib, i)
    threads.append(t)

for t in threads:
    t.join()

print('Fibonacci sequence:', fib.fibonacci_array)
