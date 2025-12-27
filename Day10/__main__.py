"""AoC :: Day 10"""
from dataclasses import dataclass
from pathlib import Path
import re

from ortools.linear_solver import pywraplp

# Constants
input_path = Path(__file__).parent / 'Day10.in'


@dataclass
class Lights:
    """An array of indicator lights represented as a binary integer"""
    goal: int
    buttons: list[int]
    joltage: list[int]
    state: int = 0
    
    def apply(self, schematic: int):
        """Apply a schematic to the lights"""
        self.state = self.state ^ schematic
    
    @staticmethod
    def _button_tuple_to_int(s: str):
        return sum(2**int(i) for i in s.split(","))
    
    def _button_to_joltage(self, button: int):
        n = len(self.joltage)
        v = list(map(int, bin(button)[2:]))
        if len(v) < n:
            v = [0,]*(n-len(v)) + v
        return v
    
    @classmethod
    def parse(cls, line: str):
        """parse a line of inputs into Lights"""
        # Parse the goal e.g. [#.#] -> 5
        re_goal = re.compile(r"\[((\.|#)+)\]")
        m_goal = re_goal.search(line)
        assert m_goal is not None, f"goal str not found in '{line}'"
        goal = int("".join(reversed(m_goal.group(1))).replace(".", "0").replace("#", "1"), 2)

        # Parse the buttons e.g. (1,3) -> 10
        re_button = re.compile(r"\(((\d+,?)+)\)")
        m_button = re_button.finditer(line)
        buttons = [cls._button_tuple_to_int(m.group(1)) for m in m_button]

        # Parse the joltage
        re_joltage = re.compile(r"\{((\d+,?)+)\}")
        m_joltage = re_joltage.search(line)
        assert m_joltage is not None, f"joltage str not found in '{line}'"
        joltage = list(map(int, reversed(m_joltage.group(1).split(","))))

        return cls(goal=goal, buttons=buttons, joltage=joltage)

    def solve_lights(self):
        """Find the least number of button presses to get from the initial state to the goal"""
        # init
        steps = 0
        visited = {self.state}
        cursors = {self.state}

        while self.goal not in cursors:
            cursors = {cursor^button for cursor in cursors for button in self.buttons}
            cursors -= visited
            visited |= cursors
            steps += 1

        return steps

    def solve_joltage(self) -> int:
        """Meet the joltage requirements with the least number of button presses"""
        # Create the mip solver with the CP-SAT backend.
        solver: pywraplp.Solver = pywraplp.Solver.CreateSolver("SAT")
        if not solver:
            raise Exception("solver not initialised")

        # Create the data model
        m, n = len(self.joltage), len(self.buttons)
        coefficients = self._create_coefficient_matrix()

        # Define the variables
        infinity = solver.infinity()
        x: dict[int, pywraplp.Variable] = {
            j: solver.IntVar(0, infinity, f"x[{j}]") for j in range(n)
        }

        # Set the constraints (sum of coeffs * x >= joltage requirement)
        for i in range(m):
            constraint: pywraplp.Constraint = solver.Constraint(self.joltage[i], self.joltage[i])
            for j in range(n):
                constraint.SetCoefficient(x[j], coefficients[j][i])

        # Set the objective function (minimize total button presses)
        objective: pywraplp.Objective = solver.Objective()
        for j in range(n):
            # Each button press adds 1 to the objective
            objective.SetCoefficient(x[j], 1)
        objective.SetMinimization()

        # Solve the system
        solver.Solve()
        return int(objective.Value())

    def _create_coefficient_matrix(self):
        """Stores the data for the problem."""
        return [
            self._button_to_joltage(button) for button in self.buttons
        ]


def parse(path: Path):
    """Parse the plaintext input"""
    return [
        Lights.parse(line) for line in path.read_text().strip().splitlines()
    ]


def part_one(data: list[Lights]):
    """Solution to part one"""
    return sum(lights.solve_lights() for lights in data)


def part_two(data: list[Lights]):
    """Solution to part two"""
    return sum(lights.solve_joltage() for lights in data)


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
