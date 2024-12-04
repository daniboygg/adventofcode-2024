def main():
    with open("input.txt", "r") as f:
        data = f.readlines()

    data = [l.strip() for l in data]

    result = first(data)
    print(f"Result 1: {result}")

    result = second(data)
    print(f"Result 2: {result}")


def first(lines: list[str]):
    count = 0
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == "X":
                words = diagonal_words(lines, i, j)
                count += len(words)
    return count


def diagonal_words(lines: [str], i: int, j: int) -> list[str]:
    word_size = 4
    found_words = [lines[i][j] for _ in range(8)]
    for d in range(1, word_size):
        # right
        next_col = j + d
        if next_col < len(lines[i]):
            found_words[0] += lines[i][next_col]

        # down
        new_row = i + d
        if new_row < len(lines):
            found_words[1] += lines[new_row][j]

        # left
        next_col = j - d
        if next_col >= 0:
            found_words[2] += lines[i][next_col]

        # up
        new_row = i - d
        if new_row >= 0:
            found_words[3] += lines[new_row][j]

        # down_right
        next_row = i + d
        next_col = j + d
        if next_row < len(lines) and next_col < len(lines[next_row]):
            found_words[4] += lines[next_row][next_col]

        # up right
        next_row = i - d
        next_col = j + d
        if next_row >= 0 and next_col < len(lines[next_row]):
            found_words[5] += lines[next_row][next_col]

        # down left
        next_row = i + d
        next_col = j - d
        if next_row < len(lines) and next_col >= 0:
            found_words[6] += lines[next_row][next_col]

        # up left
        next_row = i - d
        next_col = j - d
        if next_row >= 0 and next_col >= 0:
            found_words[7] += lines[next_row][next_col]

    words = [f for f in found_words if f == "XMAS"]
    return words


def second(lines: list[str]):
    count = 0
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == "A" and 0 < i < len(lines) - 1 and 0 < j < len(line) - 1:
                if is_diagonal_cross(lines, i, j):
                    count += 1

    return count


def is_diagonal_cross(lines: [str], i: int, j: int) -> bool:
    crosses = [
        [
            ['M', ".", "S"],
            [".", "A", "."],
            ['M', ".", "S"],
        ],
        [
            ['M', ".", "M"],
            [".", "A", "."],
            ['S', ".", "S"],
        ],
        [
            ['S', ".", "M"],
            [".", "A", "."],
            ['S', ".", "M"],
        ],
        [
            ['S', ".", "S"],
            [".", "A", "."],
            ['M', ".", "M"],
        ],
    ]
    for cross in crosses:
        if (
                lines[i - 1][j - 1] == cross[0][0]
                and lines[i - 1][j + 1] == cross[0][2]
                and lines[i + 1][j - 1] == cross[2][0]
                and lines[i + 1][j + 1] == cross[2][2]
        ):
            return True
    return False


if __name__ == '__main__':
    main()
