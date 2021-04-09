class Fibonacci:
    def __init__(self, n):
        self.a = 0
        self.b = 1
        self.cnt = 1
        self.n = n

    def __iter__(self):
        return self

    def __next__(self):
        if self.cnt > self.n:
            raise StopIteration
        if self.cnt > 1:
            self.a, self.b = self.b, self.a + self.b
        self.cnt += 1
        return self.b


def print_fibonacci_sequence():
    for i in Fibonacci(5):
        print(i)


def main():
    print_fibonacci_sequence()


if __name__ == "__main__":
    main()
