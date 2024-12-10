import collections
import sys


def main(make_tests):
    if make_tests:
        with open("input_test.txt", "r") as f:
            data = f.readlines()

        result = first(data)
        assert result == 1928, f"Expected 1, actual {result}"
        result = first(data)
        assert result == 2858, f"Expected 1, actual {result}"

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
    whole_detector_index = None
    for index, value in enumerate(disk_map):
        if value != ".":
            whole_detector_index = None
            continue

        if whole_detector_index:
            wholes[whole_detector_index] += 1
        else:
            whole_detector_index = index
            wholes[whole_detector_index] = 1

    Last = collections.namedtuple("Last", "value first_index")
    last_number: Last | None = None
    disk_map_reversed = list(reversed(disk_map))
    for index, value in enumerate(disk_map_reversed):
        if last_number:
            if value == last_number.value:
                continue
            else:
                if len(wholes) == 0:
                    break
                file_size = index - last_number.first_index
                assert file_size > 0
                for i in sorted(wholes.keys()):
                    size = wholes[i]
                    if size >= file_size:
                        for j in range(i, i + file_size):
                            disk_map[j] = last_number.value

                        new_size = wholes[i] - file_size
                        if new_size > 0:
                            wholes[i + file_size] = new_size
                        del wholes[i]

                        for j in range(len(disk_map) - index, len(disk_map) - last_number.first_index):
                            disk_map[j] = "."
                        # print_disk_map(disk_map)
                        break
                if value != ".":
                    last_number = Last(value, index)
                else:
                    last_number = None
        elif value != ".":
            last_number = Last(value, index)

    total = 0
    for index, value in enumerate(disk_map):
        if value == ".":
            continue
        total += index * int(value)

    return total


def print_disk_map(value):
    print("".join(value))


if __name__ == '__main__':
    main(make_tests=len(sys.argv) > 1 and sys.argv == "--tests")
