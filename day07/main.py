import itertools
import operator
import os


def main():
    with open("input.txt", "r") as f:
        data = f.readlines()

    result = first(data)
    print(f"Result 1: {result}")

    result = second(data)
    print(f"Result 2: {result}")


def first(lines: list[str]):
    total = 0
    for n_line, line in enumerate(lines):
        expected_result, numbers = line.split(":")
        expected_result = int(expected_result)
        numbers = [int(n) for n in numbers.strip().split(" ")]

        if is_valid(numbers, expected_result, [operator.add, operator.mul], n_line):
            total += expected_result

    return total


def second(lines: list[str]):
    total = 0
    for n_line, line in enumerate(lines):
        expected_result, numbers = line.split(":")
        expected_result = int(expected_result)
        numbers = [int(n) for n in numbers.strip().split(" ")]

        if is_valid(numbers, expected_result, [operator.add, operator.mul, concat], n_line):
            total += expected_result

    return total


def concat(a, b):
    return int(f"{a}{b}")


def is_valid(numbers, expected_result, possible_operators, n_line) -> bool:
    between = len(numbers) - 1
    operators_list = list(itertools.product(possible_operators, repeat=between))

    for iteration, operators in enumerate(operators_list):
        result = numbers[0]
        for i in range(1, len(numbers)):
            result = operators[i - 1](result, numbers[i])

        if result == expected_result:
            return True

    return False


if __name__ == '__main__':
    main()
