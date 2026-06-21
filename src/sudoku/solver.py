import itertools
from collections import Counter, defaultdict
from typing import Iterable, Sequence

import attrs

from sudoku import puzzle

type Solution = str


@attrs.define(frozen=True)
class SolverDiagnostic:
    turn: int
    label: str
    squares_affected: int


@attrs.define
class Solver:
    """
    Sudoku solver that does NOT support search or backtracking.
    """

    grid: puzzle.Grid

    # reverse lookup from squares to the related units
    _square_rows: dict[puzzle.Square, puzzle.Unit] = attrs.field(init=False)
    _square_cols: dict[puzzle.Square, puzzle.Unit] = attrs.field(init=False)
    _square_boxes: dict[puzzle.Square, puzzle.Unit] = attrs.field(init=False)
    _square_options: dict[puzzle.Square, set[str]] = attrs.field(init=False)

    # "event" queues for interesting squares that need looking into
    _solved_set: set[puzzle.Square] = attrs.field(init=False)
    _changed_set: set[puzzle.Square] = attrs.field(init=False)

    _turn: int = 0
    _diagnostics: list[SolverDiagnostic] = attrs.field(init=False)

    class Unsolvable(Exception): ...

    def __attrs_post_init__(self):
        self._square_rows = {sq: row for row in self.grid.rows for sq in row.squares}
        self._square_cols = {sq: col for col in self.grid.columns for sq in col.squares}
        self._square_boxes = {sq: box for box in self.grid.boxes for sq in box.squares}
        self._square_options = {
            sq: set(puzzle.ALL_NUMS) if sq.is_empty else set() for sq in self.grid.squares.values()
        }
        self._changed_set = set()
        self._diagnostics = []

    def solve(self) -> Solution:

        initial_squares = set(self._non_empty_squares())
        for sq in initial_squares:
            # We'll "set" the value again, but no worries.
            self._solve_square(sq, sq.value)
        self._record_diagnostic("InitialSolved", len(initial_squares))

        while not self.grid.solved():
            self._turn += 1
            strategies = [
                self.strategy_naked_single(),
                self.strategy_hidden_single(),
            ]
            if not any(strategies):
                raise Solver.Unsolvable("".join("".join(line) for line in self.grid.lines()))
        return "".join("".join(line) for line in self.grid.lines())

    def _solve_square(self, square: puzzle.Square, value: str) -> None:
        """
        When solving a square, clear out square and neighbouring square possibilities.

        Add any changing neighbours to the change queue, so we inspect them for naked singles.
        """

        square.value = value
        self._square_options[square].clear()
        # Remove value from any neighbouring (row, column, or box) possibilities
        for nb in self._neighbours(square):
            if value in self._square_options[nb]:
                self._square_options[nb].remove(value)
                self._changed_set.add(nb)

    def strategy_naked_single(self) -> bool:
        """
        Inspect the changed-set, and solve any squares with a single option remaining.

        Returns False if no squares could be solved, True otherwise.
        """
        changes = 0
        for changed in self._changed_set:
            if len(self._square_options[changed]) == 1:
                self._solve_square(changed, self._square_options[changed].pop())
                changes += 1
        if changes:
            self._record_diagnostic("NakedSingle", changes)
        return bool(changes)

    def strategy_hidden_single(self) -> bool:
        """
        Inspect the possibles of each cell, if a possible is noted only once in the Unit it
        can't go anywhere else, so that's the value.
        """
        changes = 0
        for unit in itertools.chain(self.grid.columns, self.grid.rows, self.grid.boxes):
            # Use a counter to find count of each possible in the group, if the count is 1, then
            # we know the possible can't go anywhere else, even if the square had multiple possibilities.
            # It's the inverse of the naked single.
            singles = {
                item
                for item, count in Counter(
                    itertools.chain.from_iterable(self._square_options[sq] for sq in unit.squares)
                ).items()
                if count == 1
            }
            for sq in unit.squares:
                if match := singles & self._square_options[sq]:
                    # found a hidden single!
                    changes += 1
                    # We can't have multiple singles matching a single square, so assume it's one and pop the match.
                    self._solve_square(sq, match.pop())
        if changes:
            self._record_diagnostic("HiddenSingle", changes)
        return bool(changes)

    def _non_empty_squares(self) -> list[puzzle.Square]:
        return [sq for sq in self.grid.squares.values() if sq.value != puzzle.EMPTY]

    def _units_of_square(self, square: puzzle.Square) -> Sequence[puzzle.Unit]:
        return [self._square_rows[square], self._square_cols[square], self._square_boxes[square]]

    def _neighbours(self, square: puzzle.Square) -> Iterable[puzzle.Square]:
        for unit in self._units_of_square(square):
            for sq in unit.squares:
                if sq != square:
                    yield sq

    def report_diagnostics(self) -> str:
        count_solves_per_strategy: defaultdict[str, int] = defaultdict(int)
        for diag in self._diagnostics:
            count_solves_per_strategy[diag.label] += diag.squares_affected
        num_turns = self._diagnostics[-1].turn
        report = ["Diagnostics", "==========="]
        report.extend(
            [f"Strategy: {label} -> {count}" for label, count in count_solves_per_strategy.items()]
        )
        report.extend(["", "Statistics", "==========", f"Turns: {num_turns}"])
        return "\n".join(report)

    def _record_diagnostic(self, label: str, affected: int) -> None:
        self._diagnostics.append(
            SolverDiagnostic(turn=self._turn, label=label, squares_affected=affected)
        )
