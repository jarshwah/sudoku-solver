import attrs


class InvalidGrid(Exception): ...


type Coord = tuple[int, int]

EMPTY: str = "."
NUMBERS: str = "123456789"
ALLOWED: str = NUMBERS + EMPTY


@attrs.define(frozen=False)
class Square:
    location: str
    value: str
    options: str

    def __hash__(self) -> int:
        return hash(self.location)


@attrs.define
class Grid:
    squares: dict[Coord, Square] = attrs.Factory(dict[Coord, Square])

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
            squares[(row, col)] = Square(
                location=f"R{row}C{col}", value=sq, options=NUMBERS
            )
            col += 1
            if col >= 9:
                row += 1
                col = 0
        return Grid(squares=squares)

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

    def _lines(self) -> list[str]:
        lines: list[str] = []
        for rc in range(9):
            line: list[str] = []
            for cc in range(9):
                line.append(self.squares[(rc, cc)].value)
            lines.append("".join(line))
        return lines

    def __len__(self) -> int:
        return len(self.squares)
