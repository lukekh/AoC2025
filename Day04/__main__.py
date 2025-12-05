"""AoC :: Day 4"""
import numpy as np
from pathlib import Path


input_path = Path(__file__).parent / 'Day04.in'

ROLL_SYMBOL = "@"

def parse(path: Path):
    """Parse the plaintext input"""
    lines = path.read_text().strip().splitlines()
    rows, cols = len(lines), len(lines[0])

    # init a np.ndarray
    array = np.zeros((rows, cols), dtype=bool)
    for line in lines:
        for j, c in enumerate(line):
            array[lines.index(line), j] = (c == ROLL_SYMBOL)    
    return array

# Part one effectively implements a CNN filter with padding over the input data
FILTER = np.array(
    [[1, 1, 1],
     [1, 0, 1],
     [1, 1, 1]]
)

def part_one(data: np.ndarray, adj: int = 4):
    """Solution to part one"""
    coords: set[tuple[int, int]] = set()
    padded_data = np.pad(data, ((1,1),(1,1)), mode="constant")
    for row, vec in enumerate(data):
        for col, val in enumerate(vec):
            # Only need to count this if there is a roll there, i.e. val is True
            if val and np.sum(padded_data[row:row+3,col:col+3] * FILTER) < adj:
                coords.add((row, col))
    return coords


def part_two(data: np.ndarray, coords: set[tuple[int, int]]):
    """Solution to part two"""
    count = 0
    while coords:
        # Update data with removed rolls
        count += len(coords)
        for coord in coords:
            data[coord] = False
        # Get new coords
        coords = part_one(data)
    return count


def main():
    """Run the solutions and print the results"""
    print(__doc__)
    # Parse inputs
    data = parse(input_path)
    # Part 1
    print(f"Part 1: {len(coords := part_one(data))}")
    # Part 2
    print(f"Part 2: {part_two(data, coords)}")


if __name__ == '__main__':
    main()
