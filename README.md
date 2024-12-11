# Advent of code 2024

Implemented in [zig](https://ziglang.org/) 0.13 for https://adventofcode.com/.

As a [Django](https://www.djangoproject.com/) developer I will solve the problems in python to understand then first.

On every folder create input.txt (real problem data) and input_test.txt (example problem data) with problem data
and execute:

* for python: `python main.py`
* for zig: `zig run main.zig`
* compare time executions:
    1. Install https://github.com/sharkdp/hyperfine
    2. compile zig with `zig build-exe main.zig -femit-bin=zig -O ReleaseSafe`
    3. execute `hyperfine "./zig" "python main.py" --export-markdown times.md`

You can generate the structure of a new day with the util script `python create_day <number_of_day>`

## test

For quick iteration on changing the problem definition (because I'm stuck, or I want to improve performance) you can
run the problem with `--tests` like `python main.py --tests`. This will assert that given input_test.txt data the
results are correct.