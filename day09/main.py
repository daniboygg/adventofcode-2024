import sys


def main(make_tests):
    if make_tests:
        with open("input_test.txt", "r") as f:
            data = f.readlines()

        result = first(data)
        assert result == 1928, f"Expected 1928, actual {result}"
        result = second(data)
        assert result == 2858, f"Expected 2858, actual {result}"

    with open("input.txt", "r") as f:
        data = f.readlines()

    result = first(data)
    print(f"Result 1: {result}")
    result = second(data)
    print(f"Result 2: {result}")


def first(lines: list[str]):
    line = lines[0].strip()

    file_id = 0
    disk_map = []

    for index, value in enumerate(line):
        if index % 2 == 0:
            for _ in range(int(value)):
                disk_map.append(str(file_id))
            file_id += 1
        else:
            for _ in range(int(value)):
                disk_map.append(".")

    wholes = []
    for index, value in enumerate(disk_map):
        if value == ".":
            wholes.append(index)

    for index, value in enumerate(reversed(disk_map)):
        if len(wholes) == 0:
            break

        real_index = len(disk_map) - 1 - index
        if disk_map[real_index] == ".":
            continue

        i = wholes.pop(0)
        if i > real_index:
            wholes.clear()
            break

        disk_map[i] = disk_map[real_index]
        disk_map[real_index] = "."

    total = 0
    for index, value in enumerate(disk_map):
        if value == ".":
            break
        total += index * int(value)

    return total


def is_valid(disk_map):
    leftmost_space = disk_map.index(".")
    for i in disk_map[leftmost_space:]:
        if i != ".":
            return False
    return True


def second(lines: list[str]):
    line = lines[0].strip()

    file_id = 0
    disk_map = []

    for index, value in enumerate(line):
        if index % 2 == 0:
            for _ in range(int(value)):
                disk_map.append(str(file_id))
            file_id += 1
        else:
            for _ in range(int(value)):
                disk_map.append(".")

    wholes = {}
    last_whole_index = None
    numbers = {}
    last_number_index = None
    last_number_value = None
    for index, value in enumerate(disk_map):
        if value == ".":
            if last_whole_index:
                wholes[last_whole_index] += 1
            else:
                last_whole_index = index
                wholes[last_whole_index] = 1

            last_number_index = None
            last_number_value = None
        else:
            if last_number_index:
                if last_number_value == value:
                    numbers[last_number_index] += 1
                else:
                    last_number_index = index
                    last_number_value = value
                    numbers[last_number_index] = 1
            else:
                last_number_index = index
                last_number_value = value
                numbers[last_number_index] = 1

            last_whole_index = None

    number_indexes = sorted(numbers.keys(), reverse=True)
    for i_number in number_indexes:
        for i_whole in sorted(wholes.keys()):
            if i_number < i_whole:
                break

            whole_size = wholes[i_whole]
            number_size = numbers[i_number]
            if whole_size >= number_size:
                for j in range(i_number, i_number + number_size):
                    disk_map[i_whole + j - i_number] = disk_map[j]
                    disk_map[j] = "."

                new_size = whole_size - number_size
                if new_size > 0:
                    wholes[i_whole + number_size] = new_size
                del wholes[i_whole]
                break

    total = 0
    for index, value in enumerate(disk_map):
        if value == ".":
            continue
        total += index * int(value)

    return total


def print_disk_map(value):
    print("".join(value))


if __name__ == '__main__':
    main(make_tests=len(sys.argv) > 1 and sys.argv[1] == "--tests")
