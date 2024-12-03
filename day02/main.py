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
        items = list(map(lambda x: int(x), line.split(" ")))
        if is_safe(items):
            total += 1
    return total


def second(lines: list[str]):
    total = 0
    for line in lines:
        items = list(map(lambda x: int(x), line.split(" ")))
        if is_safe(items):
            total += 1
            continue

        for i in range(len(items)):
            new_items = items[:]
            new_items.pop(i)
            if is_safe(new_items):
                total += 1
                break
    return total


def is_safe(items: list[int]):
    last_number = items[0]
    last_diff = 0
    for number in items[1:]:
        diff = number - last_number
        if last_diff != 0:
            if last_diff > 0 and diff < 0:
                return False
            if last_diff < 0 and diff > 0:
                return False
        if abs(diff) < 1 or abs(diff) > 3:
            return False

        last_number = number
        last_diff = diff

    return True


if __name__ == '__main__':
    main()
