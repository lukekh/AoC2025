"""AoC :: Day 9"""
from dataclasses import dataclass
from functools import cached_property
import heapq
from pathlib import Path

# Constants
input_path = Path(__file__).parent / 'Day09.in'


@dataclass(order=True)  # order=True so that we can put these in a heap
class Tile:
    x: int
    y: int

    def __mul__(self, other: "Tile"):
        return (abs(self.x - other.x) + 1) * (abs(self.y - other.y) + 1)


@dataclass
class Edge:
    t1: Tile
    t2: Tile

    def vertical(self):
        return self.t1.x == self.t2.x
    
    def ray_cast(self, t: Tile):
        """return True if t casts a ray through this edge"""
        return (t.x < self.t1.x) and (min(self.t1.y, self.t2.y) < t.y < max(self.t1.y, self.t2.y))
    
    @cached_property
    def xs(self):
        return sorted([self.t1.x, self.t2.x])
    
    @cached_property
    def ys(self):
        return sorted([self.t1.y, self.t2.y])
    
    def intersect(self, r1: Tile, r2: Tile):
        """true if the edge crosses or is contained by rect formed using t1 and t2"""
        mx, Mx = self.xs
        my, My = self.ys
        return (
            mx < max(r1.x, r2.x) # Check the leftmost point on edge is left of rightmost point on rect
        ) and (
            Mx > min(r1.x, r2.x) # Check the rightmost point on edge is right of leftmost point on rect
        ) and (
            my < max(r1.y, r2.y) # Check if lowest point on edge is below highest part of rect
        ) and (
            My > min(r1.y, r2.y) # Check if highest point on edge is above lowest part of rect
        )


def parse(path: Path):
    """Parse the plaintext input"""
    return [Tile(*map(int, line.split(","))) for line in path.read_text().strip().splitlines()]


def solution_generator(data: list[Tile]):
    """Generate solutions so that the heap can be used for both parts"""
    heap: list[tuple[float, tuple[Tile, Tile]]] = []
    for i, t1 in enumerate(data[:-1]):
        for t2 in data[i+1:]:
            # Use negative of area since we want to maximise this
            heapq.heappush(heap, (-(t1*t2), (t1,t2)))
    
    # Max will be the first on the heap
    yield -heap[0][0]

    edges = [Edge(t1,t2) for t1, t2 in zip(data, data[1:]+[data[0]])]
    vertical_edges = [e for e in edges if e.vertical()]

    def inside(t1: Tile):
        """Use ray casting to determine if a point is inside the polygon"""
        return sum(e.ray_cast(t1) for e in vertical_edges) % 2

    def intersect(t1: Tile, t2: Tile):
        """returns True if none of the edges intersects with the rectangle formed with t1 and t2"""
        return not any(e.intersect(t1, t2) for e in edges)

    # The heap is already ordered by rectangle size, we just need to 
    # check the rectangles are valid
    while heap:
        neg_area, (t1,t2) = heapq.heappop(heap)
        if intersect(t1, t2) and inside(t1):
            yield -neg_area


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


if __name__ == '__main__':
    main()
