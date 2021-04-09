def generator(n):
    while n:
        n -= 1
        yield n


def with_cycle():
    print("With cycle")
    my_generator = generator(3)
    print(my_generator)
    for i in my_generator:
        print(i)


def without_cycle():
    print("Without cycle")
    my_generator = generator(3)
    print(my_generator)
    print(next(my_generator))
    print(next(my_generator))
    print(next(my_generator))


def try_expect():
    print("Try-expect")
    my_generator = generator(3)
    print(my_generator)
    try:
        print(next(my_generator))
        print(next(my_generator))
        print(next(my_generator))
        print(next(my_generator))
    except StopIteration:
        print("StopIteration")


def main():
    with_cycle()
    without_cycle()
    try_expect()


if __name__ == "__main__":
    main()
