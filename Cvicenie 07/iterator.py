class MyIterator:
    def __init__(self, data):
        self.data = data

    def __iter__(self):
        return self

    def __next__(self):
        if self.data:
            return self.data.pop(0)
        else:
            raise StopIteration


def with_cycle():
    print("With cycle")
    for i in MyIterator([0, 1, 2]):
        print(i)


def without_cycle():
    print("Without cycle")
    iterator = MyIterator([3, 4, 5, 6])
    print(next(iterator))
    print(next(iterator))
    print(next(iterator))
    print(next(iterator))


def try_expect():
    print("Try-expect")
    iterator = MyIterator([7, 8, 9, 10])
    try:
        print(next(iterator))
        print(next(iterator))
        print(next(iterator))
        print(next(iterator))
        print(next(iterator))
    except StopIteration:
        print("StopIteration")


def main():
    with_cycle()
    without_cycle()
    try_expect()


if __name__ == "__main__":
    main()
