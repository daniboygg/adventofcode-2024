# Advent of code 2024

Implemented in [zig](https://ziglang.org/) 0.13 for https://adventofcode.com/.

As a [Djagno](https://www.djangoproject.com/) developer I will solve the problems in python to understand then first.

On every folder create input.txt with problem data and execute:

* for python: `python main.py`
* for zig: `zig run main.zig`
* compare time executions:
    1. Install https://github.com/sharkdp/hyperfine
    2. compile zig with `zig build-exe main.zig -femit-bin=zig -O ReleaseSafe`
    3. execute `hyperfine "python main.py" "./zig" --export-markdown times.md`

You can generate the structure of a new day with the util script `python create_day <number_of_day>`