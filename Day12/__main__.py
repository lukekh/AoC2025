"""
AoC :: Day 12

After seeing that the maximum  present/grid ratio was < 0.75 for all feasible regions, I took a punt
on part 1 being trivial after testing for feasibility.
"""
from dataclasses import dataclass
import numpy as np
from pathlib import Path

# Constants
input_path = Path(__file__).parent / 'Day12.in'

@dataclass
class Placement:
    shape: np.ndarray
    position: tuple[int, int]

@dataclass
class Region:
    width: int
    length: int
    requirements: tuple[int, ...]

    @classmethod
    def parse(cls, s: str):
        shape, req = s.split(":")
        width, length = map(int, shape.split("x"))
        requirements = tuple(map(int, req.strip().split(" ")))
        return cls(width, length, requirements)
    
    def feasible(self, shapes: list[np.ndarray]) -> bool:
        """returns True if the total area can accommodate the total area of the shapes"""
        return np.dot(self.requirements, [shape.sum() for shape in shapes]) < (self.width * self.length)
    
    def pct(self, shapes: list[np.ndarray]) -> float:
        """returns True if the total area can accommodate the total area of the shapes"""
        return float(np.dot(self.requirements, [shape.sum() for shape in shapes]) / (self.width * self.length))


class Grid:
    def __init__(self, shape: tuple[int, int], shapes: list[np.ndarray], requirements: list[int]):
        self.grid = np.zeros(shape).astype(bool)
        self.pieces = [shape for i, requirement in enumerate(requirements) for shape in [shapes[i],]*requirement]
        self.placements: list[Placement] = []
    
    def next_pos(self, j):
        pass
    
    def solve(self):
        """
        returns true if a solution exists
        
        use dfs with backtracking to see if a solution exists
        """
        for piece in self.pieces:
            pass


def array_from_shape_string(s: str) -> np.ndarray:
    """Convert a shape string into a numpy array"""
    return np.array([
            [(True if char == "#" else False) for char in line] for line in s.strip().splitlines()
    ])

def parse(path: Path):
    """Parse the plaintext input"""
    raw_input = path.read_text()
    *raw_presents, raw_region = raw_input.split("\n\n")
    shapes = [
        array_from_shape_string(shape) for shape in [
            present.strip().split(":", maxsplit=1)[1].strip() for present in raw_presents
        ]
    ]
    return shapes, list(map(Region.parse, raw_region.strip().splitlines()))


def part_one(shapes: list[np.ndarray], regions: list[Region]):
    """Solution to part one"""
    return int(sum(region.feasible(shapes) for region in regions)), max([region.pct(shapes) for region in regions if region.feasible(shapes)])


def part_two():
    """Solution to part two"""
    return "SMASH THAT MFING DECORATE BUTTON"


def main():
    """Run the solutions and print the results"""
    print(__doc__)
    # Parse inputs
    shapes, regions = parse(input_path)
    # Part 1
    print(f"Part 1: {part_one(shapes, regions)}")
    # Part 2
    print(f"Part 2: {part_two()}")


if __name__ == '__main__':
    main()
