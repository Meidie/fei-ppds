from fei.ppds import Thread, Mutex, print
from random import randint
from time import sleep

NUMBER_OF_THREADS = 10


class Fibonacci:
    def __init__(self, N):
        self.N = N
        self.index = 0
        self.mutex = Mutex()
        self.fibonacci_array = [0, 1] + [0] * self.N
        self.mutex = Mutex()

    def count_fibonacci_sequence(self, thread_number):
        (print("thread %d" % thread_number, end=" -> ")
         if thread_number != (self.N - 1)
         else print("thread %d" % thread_number))

        self.fibonacci_array[thread_number + 2] = \
            self.fibonacci_array[thread_number + 1] \
            + self.fibonacci_array[thread_number]


def do_fibonacci_sequence(fib, thread_number):
    sleep(randint(1, 10) / 10)
    while True:
        fib.mutex.lock()
        if thread_number == fib.index:
            fib.count_fibonacci_sequence(thread_number)
            fib.index += 1

        fib.mutex.unlock()

        if fib.index == fib.N:
            break


fib = Fibonacci(NUMBER_OF_THREADS)
threads = list()
for i in range(NUMBER_OF_THREADS):
    t = Thread(do_fibonacci_sequence, fib, i)
    threads.append(t)

for t in threads:
    t.join()

print('Fibonacci sequence:', fib.fibonacci_array)
