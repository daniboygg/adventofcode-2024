from __future__ import annotations

import sys
from dataclasses import dataclass, field
from multiprocessing import Pool


def main(make_tests):
    if make_tests:
        with open("input_test.txt", "r") as f:
            data = f.readlines()

        result = first(data)
        expected = "4,6,3,5,6,3,5,2,1,0"
        assert expected == result, f"Result 1: Expected {expected}, actual {result}"
        result = second(data, True)
        expected = 117440
        assert expected == result, f"Result 2: Expected {expected}, actual {result}"

    with open("input.txt", "r") as f:
        data = f.readlines()

    result = first(data)
    print(f"Result 1: {result}")
    result = second(data)
    print(f"Result 2: {result}")


def first(lines: list[str]):
    program = Program()
    for line in lines:
        if line.startswith("Register A: "):
            program.register_a = int(line.split("Register A: ")[1])
        if line.startswith("Register B: "):
            program.register_b = int(line.split("Register B: ")[1])
        if line.startswith("Register C: "):
            program.register_c = int(line.split("Register C: ")[1])
        if line.startswith("Program: "):
            program.instructions = list(map(int, line.split("Program: ")[1].split(",")))

    output = program.run()
    return ",".join(output)


def second(lines: list[str], is_test=False):
    if is_test:
        lines = """Register A: 2024
        Register B: 0
        Register C: 0
        
        Program: 0,3,5,4,3,0
        """
        lines = lines.split("\n")
    program = Program()
    for line in lines:
        line = line.strip()
        if line.startswith("Register A: "):
            program.register_a = int(line.split("Register A: ")[1])
        if line.startswith("Register B: "):
            program.register_b = int(line.split("Register B: ")[1])
        if line.startswith("Register C: "):
            program.register_c = int(line.split("Register C: ")[1])
        if line.startswith("Program: "):
            program.instructions = list(map(int, line.split("Program: ")[1].split(",")))

    step = 1_000_000
    start = 0
    if not is_test:
        # the last brute-force iteration stopped at 124_000_000 and nothing found
        start = 124_000_000

    start, end = start, start + step
    register_a = None

    # brute force solution with python parallel multiprocess
    while register_a is None:
        splitter = RangeSplitter(start, end)
        if not is_test:
            print(f"Find value in range: {splitter}")
        ranges = splitter.split()
        args = [(x, program) for x in ranges]
        with Pool(8) as pool:
            for result in pool.imap(find_register, args):
                if result is not None:
                    pool.terminate()
                    register_a = result
                    break
            else:
                register_a = None

        if register_a:
            break
        start, end = end, end + step

    assert register_a is not None
    return register_a


def find_register(args):
    register_as, program = args
    for register_a in register_as:
        program = Program(register_a=register_a, instructions=program.instructions)
        output = list(map(int, program.run()))
        if output == program.instructions:
            return register_a
    return None


@dataclass
class RangeSplitter:
    start: int
    end: int

    def __str__(self):
        return f"{self.start:_}-{self.end:_}"

    def split(self):
        ranges = []
        for i in range(self.start, self.end, 100_000):
            ranges.append(range(i, i + 100_000))
        return ranges


@dataclass
class Program:
    register_a: int = 0
    register_b: int = 0
    register_c: int = 0
    instruction_pointer: int = 0
    instructions: list = field(default_factory=list)
    output: list = field(default_factory=list)

    def run(self):
        while self.instruction_pointer < len(self.instructions):
            instruction = self.instructions[self.instruction_pointer]
            operand = self.instructions[self.instruction_pointer + 1]
            # print(f"instruction {instruction}({operand}) ip {self.instruction_pointer}")
            self.exec_instruction(instruction, operand)

        return self.output

    def exec_instruction(self, instruction: int, operand: int):
        match instruction:
            case 0:  # adv
                operand = self.combo_operand(operand)
                self.register_a = self.register_a // 2 ** operand
            case 1:  # bxl
                operand = self.literal_operand(operand)
                self.register_b = self.register_b ^ operand
            case 2:  # bst
                operand = self.combo_operand(operand)
                self.register_b = operand % 8
            case 3:  # jnz
                if self.register_a == 0:
                    self.instruction_pointer += 2
                else:
                    operand = self.literal_operand(operand)
                    self.instruction_pointer = operand
            case 4:  # bxc
                # ignores operand
                self.register_b = self.register_b ^ self.register_c
            case 5:  # out
                operand = self.combo_operand(operand)
                self.output.append(str(operand % 8))
            case 6:  # bvd
                operand = self.combo_operand(operand)
                self.register_b = self.register_a // 2 ** operand
            case 7:  # cdv
                operand = self.combo_operand(operand)
                self.register_c = self.register_a // 2 ** operand
            case error:
                assert False, f"Operand {error} is not valid"

        if instruction != 3:
            self.instruction_pointer += 2

    def combo_operand(self, operand):
        match operand:
            case 0 | 1 | 2 | 3:
                return operand
            case 4:
                return self.register_a
            case 5:
                return self.register_b
            case 6:
                return self.register_c
            case error:
                assert False, f"Operand {error} is not valid"

    def literal_operand(self, operand):
        return operand


if __name__ == '__main__':
    main(make_tests=len(sys.argv) > 1 and sys.argv[1] == "--tests")
