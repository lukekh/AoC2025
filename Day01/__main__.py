"""AoC :: Day 1"""
from pathlib import Path

input_path = Path(__file__).parent / 'Day01.in'

def parse(path: Path):
    """Parse the plaintext input"""
    instructions = path.read_text().replace("R", "").replace("L", "-").strip().splitlines()
    return [int(instruction) for instruction in instructions]


def part_one(data: list[int], start: int = 50, dial_max: int = 100):
    """Solve part one of Day 1"""
    ctr = 0
    for instruction in data:
        start = (start + instruction) % dial_max
        ctr += (start == 0)
    return ctr


def part_two(data: list[int], start: int = 50, dial_max: int = 100):
    """Solve part two of Day 1"""
    ctr = 0
    for instruction in data:
        ctr += abs((start + instruction) // dial_max)
        start = (start + instruction) % dial_max
    return ctr


def main():
    """Run the solutions for Day 1 and print the results"""
    # Parse inputs
    data = parse(input_path)
    # Part 1
    print(f"Part 1: {part_one(data)}")
    # Part 2
    print(f"Part 2: {part_two(data)}")


if __name__ == '__main__':
    main()
