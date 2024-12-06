import os
from collections import namedtuple
from dataclasses import dataclass
from time import sleep


def main():
    with open("input.txt", "r") as f:
        data = f.readlines()

    result = first(data)
    print(f"Result 1: {result}")

    result = second(data)
    print(f"Result 2: {result}")


def first(lines: list[str]):
    grid = []
    guard = Guard(Pos(0, 0), UP)
    for row, line in enumerate(lines):
        grid.append([])
        for col, c in enumerate(line.strip()):
            grid[row].append(c)
            if c == "^":
                guard.position = Pos(row, col)

    next_position = guard.peek(grid)
    visited = {guard.position}
    while next_position != "":
        if next_position == "#":
            guard.turn_right()
        else:
            guard.advance()
            visited.add(guard.position)

        next_position = guard.peek(grid)
        # display(grid, guard, visited)

    return len(visited)


def second(lines: list[str]):
    grid = []
    start_position = Pos(0, 0)
    total = 0
    for row, line in enumerate(lines):
        grid.append([])
        for col, c in enumerate(line.strip()):
            grid[row].append(c)
            total += 1
            if c == "^":
                start_position = Pos(row, col)

    loop_possibilities = 0
    tries = 0
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] != ".":
                continue

            guard = Guard(start_position, UP)
            grid[row][col] = "#"
            if has_loop(grid, guard, show_display=False):
                loop_possibilities += 1
            grid[row][col] = "."

            # os.system('clear')
            # print(f"{tries} / {total} ")
            # tries += 1

    return loop_possibilities


def has_loop(grid, guard, show_display) -> bool:
    next_position = guard.peek(grid)
    visited = {guard.position}
    loop_detector = 0
    while next_position != "":
        if loop_detector >= len(visited):
            return True

        if next_position == "#":
            guard.turn_right()
        else:
            guard.advance()
            if guard.position in visited:
                loop_detector += 1
            else:
                visited.add(guard.position)
                loop_detector = 0

        next_position = guard.peek(grid)
        if show_display:
            display(grid, guard, visited)

    return False


def display(grid: list[list[str]], guard, visited):
    os.system('clear')
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if Pos(row, col) in visited:
                print(f" X ", end="")
            else:
                print(f" {grid[row][col]} ", end="")

        print()
    sleep(.05)


Pos = namedtuple('Pos', 'row col')

UP = Pos(-1, 0)
RIGHT = Pos(0, 1)
DOWN = Pos(1, 0)
LEFT = Pos(0, -1)


@dataclass
class Guard:
    position: Pos
    direction: Pos

    def advance(self):
        self.position = Pos(self.position.row + self.direction.row, self.position.col + self.direction.col)

    def turn_right(self):
        if self.direction == UP:
            self.direction = RIGHT
        elif self.direction == RIGHT:
            self.direction = DOWN
        elif self.direction == DOWN:
            self.direction = LEFT
        elif self.direction == LEFT:
            self.direction = UP

    def peek(self, grid) -> str:
        new_pos = Pos(self.position.row + self.direction.row, self.position.col + self.direction.col)
        if new_pos.row >= len(grid) or new_pos.row < 0:
            return ""
        if new_pos.col >= len(grid[new_pos.row]) or new_pos.col < 0:
            return ""
        return grid[new_pos.row][new_pos.col]


if __name__ == '__main__':
    main()
