"""AoC :: Day 11"""
from math import prod
import networkx as nx
from pathlib import Path

# Constants
input_path = Path(__file__).parent / 'Day11.in'

def parse(path: Path) -> nx.DiGraph:
    """Parse the plaintext input"""
    G = nx.DiGraph()
    for line in path.read_text().strip().splitlines():
        name, raw_outputs = line.split(": ")
        outputs = raw_outputs.split(" ")
        G.add_node(name)
        G.add_edges_from((name, output.strip()) for output in outputs if output)
    return G


def part_one(graph: nx.DiGraph, start: str = "you", stop: str = "out"):
    """Solution to part one"""
    # init counts
    counts = {}
    # iterate over topologically sorted graph
    for n in nx.topological_sort(graph):
        # Start node
        if n == start:
            counts[n] = 1
        # Only starts propagating after start
        if counts:
            for j in graph.successors(n):
                counts[j] = counts.get(j, 0) + counts.get(n, 0)
        # Stop once we reach the target
        if n == stop:
            break
    # Return number of paths that reach the stop node
    return counts[stop]

def part_two(graph: nx.DiGraph, visits: set[str], start: str = "svr", stop: str = "out"):
    """Solution to part two"""
    # Find order which nodes will be visited
    sorted_nodes = [n for n in nx.topological_sort(graph) if n in visits | {start, stop}]
    # Calculate product of paths between each consecutive pair of nodes
    return prod(part_one(graph, n1, n2) for n1, n2 in zip(sorted_nodes[:-1], sorted_nodes[1:]))


def main():
    """Run the solutions and print the results"""
    print(__doc__)
    # Parse inputs
    graph = parse(input_path)
    # Part 1
    print(f"Part 1: {part_one(graph)}")
    # Part 2
    print(f"Part 2: {part_two(graph, visits={"dac", "fft"})}")


if __name__ == '__main__':
    main()
