from fei.ppds import Thread, Semaphore, Mutex, print
from random import randint
from time import sleep
import barrier

NUMBER_OF_THREADS = 100


class Fibonacci:
    def __init__(self, N):
        self.N = N
        self.fibonacci_array = [0, 1] + [0] * self.N
        self.semaphore_array = [Semaphore(1)] + [Semaphore(0)
                                                 for each in range(self.N)]

    def count_fibonacci_sequence(self, thread_number):
        (print("thread %d" % thread_number, end=" -> ")
         if thread_number != (self.N - 1)
         else print("thread %d" % thread_number))

        self.fibonacci_array[thread_number + 2] = \
            self.fibonacci_array[thread_number + 1] \
            + self.fibonacci_array[thread_number]


def do_fibonacci_sequence(fib, sb, thread_number):
    # sleep(randint(1, 10) / 10)
    sb.wait()

    fib.semaphore_array[thread_number].wait()
    fib.count_fibonacci_sequence(thread_number)
    fib.semaphore_array[thread_number + 1].signal()


sb = barrier.SimpleBarrier(NUMBER_OF_THREADS)
fib = Fibonacci(NUMBER_OF_THREADS)
threads = list()
for i in range(NUMBER_OF_THREADS):
    t = Thread(do_fibonacci_sequence, fib, sb, i)
    threads.append(t)

for t in threads:
    t.join()

print('Fibonacci sequence:', fib.fibonacci_array)
