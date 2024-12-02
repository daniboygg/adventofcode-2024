from collections import Counter


def main():
    with open("input.txt", "r") as f:
        data = f.readlines()

    result = first(data)
    print(f"Result 1: {result}")

    result = second(data)
    print(f"Result 2: {result}")


def first(lines: list[str]):
    col_1 = []
    col_2 = []

    for line in lines:
        f, s = line.split("   ")
        col_1.append(int(f))
        col_2.append(int(s))

    col_1 = sorted(col_1)
    col_2 = sorted(col_2)

    total = 0

    for f, s in zip(col_1, col_2):
        total += max(f, s) - min(f, s)

    return total


def second(lines: list[str]):
    col_1 = []
    col_2 = []

    for line in lines:
        i, s = line.split("   ")
        col_1.append(int(i))
        col_2.append(int(s))

    total = 0

    c = Counter(col_2)
    for i in col_1:
        total += i * c.get(i, 0)

    return total


if __name__ == '__main__':
    main()
