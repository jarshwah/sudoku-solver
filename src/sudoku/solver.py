from typing import Iterable, Sequence

import attrs

from sudoku import puzzle

type Solution = str


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

    class Unsolvable(Exception): ...

    def __attrs_post_init__(self):
        self._square_rows = {sq: row for row in self.grid.rows for sq in row.squares}
        self._square_cols = {sq: col for col in self.grid.columns for sq in col.squares}
        self._square_boxes = {sq: box for box in self.grid.boxes for sq in box.squares}
        self._square_options = {
            sq: set(puzzle.ALL_NUMS) if sq.value == puzzle.EMPTY else set()
            for sq in self.grid.squares.values()
        }
        self._solved_set = set(self._non_empty_squares())
        self._changed_set = set()

    def solve(self) -> Solution:
        while not self.grid.solved():
            strategies = [
                self.strategy_reduce_options(),
            ]
            if not any(strategies):
                raise Solver.Unsolvable("".join("".join(line) for line in self.grid.lines()))
        return "".join("".join(line) for line in self.grid.lines())

    def strategy_reduce_options(self) -> bool:
        """
        Given newly-solved squares, remove that squares value from all of its neighbours options.

        Returns False if no changes were made, True otherwise.
        """
        changes = False
        while self._solved_set:
            solved = self._solved_set.pop()
            val = solved.value
            for nb in self._neighbours(solved):
                if val in self._square_options[nb]:
                    self._square_options[nb].remove(val)
                    self._changed_set.add(nb)
                    changes = True
        return changes

    def _non_empty_squares(self) -> list[puzzle.Square]:
        return [sq for sq in self.grid.squares.values() if sq.value != puzzle.EMPTY]

    def _units(self, square: puzzle.Square) -> Sequence[puzzle.Unit]:
        return [self._square_rows[square], self._square_cols[square], self._square_boxes[square]]

    def _neighbours(self, square: puzzle.Square) -> Iterable[puzzle.Square]:
        for unit in self._units(square):
            for sq in unit.squares:
                if sq != square:
                    yield sq
