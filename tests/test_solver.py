import pytest

from sudoku import puzzle
from sudoku.solver import Solver

from .helpers import build_puzzle, solved_puzzle


class TestSolver:
    class TestLookups:
        def test_reverse_lookups(self):
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
            assert solver._square_options[first] == set()

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
            assert solver._square_options[last] == set()

            forth = grid.squares[0, 3]
            assert solver._square_options[forth] == puzzle.ALL_NUMS

    class TestSolve:
        def test_already_solved_puzzle(self):
            already_solved = solved_puzzle()
            assert Solver(puzzle.Grid.construct(already_solved)).solve() == already_solved

        def test_almost_solved_puzzle(self):
            already_solved = solved_puzzle()
            almost_solved = already_solved[:-1] + "."
            assert Solver(puzzle.Grid.construct(almost_solved)).solve() == already_solved

        def test_unsolvable(self):
            # An empty puzzle can't be solved without brute-forcing/backtracking, which
            # this will not support.
            with pytest.raises(Solver.Unsolvable, match="....."):
                Solver(puzzle.Grid.construct(build_puzzle(""))).solve()

    class TestEasyPuzzles:
        @pytest.mark.parametrize(
            "example",
            [
                # Test Cases from: https://raw.githubusercontent.com/grantm/sudoku-exchange-puzzle-bank/refs/heads/master/easy.txt
                pytest.param(
                    "050703060007000800000816000000030000005000100730040086906000204840572093000409000",
                    id="0000183b305c",
                ),
                pytest.param(
                    "302401809001000300000000000040708010780502036000090000200609003900000008800070005",
                    id="0001d5d6314e",
                ),
                pytest.param(
                    "000823001003000400070000052300960010000102000010038006830000040002000900600789000",
                    id="000212406270",
                ),
                pytest.param(
                    "000703000100904002400000003046000790000000000003000800007090100065070420010060080",
                    id="014f9fe70845",
                ),
                pytest.param(
                    "050720800900000000030800602020000005005030100400000060709003020000000004003092010",
                    id="01b05e3b9316",
                ),
                pytest.param(
                    "000000200030080007920006080089005001000703000100200540090600054200070090008000000",
                    id="01d27156e360",
                ),
                pytest.param(
                    "020075300003006502590000060760103000900040005000509037070000051209300700004810090",
                    id="001ebdd0faf7",
                ),
                pytest.param(
                    "000070400040300270758000100000265040600704003070813000007000526062007080003050000",
                    id="815a2690da29",
                ),
                pytest.param(
                    "009000000070900640020157009008596320003702500057831900400378010032005090000000700",
                    id="84a799f72a6c",
                ),
                pytest.param(
                    "000207950871050020200000040700103004090000030600809005080000002030010569016302000",
                    id="9b7715d9457b",
                ),
            ],
        )
        def test_puzzles(self, example: str):
            assert Solver(puzzle.Grid.construct(example)).solve()
