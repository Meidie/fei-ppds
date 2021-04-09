def fib(n):
    i = 1
    a, b = 0, 1
    while True:
        if i > n:
            break
        yield b
        a, b = b, a + b
        i += 1


def print_fibonacci_sequence():
    for num in fib(5):
        print(num)


def main():
    print_fibonacci_sequence()


if __name__ == "__main__":
    main()
