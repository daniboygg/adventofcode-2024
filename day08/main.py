from __future__ import annotations
import itertools
from dataclasses import dataclass


def main():
    with open("input.txt", "r") as f:
        data = f.readlines()

    result = first(data)
    print(f"Result 1: {result}")

    result = second(data)
    print(f"Result 2: {result}")


def first(lines: list[str]):
    antennas = {}
    grid = []
    for row in range(len(lines)):
        grid.append([])
        for col in range(len(lines[row].strip())):
            grid[row].append(lines[row][col])
            if lines[row][col] != ".":
                frequency = lines[row][col]
                antennas.setdefault(frequency, []).append(
                    Antenna(Pos(row, col), frequency),
                )

    antinodes = set()
    for frequency, antennas in antennas.items():
        for a0, a1 in itertools.combinations(antennas, 2):  # type: Antenna, Antenna
            points = get_antinodes(a0, a1, grid)
            for point in points:
                grid[point.row][point.col] = "#"
                antinodes.add(point)

    # print_grid(grid)

    return len(antinodes)


def get_antinodes(a0: Antenna, a1: Antenna, grid) -> list[Pos]:
    dy = a0.pos.row - a1.pos.row
    dx = a0.pos.col - a1.pos.col

    line_points = []

    pos = Pos(a0.pos.row + dy, a0.pos.col + dx)
    while pos.is_valid_in(grid):
        da0y = abs(a0.pos.row - pos.row)
        da0x = abs(a0.pos.col - pos.col)
        da1y = abs(a1.pos.row - pos.row)
        da1x = abs(a1.pos.col - pos.col)
        if (
                (da0y == 2 * da1y or da0y * 2 == da1y)
                and (da0x == 2 * da1x or da0x * 2 == da1x)
        ):
            line_points.append(Pos(pos.row, pos.col))

        pos = Pos(pos.row + dy, pos.col + dx)

    pos = Pos(a1.pos.row, a1.pos.col)
    while pos.is_valid_in(grid):
        da0y = abs(a0.pos.row - pos.row)
        da0x = abs(a0.pos.col - pos.col)
        da1y = abs(a1.pos.row - pos.row)
        da1x = abs(a1.pos.col - pos.col)
        if (
                (da0y == 2 * da1y or da0y * 2 == da1y)
                and (da0x == 2 * da1x or da0x * 2 == da1x)
        ):
            line_points.append(Pos(pos.row, pos.col))

        pos = Pos(pos.row - dy, pos.col - dx)

    return line_points


def second(lines: list[str]):
    antennas = {}
    grid = []
    for row in range(len(lines)):
        grid.append([])
        for col in range(len(lines[row].strip())):
            grid[row].append(lines[row][col])
            if lines[row][col] != ".":
                frequency = lines[row][col]
                antennas.setdefault(frequency, []).append(
                    Antenna(Pos(row, col), frequency),
                )

    antinodes = set()
    for frequency, antennas in antennas.items():
        for a0, a1 in itertools.combinations(antennas, 2):  # type: Antenna, Antenna
            points = get_all_points_in_line(a0, a1, grid)
            for point in points:
                grid[point.row][point.col] = "#"
                antinodes.add(point)

    # print_grid(grid)

    return len(antinodes)


def get_all_points_in_line(a0: Antenna, a1: Antenna, grid) -> list[Pos]:
    dy = a0.pos.row - a1.pos.row
    dx = a0.pos.col - a1.pos.col

    line_points = [a0.pos, a1.pos]

    pos = Pos(a0.pos.row + dy, a0.pos.col + dx)
    while pos.is_valid_in(grid):
        line_points.append(Pos(pos.row, pos.col))
        pos = Pos(pos.row + dy, pos.col + dx)

    pos = Pos(a0.pos.row - dy, a0.pos.col - dx)
    while pos.is_valid_in(grid):
        line_points.append(Pos(pos.row, pos.col))
        pos = Pos(pos.row - dy, pos.col - dx)

    return line_points


@dataclass(frozen=True)
class Pos:
    row: int
    col: int

    def is_valid_in(self, lines: list) -> bool:
        if self.row < 0 or self.row > len(lines) - 1:
            return False
        if self.col < 0 or self.col > len(lines[self.row]) - 1:
            return False
        return True


@dataclass
class Antenna:
    pos: Pos
    frequency: str


def print_grid(grid):
    for line in grid:
        line = " ".join(line)
        print(line)


if __name__ == '__main__':
    main()
