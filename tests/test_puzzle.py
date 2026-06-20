import textwrap

import pytest

from sudoku import puzzle
from sudoku.puzzle import Orientation


def build_puzzle(partial: str) -> str:
    remaining = 81 - len(partial)
    return partial + "." * remaining


class TestGrid:
    class TestConstruction:
        def test_construct_no_puzzle(self):
            with pytest.raises(puzzle.InvalidGrid, match="Size 0 != 81"):
                puzzle.Grid.construct("")

        def test_construct_too_small(self):
            with pytest.raises(puzzle.InvalidGrid, match="Size 3 != 81"):
                puzzle.Grid.construct("123")

        def test_construct_too_big(self):
            with pytest.raises(puzzle.InvalidGrid, match="Size 300 != 81"):
                puzzle.Grid.construct("123" * 100)

        def test_construct_invalid_square(self):
            with pytest.raises(puzzle.InvalidGrid, match="P not in"):
                puzzle.Grid.construct("P" * 81)

        def test_construct_just_right(self):
            grid = puzzle.Grid.construct("1" * 81)
            assert len(grid) == 81

        def test_construct_all_empty(self):
            grid = puzzle.Grid.construct("." * 81)
            assert len(grid) == 81

    class TestUnits:
        def test_unit_rows(self):
            grid = puzzle.Grid.construct(build_puzzle("123456789.9.......8"))
            row0 = grid.rows[0]
            assert row0.orientation == Orientation.ROW
            assert row0.pos == 0
            assert "".join([s.value for s in row0.squares]) == "123456789"
            row1 = grid.rows[1]
            assert row1.orientation == Orientation.ROW
            assert row1.pos == 1
            assert "".join([s.value for s in row1.squares]) == ".9......."
            row2 = grid.rows[2]
            assert row2.orientation == Orientation.ROW
            assert row2.pos == 2
            assert "".join([s.value for s in row2.squares]) == "8........"

        def test_unit_cols(self):
            grid = puzzle.Grid.construct(build_puzzle("12.......34.......78......."))
            col0 = grid.columns[0]
            assert col0.orientation == Orientation.COL
            assert col0.pos == 0
            assert "".join([s.value for s in col0.squares]) == "137......"
            col1 = grid.columns[1]
            assert col1.orientation == Orientation.COL
            assert col1.pos == 1
            assert "".join([s.value for s in col1.squares]) == "248......"
            col2 = grid.columns[2]
            assert col2.orientation == Orientation.COL
            assert col2.pos == 2
            assert "".join([s.value for s in col2.squares]) == "........."

        def test_unit_boxes(self):
            layout = build_puzzle("123" + ("." * 6) + "456")
            # Put 987 in the bottom right corner
            layout = layout[:-3] + "987"
            grid = puzzle.Grid.construct(layout)
            box0 = grid.boxes[0]
            assert box0.orientation == Orientation.BOX
            assert box0.pos == 0
            assert "".join([s.value for s in box0.squares]) == "123456..."
            box8 = grid.boxes[8]
            assert box8.orientation == Orientation.BOX
            assert box8.pos == 8
            assert "".join([s.value for s in box8.squares]) == "......987"

    class TestRendering:
        def test_render_empty(self):
            grid = puzzle.Grid.construct("." * 81)
            assert grid.render() == textwrap.dedent(
                """\
                +---+---+---+
                |...|...|...|
                |...|...|...|
                |...|...|...|
                +---+---+---+
                |...|...|...|
                |...|...|...|
                |...|...|...|
                +---+---+---+
                |...|...|...|
                |...|...|...|
                |...|...|...|
                +---+---+---+"""
            )

        def test_render_puzzle(self):
            grid = puzzle.Grid.construct("123456789" + "." * (81 - 18) + "987564321")
            assert grid.render() == textwrap.dedent(
                """\
                +---+---+---+
                |123|456|789|
                |...|...|...|
                |...|...|...|
                +---+---+---+
                |...|...|...|
                |...|...|...|
                |...|...|...|
                +---+---+---+
                |...|...|...|
                |...|...|...|
                |987|564|321|
                +---+---+---+"""
            )


class TestUnit:
    def test_complete(self):
        unit = puzzle.Unit(
            pos=0,
            orientation=puzzle.Orientation.ROW,
            squares=[
                puzzle.Square((0, 0), value="1"),
                puzzle.Square((0, 1), value="2"),
                puzzle.Square((0, 2), value="3"),
                puzzle.Square((0, 3), value="4"),
                puzzle.Square((0, 4), value="5"),
                puzzle.Square((0, 5), value="6"),
                puzzle.Square((0, 6), value="7"),
                puzzle.Square((0, 7), value="8"),
                puzzle.Square((0, 8), value="9"),
            ],
        )
        assert unit.complete()

    def test_incomplete(self):
        unit = puzzle.Unit(
            pos=0,
            orientation=puzzle.Orientation.ROW,
            squares=[
                puzzle.Square((0, 0), value="1"),
                puzzle.Square((0, 1), value="2"),
                puzzle.Square((0, 2), value="3"),
                puzzle.Square((0, 3), value="4"),
                puzzle.Square((0, 4), value="5"),
                puzzle.Square((0, 5), value="6"),
                puzzle.Square((0, 6), value="7"),
                puzzle.Square((0, 7), value="8"),
                puzzle.Square((0, 8), value="."),
            ],
        )
        assert not unit.complete()

    def test_invalid(self):
        unit = puzzle.Unit(
            pos=0,
            orientation=puzzle.Orientation.ROW,
            squares=[
                puzzle.Square((0, 0), value="1"),
                puzzle.Square((0, 1), value="2"),
                puzzle.Square((0, 2), value="3"),
                puzzle.Square((0, 3), value="4"),
                puzzle.Square((0, 4), value="1"),
                puzzle.Square((0, 5), value="6"),
                puzzle.Square((0, 6), value="7"),
                puzzle.Square((0, 7), value="8"),
                puzzle.Square((0, 8), value="."),
            ],
        )
        with pytest.raises(puzzle.Unit.Invalid, match="Duplicate '1' found in ROW:0"):
            unit.valid()

    def test_valid(self):
        unit = puzzle.Unit(
            pos=0,
            orientation=puzzle.Orientation.ROW,
            squares=[
                puzzle.Square((0, 0), value="1"),
                puzzle.Square((0, 1), value="2"),
                puzzle.Square((0, 2), value="3"),
                puzzle.Square((0, 3), value="4"),
                puzzle.Square((0, 4), value="5"),
                puzzle.Square((0, 5), value="6"),
                puzzle.Square((0, 6), value="7"),
                puzzle.Square((0, 7), value="8"),
                puzzle.Square((0, 8), value="9"),
            ],
        )
        assert unit.valid()

    def test_remaining(self):
        unit = puzzle.Unit(
            pos=0,
            orientation=puzzle.Orientation.ROW,
            squares=[
                puzzle.Square((0, 0), value="1"),
                puzzle.Square((0, 1), value="."),
                puzzle.Square((0, 2), value="."),
                puzzle.Square((0, 3), value="."),
                puzzle.Square((0, 4), value="5"),
                puzzle.Square((0, 5), value="6"),
                puzzle.Square((0, 6), value="7"),
                puzzle.Square((0, 7), value="8"),
                puzzle.Square((0, 8), value="9"),
            ],
        )
        assert unit.remaining() == 3
