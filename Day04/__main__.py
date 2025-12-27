"""AoC :: Day 4"""
import numpy as np
from pathlib import Path
# This speeds things up significantly
from scipy.signal import convolve2d

# Constants
input_path = Path(__file__).parent / "Day04.in"
ROLL_SYMBOL = "@"


def parse(path: Path):
    """Parse the plaintext input"""
    lines = path.read_text().strip().splitlines()
    rows, cols = len(lines), len(lines[0])

    # init a np.ndarray
    array = np.zeros((rows, cols), dtype=bool)
    for row, line in enumerate(lines):
        for j, c in enumerate(line):
            array[row, j] = c == ROLL_SYMBOL
    return array


# Part one effectively implements a CNN convolution over the input data
FILTER = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])


def part_one(data: np.ndarray, adj: int = 4):
    """Solution to part one"""
    # Convolve to count neighbors for each cell
    neighbor_count = convolve2d(data, FILTER, mode="same", boundary="fill", fillvalue=0)
    # Cell is True if it's set AND has fewer than `adj` neighbors
    return data & (neighbor_count < adj)


def part_two(data: np.ndarray, coord_mat: np.ndarray):
    """
    Solution to part two

    Expects the output of part one as input to save one step of computation.
    """
    move_map = np.zeros(data.shape, dtype=bool)
    while coord_mat.any():
        # Update data with removed rolls
        move_map |= coord_mat
        data &= ~coord_mat
        # Get new coords
        coord_mat = part_one(data)
    return np.sum(move_map)


def main():
    """Run the solutions and print the results"""
    print(__doc__)
    # Parse inputs
    data = parse(input_path)
    # Part 1
    print(f"Part 1: {np.sum(coords := part_one(data))}")
    # Part 2
    print(f"Part 2: {part_two(data, coords)}")


if __name__ == "__main__":
    main()
