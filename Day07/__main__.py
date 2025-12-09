"""AoC :: Day 7"""
from pathlib import Path

# Constants
input_path = Path(__file__).parent / 'Day07.in'
START_SYMBOL = "S"
SPLITTER_SYMBOL = "^"

def parse(path: Path):
    """Parse the plaintext input"""
    start_line, *lines = path.read_text().strip().splitlines()
    # S should be on first line
    start_index = start_line.index(START_SYMBOL)
    # Record index of each splitter in string
    splitters = [{i for i, char in enumerate(line) if char == "^"} for line in lines]
    return start_index, splitters


def part_one(start_index: int, splitters: list[set[int]]):
    """Solution to part one"""
    # init beams and counter
    beams = {start_index}
    ctr = 0
    # calculate splits on each line
    for line in splitters:
        hit_idxs = beams & line
        beams -= hit_idxs
        beams |= {i for h in hit_idxs for i in (h-1, h+1)}
        ctr += len(hit_idxs)
    return ctr


def part_two(start_index: int, splitters: list[set[int]]):
    """Solution to part two"""
    # init beams and counter
    beams = {start_index: 1}
    # calculate splits on each line
    for line in splitters:
        new_beams = {}
        for beam, count in beams.items():
            if beam in line:
                new_beams[beam-1] = new_beams.get(beam-1, 0) + count
                new_beams[beam+1] = new_beams.get(beam+1, 0) + count
            else:
                new_beams[beam] = new_beams.get(beam, 0) + count
        beams = new_beams
    return sum(beams.values())


def main():
    """Run the solutions and print the results"""
    print(__doc__)
    # Parse inputs
    start_index, splitters = parse(input_path)
    # Part 1
    print(f"Part 1: {part_one(start_index, splitters)}")
    # Part 2
    print(f"Part 2: {part_two(start_index, splitters)}")


if __name__ == '__main__':
    main()
