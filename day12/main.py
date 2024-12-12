from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import NamedTuple


def main(make_tests):
    if make_tests:
        with open("input_test.txt", "r") as f:
            data = f.readlines()

        result = first(data)
        expected = 1930
        assert expected == result, f"Result 1: Expected {expected}, actual {result}"
        result = second(data)
        expected = 1206
        assert expected == result, f"Result 2: Expected {expected}, actual {result}"

    with open("input.txt", "r") as f:
        data = f.readlines()

    result = first(data)
    print(f"Result 1: {result}")
    result = second(data)
    print(f"Result 2: {result}")


def first(lines: list[str]):
    matrix = []
    rows = len(lines)
    for line in lines:
        matrix.append([])
        for c in line.strip():
            matrix[-1].append(c)
        assert len(matrix[-1]) == rows, "Matrix is not a square"
    matrix_size = len(matrix)

    already_in_region = set()
    price = 0
    for row in range(matrix_size):
        for col in range(matrix_size):
            point = Pos(row, col)
            if point in already_in_region:
                continue

            r = expand_point_to_region(point, matrix)
            already_in_region.update(r.positions)
            price += len(r.positions) * r.perimeter(matrix)
    return price


def second(lines: list[str]):
    matrix = []
    rows = len(lines)
    for line in lines:
        matrix.append([])
        for c in line.strip():
            matrix[-1].append(c)
        assert len(matrix[-1]) == rows, "Matrix is not a square"
    matrix_size = len(matrix)

    already_in_region = set()
    price = 0
    for row in range(matrix_size):
        for col in range(matrix_size):
            point = Pos(row, col)
            if point in already_in_region:
                continue

            r = expand_point_to_region(point, matrix)
            already_in_region.update(r.positions)
            price += len(r.positions) * r.sides(matrix)
    return price


def expand_point_to_region(p, matrix) -> Region:
    plant = matrix[p.row][p.col]
    positions = set()
    explore = set()
    explore.add(p)
    while explore:
        item = explore.pop()
        if matrix[item.row][item.col] == plant:
            positions.add(item)

        for direction in [UP, RIGHT, DOWN, LEFT]:
            p = item.add(direction, matrix)
            if p is None or p in positions or matrix[p.row][p.col] != plant:
                continue
            explore.add(p)

    return Region(plant, positions)


@dataclass
class Region:
    plant: str
    positions: set[Pos]

    def __str__(self):
        return f"Plant {self.plant} -> region {self.positions}"

    def has_position(self, position):
        return position in self.positions

    def perimeter(self, matrix) -> int:
        total_fences = 0
        for p in self.positions:
            fences = 4
            for direction in [UP, RIGHT, DOWN, LEFT]:
                adjacent = p.add(direction, matrix)
                if adjacent in self.positions:
                    fences -= 1
            total_fences += fences
        return total_fences

    def sides(self, matrix) -> int:
        # TODO
        return 0


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

    def opposite_direction(self) -> Pos:
        if self == UP:
            return DOWN
        if self == RIGHT:
            return LEFT
        if self == DOWN:
            return UP
        if self == LEFT:
            return RIGHT


UP = Pos(-1, 0)
RIGHT = Pos(0, 1)
DOWN = Pos(1, 0)
LEFT = Pos(0, -1)

if __name__ == '__main__':
    main(make_tests=len(sys.argv) > 1 and sys.argv[1] == "--tests")
