from sudoku import puzzle
from sudoku.solver import Solver

from .helpers import build_puzzle


class TestSolver:
    class TestLookups:
        grid = puzzle.Grid.construct(build_puzzle("123...789"))
        solver = Solver(grid)

        # the 1 is in row 1, column 1, box 1 (1-indexed)
        first = grid.squares[0, 0]
        row = solver._square_rows[first]
        assert row.orientation == puzzle.Orientation.ROW
        assert row.pos == 0
        assert first in row.squares
        col = solver._square_cols[first]
        assert col.orientation == puzzle.Orientation.COL
        assert col.pos == 0
        assert first in col.squares
        box = solver._square_boxes[first]
        assert box.orientation == puzzle.Orientation.BOX
        assert box.pos == 0
        assert first in box.squares
        solver._square_options[first] == set()

        # the 9 is in row 1, column 9, box 3 (1-indexed)
        last = grid.squares[0, 8]
        row = solver._square_rows[last]
        assert row.orientation == puzzle.Orientation.ROW
        assert row.pos == 0
        assert last in row.squares
        col = solver._square_cols[last]
        assert col.orientation == puzzle.Orientation.COL
        assert col.pos == 8
        assert last in col.squares
        box = solver._square_boxes[last]
        assert box.orientation == puzzle.Orientation.BOX
        assert box.pos == 2
        assert last in box.squares
        solver._square_options[last] == set()

        forth = grid.squares[0, 3]
        assert solver._square_options[forth] == puzzle.ALL_NUMS
