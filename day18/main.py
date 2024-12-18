from __future__ import annotations

import sys
from collections import deque
from typing import NamedTuple


def main(make_tests):
    if make_tests:
        with open("input_test.txt", "r") as f:
            data = f.readlines()

        result = first(data, 7, 12)
        expected = 22
        assert expected == result, f"Result 1: Expected {expected}, actual {result}"
        result = second(data, 7, 12)
        expected = [6, 1]
        assert expected == result, f"Result 2: Expected {expected}, actual {result}"

    with open("input.txt", "r") as f:
        data = f.readlines()

    result = first(data, 71, 1024)
    print(f"Result 1: {result}")
    result = second(data, 71, 1024)
    print(f"Result 2: {result}")


def first(lines: list[str], size, fall_bytes):
    matrix = [["."] * size for x in range(size)]
    for index, line in enumerate(lines):
        if index >= fall_bytes:
            break
        col, row = map(int, line.split(","))
        matrix[row][col] = "#"

    path = breath_first_search(matrix, size)
    assert path, "A solution should be found"
    return len(path)


def second(lines: list[str], size, fall_bytes):
    matrix = [["."] * size for x in range(size)]
    for index, line in enumerate(lines):
        col, row = map(int, line.split(","))
        matrix[row][col] = "#"

        path = breath_first_search(matrix, size)
        if path is None:
            break

    return [col, row]


def breath_first_search(matrix, size):
    end = Pos(size - 1, size - 1)
    visited = set()
    # path empty do not count start position
    to_visit = deque([(Pos(0, 0), [])])
    while to_visit:
        current, path = to_visit.popleft()
        if current in visited:
            continue
        if current == end:
            return path

        visited.add(current)
        for direction in [UP, RIGHT, DOWN, LEFT]:
            next_p = current.add(direction, matrix)
            if next_p is None or matrix[next_p.row][next_p.col] == "#":
                continue
            if next_p in visited:
                continue
            to_visit.append((next_p, path + [next_p]))
    return None


class Pos(NamedTuple):
    row: int
    col: int

    def add(self, other: Pos, matrix) -> Pos | None:
        new_pos = Pos(self.row + other.row, self.col + other.col)
        if not new_pos.is_valid(matrix):
            return None
        return new_pos

    def is_valid(self, matrix) -> bool:
        if self.row < 0 or self.row > len(matrix) - 1:
            return False
        if self.col < 0 or self.col > len(matrix[self.row]) - 1:
            return False
        return True


UP = Pos(-1, 0)
RIGHT = Pos(0, 1)
DOWN = Pos(1, 0)
LEFT = Pos(0, -1)

if __name__ == '__main__':
    main(make_tests=len(sys.argv) > 1 and sys.argv[1] == "--tests")
