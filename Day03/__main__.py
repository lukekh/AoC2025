"""AoC :: Day 3"""
from pathlib import Path
from typing import Sequence

# Input path
input_path = Path(__file__).parent / 'Day03.in'


def parse(path: Path):
    """Parse the plaintext input"""
    return [list(map(int, line)) for line in path.read_text().strip().splitlines()]


def indexed_max(numbers: Sequence[int]) -> tuple[int, int]:
    """Return the (index, value) pair of the left-most maximal element in a sequence"""
    return max(enumerate(numbers), key=lambda x: x[1])


def solve(line: list[int], digits: int):
    """Solve the problem for a single line"""
    def recursive_solve(line: list[int], digits: int, cum_str: str = ""):
        """Use recursion to simplify logic"""
        # Base case
        if digits < 1:
            return cum_str
        # Else proceed with recursion
        j, M = indexed_max(line[:len(line)-digits+1])
        return recursive_solve(line[j+1:], digits-1, cum_str+str(M))
    
    return int(recursive_solve(line, digits))


def part_one(data: list[list[int]]):
    """Solution to part one"""
    return sum(solve(line, 2) for line in data)


def part_two(data: list[list[int]], digits: int = 12):
    """Solution to part two"""
    return sum(solve(line, digits) for line in data)


def main():
    """Run the solutions and print the results"""
    print(__doc__)
    # Parse inputs
    data = parse(input_path)
    # Part 1
    print(f"Part 1: {part_one(data)}")
    # Part 2
    print(f"Part 2: {part_two(data)}")


if __name__ == '__main__':
    main()
