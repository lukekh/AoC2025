"""AoC :: Day 2"""
from dataclasses import dataclass
from pathlib import Path


input_path = Path(__file__).parent / 'Day02.in'


@dataclass
class Range:
    start: int
    stop: int

    @classmethod
    def parse(cls, s: str):
        """parse a Range from a string with format 'n-m'"""
        return cls(*map(int, s.split("-")))
    
    def valid(self, n: int):
        """test if n lies within the range"""
        return self.start <= n <= self.stop


def parse(path: Path):
    """Parse the plaintext input"""
    return [Range.parse(r) for r in path.read_text().strip().split(",")]


def part_one(data: list[Range], d: int = 2):
    """Solution to part one"""
    # Max value in ranges
    Ms = [str(r.stop) for r in data]
    m = max(int(M[:len(M)//d]) for M in Ms)

    s = {n for i in range(1, m+1) if (n := int(str(i)*d)) and any([r.valid(n) for r in data])}
    return sum(s)


def part_two(data: list[Range]):
    """Solution to part two"""
    # init set of numbers
    s = set()

    # Max value in ranges
    Ms = [str(r.stop) for r in data]

    for d in range(2, max(len(M) for M in Ms)):
        m = max(int(M[:len(M)//d]) for M in Ms if len(M)//d)
        s |= {n for i in range(1, m+1) if (n := int(str(i)*d)) and any([r.valid(n) for r in data])}

    return sum(s)
    

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
