"""AoC :: Day 5"""
from dataclasses import dataclass
from pathlib import Path

# Constants
input_path = Path(__file__).parent / 'Day05.in'


@dataclass
class Range:
    start: int
    stop: int

    @classmethod
    def parse(cls, s: str):
        """parse range from a string with format 'x-y'"""
        x, y = s.split("-")
        return cls(start=int(x), stop=int(y))
    
    def check(self, i: int):
        return self.start <= i <= self.stop

def parse(path: Path):
    """Parse the plaintext input"""
    ranges, ingredients = path.read_text().split("\n\n")
    return [Range.parse(r) for r in ranges.strip().splitlines()], [int(i) for i in ingredients.strip().splitlines()]


def part_one(data: list[Range], ids: list[int]):
    """Solution to part one"""
    return sum(1 for i in ids if any(r.check(i) for r in data))


def part_two(data: list[Range]):
    """
    Solution to part two
    """
    sorted_ranges = sorted(data, key=lambda r: r.start)
    end = sorted_ranges[0].start - 1
    total = 0

    for r in sorted_ranges:
        total += max(0, r.stop + 1 - max(r.start, end))
        end = max(end, r.stop+1)

    return total


def main():
    """Run the solutions and print the results"""
    print(__doc__)
    # Parse inputs
    ranges, ingredients = parse(input_path)
    # Part 1
    print(f"Part 1: {part_one(ranges, ingredients)}")
    # Part 2
    print(f"Part 2: {part_two(ranges)}")


if __name__ == '__main__':
    main()
