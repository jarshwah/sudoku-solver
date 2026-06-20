import textwrap

import pytest

from sudoku import puzzle


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
