from __future__ import annotations

import sys
from typing import NamedTuple


def main(make_tests):
    if make_tests:
        with open("input_test.txt", "r") as f:
            data = f.readlines()

        result = first(data)
        assert result == 36, f"Expected 36, actual {result}"
        result = second(data)
        assert result == 1, f"Expected 1, actual {result}"

    with open("input.txt", "r") as f:
        data = f.readlines()

    result = first(data)
    print(f"Result 1: {result}")
    result = second(data)
    print(f"Result 2: {result}")


def first(lines: list[str]):
    grid: list[list[int]] = []
    zeros: list[Pos] = []
    for row, line in enumerate(lines):
        grid.append([])
        for col, value in enumerate(line.strip()):
            grid[row].append(int(value))
            if value == "0":
                zeros.append(Pos(row, col))

    total = 0
    for zero in zeros:
        paths = walk(zero, grid)
        total += len(paths)

    return total


def walk(start, grid):
    to_visit = [start]
    visited = set()

    paths = []
    current_path = []
    while to_visit:
        current = to_visit.pop(0)
        if current in current_path or current in visited:
            continue
        visited.add(current)
        current_path.append(current)
        value = grid[current.row][current.col]
        old_size = len(to_visit)
        if n := current.go_to_next_hiking_step(UP, grid, value):
            to_visit.insert(0, n)
        if n := current.go_to_next_hiking_step(DOWN, grid, value):
            to_visit.insert(0, n)
        if n := current.go_to_next_hiking_step(RIGHT, grid, value):
            to_visit.insert(0, n)
        if n := current.go_to_next_hiking_step(LEFT, grid, value):
            to_visit.insert(0, n)
        if len(to_visit) == old_size:
            if grid[current_path[-1].row][current_path[-1].col] == 9:
                if current_path not in paths:
                    paths.append(current_path)

            # go back to the last branch
            if old_size > 0:
                new_path = []
                next_to_visite = to_visit[0]
                for p in current_path:
                    if grid[p.row][p.col] == grid[next_to_visite.row][next_to_visite.col]:
                        break
                    new_path.append(p)

                current_path = new_path

    if grid[current_path[-1].row][current_path[-1].col] == 9:
        if current_path not in paths:
            paths.append(current_path)

    return paths


def print_grid(grid, path=None):
    for row, line in enumerate(grid):
        for col, c in enumerate(line):
            if path and Pos(row, col) in path:
                print(f" {c}*", end="")
            else:
                print(f" {c} ", end="")
        print()


def second(lines: list[str]):
    return 0


class Direction(NamedTuple):
    pos: Pos
    direction: Pos


class Pos(NamedTuple):
    row: int
    col: int

    def go_to_next_hiking_step(self, direction: Pos, grid, last) -> Pos | None:
        new_pos = self.add(direction, grid)
        if new_pos is None:
            return None
        if grid[new_pos.row][new_pos.col] - last != 1:
            return None
        return new_pos

    def add(self, direction: Pos, grid) -> Pos | None:
        new_pos = Pos(self.row + direction.row, self.col + direction.col)
        if new_pos.row < 0 or new_pos.row > len(grid) - 1:
            return None
        if new_pos.col < 0 or new_pos.col > len(grid[new_pos.row]) - 1:
            return None
        return new_pos


UP = Pos(-1, 0)
RIGHT = Pos(0, 1)
DOWN = Pos(1, 0)
LEFT = Pos(0, -1)

if __name__ == '__main__':
    main(make_tests=len(sys.argv) > 1 and sys.argv[1] == "--tests")
