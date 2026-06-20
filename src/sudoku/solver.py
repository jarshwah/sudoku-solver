import attrs

from sudoku import puzzle

type Solution = str


@attrs.define
class Solver:
    grid: puzzle.Grid

    # reverse lookup from squares to the related units
    _square_rows: dict[puzzle.Square, puzzle.Unit] = attrs.field(init=False)
    _square_cols: dict[puzzle.Square, puzzle.Unit] = attrs.field(init=False)
    _square_boxes: dict[puzzle.Square, puzzle.Unit] = attrs.field(init=False)
    _square_options: dict[puzzle.Square, set[str]] = attrs.field(init=False)

    def __attrs_post_init__(self):
        self._square_rows = {sq: row for row in self.grid.rows for sq in row.squares}
        self._square_cols = {sq: col for col in self.grid.columns for sq in col.squares}
        self._square_boxes = {sq: box for box in self.grid.boxes for sq in box.squares}
        self._square_options = {
            sq: set(puzzle.ALL_NUMS) if sq.value == puzzle.EMPTY else set()
            for sq in self.grid.squares.values()
        }

    def solve(self) -> Solution:
        return "".join("".join(line) for line in self.grid.lines())
