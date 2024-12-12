import sys


def main(make_tests):
    if make_tests:
        with open("input_test.txt", "r") as f:
            data = f.readlines()

        result = first(data)
        expected = 55312
        assert expected == result, f"Result 1: Expected {expected} actual {result}"

    with open("input.txt", "r") as f:
        data = f.readlines()

    result = first(data)
    print(f"Result 1: {result}")
    result = second(data)
    print(f"Result 2: {result}")


def first(lines: list[str]):
    line = lines[0].strip()
    stones = list(map(int, line.split(" ")))
    stones = {stone: 1 for stone in stones}
    return blink(stones, 25)


def second(lines: list[str]):
    line = lines[0].strip()
    stones = list(map(int, line.split(" ")))
    stones = {stone: 1 for stone in stones}
    return blink(stones, 75)


def blink(stones, times):
    """cache.get(number, 0) because the same number could get produced by different stones"""
    for i in range(times):
        cache = {}
        for stone, quantity in stones.items():
            if stone == 0:
                cache[1] = cache.get(1, 0) + quantity
                continue

            str_stone = str(stone)
            stone_len = len(str_stone)
            if stone_len % 2 == 0:
                left = int(str_stone[stone_len // 2:])
                right = int(str_stone[:stone_len // 2])
                cache[left] = cache.get(left, 0) + quantity
                cache[right] = cache.get(right, 0) + quantity
            else:
                cache[stone * 2024] = cache.get(stone * 2024, 0) + quantity
        stones = cache
    return sum(stones.values())


if __name__ == '__main__':
    main(make_tests=len(sys.argv) > 1 and sys.argv[1] == "--tests")
