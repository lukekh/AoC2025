"""AoC :: Day 6"""
from dataclasses import dataclass
import math
from pathlib import Path
import re
from typing import Literal, Self

# Constants
input_path = Path(__file__).parent / 'Day06.in'

@dataclass
class Problem:
    numbers: list[int]
    operation: Literal["*", "+"]

    @classmethod
    def parse(cls, ns: list[str], op: str) -> Self:
        """Convert a list of string ints and an operation into a Problem"""
        match op:
            case "*":
                return cls(list(map(int, ns)), "*")
            case "+":
                return cls(list(map(int, ns)), "+")
            case _:
                raise ValueError(f"op should be one of '+' or '*', got {op}")

    def solve(self):
        """solve problem given op"""
        match self.operation:
            case "*":
                return math.prod(self.numbers)
            case "+":
                return sum(self.numbers)


def parse(path: Path):
    """Parse the plaintext input"""
    # specify pattern
    re_whitespace = re.compile(r"\s+")
    lines = [re_whitespace.split(line.strip()) for line in path.read_text().strip().splitlines()]
    return [Problem.parse(ns, op) for *ns, op in zip(*lines)]


def part_one(data: list[Problem]):
    """Solution to part one"""
    return sum(p.solve() for p in data)


def parse_differently(path: Path):
    """Parse the plaintext input ... differently"""
    *number_lines, op_line = path.read_text().splitlines()
    # Find the */+ indices in the string
    re_op = re.compile(r"\+\s+|\*\s+")
    op_matches = re_op.finditer(op_line)

    def construct_from_match(op_match: re.Match):
        """use the op_match to construct the number square"""
        start, stop = op_match.span()
        return [n for i in range(start, stop) if (n := ("".join(number_line[i] for number_line in number_lines)).strip())]

    # Parse the numbers accordingly
    return [Problem.parse(construct_from_match(op_match), op_match.group(0).strip()) for op_match in op_matches]


def part_two(path: Path):
    """Solution to part two"""
    # We need to parse it again
    data = parse_differently(path)
    # Then do part one again
    return part_one(data)


def main():
    """Run the solutions and print the results"""
    print(__doc__)
    # Parse inputs
    data = parse(input_path)
    # Part 1
    print(f"Part 1: {part_one(data)}")
    # Part 2
    print(f"Part 2: {part_two(input_path)}")


if __name__ == '__main__':
    main()
