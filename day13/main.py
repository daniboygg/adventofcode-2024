from __future__ import annotations

import sys


def main(make_tests):
    if make_tests:
        with open("input_test.txt", "r") as f:
            data = f.readlines()

        result = first(data)
        expected = 480
        assert expected == result, f"Result 1: Expected {expected}, actual {result}"
        result = second(data)
        expected = 875318608908
        assert expected == result, f"Result 2: Expected {expected}, actual {result}"

    with open("input.txt", "r") as f:
        data = f.readlines()

    result = first(data)
    print(f"Result 1: {result}")
    result = second(data)
    print(f"Result 2: {result}")


def first(lines: list[str]):
    a_token = 3
    b_token = 1

    total = 0

    a1, a2, b1, b2, c1, c2 = None, None, None, None, None, None
    for line in lines:
        line = line.strip()
        if line.startswith("Button A: "):
            a = line[len("Button A: "):]
            a = a.split(", ")
            a1 = int(a[0][len("X+"):])
            a2 = int(a[1][len("Y+"):])
        if line.startswith("Button B: "):
            b = line[len("Button B: "):]
            b = b.split(", ")
            b1 = int(b[0][len("X+"):])
            b2 = int(b[1][len("Y+"):])
        if line.startswith("Prize: "):
            c = line[len("Prize: "):]
            c = c.split(", ")
            c1 = int(c[0][len("X="):])
            c2 = int(c[1][len("Y="):])

            # https://en.wikipedia.org/wiki/Cramer%27s_rule
            x = (
                    (c1 * b2 - b1 * c2)
                    / (a1 * b2 - b1 * a2)
            )
            y = (
                    (a1 * c2 - c1 * a2)
                    / (a1 * b2 - b1 * a2)
            )

            if x.is_integer() and y.is_integer() and x <= 100 and y <= 100:
                total += x * a_token + y * b_token
                # print(f"{c} x: {x} y: {y}")

    return int(total)


def second(lines: list[str]):
    a_token = 3
    b_token = 1

    total = 0

    a1, a2, b1, b2, c1, c2 = None, None, None, None, None, None
    for line in lines:
        line = line.strip()
        if line.startswith("Button A: "):
            a = line[len("Button A: "):]
            a = a.split(", ")
            a1 = int(a[0][len("X+"):])
            a2 = int(a[1][len("Y+"):])
        if line.startswith("Button B: "):
            b = line[len("Button B: "):]
            b = b.split(", ")
            b1 = int(b[0][len("X+"):])
            b2 = int(b[1][len("Y+"):])
        if line.startswith("Prize: "):
            c = line[len("Prize: "):]
            c = c.split(", ")
            c1 = 10000000000000 + int(c[0][len("X="):])
            c2 = 10000000000000 + int(c[1][len("Y="):])

            # https://en.wikipedia.org/wiki/Cramer%27s_rule
            x = (
                    (c1 * b2 - b1 * c2)
                    / (a1 * b2 - b1 * a2)
            )
            y = (
                    (a1 * c2 - c1 * a2)
                    / (a1 * b2 - b1 * a2)
            )

            if x.is_integer() and y.is_integer():
                total += x * a_token + y * b_token
                # print(f"{c} x: {x} y: {y}")

    return int(total)


if __name__ == '__main__':
    main(make_tests=len(sys.argv) > 1 and sys.argv[1] == "--tests")
