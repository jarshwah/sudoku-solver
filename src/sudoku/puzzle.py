import enum
import itertools
from collections import Counter, defaultdict

import attrs


class InvalidGrid(Exception): ...


type Coord = tuple[int, int]

EMPTY: str = "."
NUMBERS: str = "123456789"
ALLOWED: str = NUMBERS + EMPTY
ALL_NUMS: frozenset[str] = frozenset({num for num in NUMBERS})


@enum.unique
class Orientation(enum.StrEnum):
    ROW = "ROW"
    COL = "COL"
    BOX = "BOX"


@attrs.define(frozen=False)
class Unit:
    """
    Groups a column, row, or box.
    """

    pos: int
    orientation: Orientation
    squares: list[Square]

    _valid: bool = False

    def __hash__(self) -> int:
        return hash(f"{self.pos}-{self.orientation.value}")

    def complete(self) -> bool:
        return {sq.value for sq in self.squares} == ALL_NUMS

    def remaining(self) -> int:
        return sum(sq.value == EMPTY for sq in self.squares)

    def valid(self) -> bool:
        if self._valid:
            return True
        dupes = [
            item
            for item, count in Counter(
                [sq.value for sq in self.squares if sq.value != EMPTY]
            ).items()
            if count > 1
        ]
        if dupes:
            raise Unit.Invalid(
                f"Duplicate '{dupes[0]}' found in {self.orientation.value}:{self.pos}"
            )
        complete = self.complete()
        if complete:
            self._valid = True
        return complete

    class Invalid(Exception): ...


@attrs.define(frozen=False)
class Square:
    location: Coord
    value: str

    def __hash__(self) -> int:
        return hash(self.location)

    @property
    def is_empty(self) -> bool:
        return self.value == EMPTY


@attrs.define(frozen=True)
class Grid:
    squares: dict[Coord, Square] = attrs.Factory(dict[Coord, Square])

    rows: list[Unit] = attrs.field(init=False)
    columns: list[Unit] = attrs.field(init=False)
    boxes: list[Unit] = attrs.field(init=False)

    @classmethod
    def construct(cls, puzzle: str) -> Grid:
        """
        puzzle is an 81-length string of the form: "1..3..45....7" ...
        Where "." represents an empty square.
            R0C0 = 1
            R0C1 = EMPTY
            R0C3 = 3
        """
        if (sz := len(puzzle)) != 81:
            raise InvalidGrid(f"Size {sz} != 81")
        row = col = 0
        squares: dict[Coord, Square] = {}
        for sq in puzzle:
            if sq not in ALLOWED:
                raise InvalidGrid(f"{sq} not in {ALLOWED}")
            squares[(row, col)] = Square(location=(row, col), value=sq)
            col += 1
            if col >= 9:
                row += 1
                col = 0
        return Grid(squares=squares)

    def solved(self) -> bool:
        return all(unit.valid() for unit in itertools.chain(self.rows, self.columns, self.boxes))

    def _unit_rows(self) -> list[Unit]:
        return [
            Unit(rc, Orientation.ROW, [self.squares[rc, cc] for cc in range(9)]) for rc in range(9)
        ]

    def _unit_cols(self) -> list[Unit]:
        return [
            Unit(cc, Orientation.COL, [self.squares[rc, cc] for rc in range(9)]) for cc in range(9)
        ]

    def _unit_boxes(self) -> list[Unit]:
        # group the squares to "box-coordinates" in a 3x3 matrix
        mapping: dict[Coord, list[Square]] = defaultdict(list)
        for rc in range(9):
            for cc in range(9):
                mapping[(rc // 3, cc // 3)].append(self.squares[rc, cc])
        # then construct the units from the mapping
        combos = zip(itertools.product(range(3), range(3)), itertools.count())
        return [Unit(num, Orientation.BOX, mapping[rc, cc]) for (rc, cc), num in combos]

    def __attrs_post_init__(self):
        object.__setattr__(self, "rows", self._unit_rows())
        object.__setattr__(self, "columns", self._unit_cols())
        object.__setattr__(self, "boxes", self._unit_boxes())

    def render(self) -> str:
        """
        Pretty-print the game board to a string, ready for display.
        """
        if (sz := len(self)) != 81:
            raise InvalidGrid(f"Size {sz} != 81")
        SEP = "+---+---+---+"
        WALL = "|"

        lines: list[str] = []
        for rc in range(9):
            if rc % 3 == 0:
                lines.append(SEP)
            line: list[str] = []
            for cc in range(9):
                if cc % 3 == 0:
                    line.append(WALL)
                line.append(self.squares[(rc, cc)].value)
            line.append(WALL)
            lines.append("".join(line))
        lines.append(SEP)
        return "\n".join(lines)

    def lines(self) -> list[str]:
        lines: list[str] = []
        for rc in range(9):
            line: list[str] = []
            for cc in range(9):
                line.append(self.squares[(rc, cc)].value)
            lines.append("".join(line))
        return lines

    def __len__(self) -> int:
        return len(self.squares)
