import sys


def main(make_tests):
    if make_tests:
        with open("input_test.txt", "r") as f:
            data = f.readlines()

        result = first(data)
        expected = 1
        assert expected == result, f"Result 1: Expected {expected}, actual {result}"
        result = second(data)
        expected = 1
        assert expected == result, f"Result 2: Expected {expected}, actual {result}"

    with open("input.txt", "r") as f:
        data = f.readlines()

    result = first(data)
    print(f"Result 1: {result}")
    result = second(data)
    print(f"Result 2: {result}")


def first(lines: list[str]):
    return 0


def second(lines: list[str]):
    return 0


if __name__ == '__main__':
    main(make_tests=len(sys.argv) > 1 and sys.argv[1] == "--tests")
