"""AoC :: Day 8"""
from dataclasses import dataclass
from math import prod
from pathlib import Path
from typing import Self

import networkx as nx

# Constants
input_path = Path(__file__).parent / "Day08.in"
LIMIT: int = 1000


@dataclass
class JunctionBox:
    x: int
    y: int
    z: int

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    @classmethod
    def parse(cls, s: str) -> Self:
        """parse from a list of comma separated coordinates"""
        x, y, z = map(int, s.split(","))
        return cls(x, y, z)

    def dist2(self, other: "JunctionBox") -> float:
        """returns the square of the distance between itself and the other box"""
        return (self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2


def parse(path: Path):
    """Parse the plaintext input"""
    return [JunctionBox.parse(row) for row in path.read_text().strip().splitlines()]


def solution_generator(data: list[JunctionBox], limit: int = LIMIT):
    """A generator that yields the solutions to both parts"""
    # All pairs possible sorted from closest to furthest away
    dist2_ranked_pairs = sorted(
        ((j1.dist2(j2), (j1, j2)) for i, j1 in enumerate(data) for j2 in data[i+1:]),
        key=lambda t: t[0],
    )

    graph: nx.Graph[JunctionBox] = nx.Graph()
    remaining_nodes = set(data)

    # Determine edges
    for _, (j1, j2) in dist2_ranked_pairs[:limit]:
        graph.add_edge(j1, j2)
        remaining_nodes -= {j1, j2}

    # Yield solution to part one
    yield prod(
        sorted(map(len, nx.connected_components(graph)))[-3:]
    )

    # Continue on until it is one connected component
    for _, (j1, j2) in dist2_ranked_pairs[limit:]:
        graph.add_edge(j1, j2)
        remaining_nodes -= {j1, j2}
        if not remaining_nodes and nx.is_connected(graph):
            # Yield solution to part two
            yield j1.x * j2.x

    raise ValueError("graph was never connected")


def main():
    """Run the solutions and print the results"""
    print(__doc__)
    # Parse inputs
    data = parse(input_path)
    gen = solution_generator(data)
    # Part 1
    print(f"Part 1: {next(gen)}")
    # Part 2
    print(f"Part 2: {next(gen)}")


if __name__ == "__main__":
    main()
