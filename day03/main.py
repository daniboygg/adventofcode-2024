import re


def main():
    with open("input.txt", "r") as f:
        data = f.readlines()

    result = first(data)
    print(f"Result 1: {result}")

    result = second(data)
    print(f"Result 2: {result}")


def first(lines: list[str]):
    total = 0
    for line in lines:
        for match in re.finditer(r"mul\((\d{1,3}),(\d{1,3})\)", line):
            total += int(match.group(1)) * int(match.group(2))
    return total


def second(lines: list[str]):
    total = 0
    enabled = True
    for line in lines:
        for match in re.finditer(r"mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\)", line):
            if match.group(0) == "do()":
                enabled = True
            elif match.group(0) == "don't()":
                enabled = False
            elif enabled:
                total += int(match.group(1)) * int(match.group(2))
    return total


if __name__ == '__main__':
    main()
