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

    class TestPuzzles:
        @pytest.mark.parametrize(
            "example",
            [
                # Test Cases from: https://raw.githubusercontent.com/grantm/sudoku-exchange-puzzle-bank/refs/heads/master/easy.txt
                pytest.param(
                    "050703060007000800000816000000030000005000100730040086906000204840572093000409000",
                    id="1.2 0000183b305c",
                ),
                pytest.param(
                    "302401809001000300000000000040708010780502036000090000200609003900000008800070005",
                    id="1.2 0001d5d6314e",
                ),
                pytest.param(
                    "000823001003000400070000052300960010000102000010038006830000040002000900600789000",
                    id="1.2 000212406270",
                ),
                pytest.param(
                    "000703000100904002400000003046000790000000000003000800007090100065070420010060080",
                    id="1.2 014f9fe70845",
                ),
                pytest.param(
                    "050720800900000000030800602020000005005030100400000060709003020000000004003092010",
                    id="1.2 01b05e3b9316",
                ),
                pytest.param(
                    "000000200030080007920006080089005001000703000100200540090600054200070090008000000",
                    id="1.2 01d27156e360",
                ),
                pytest.param(
                    "020075300003006502590000060760103000900040005000509037070000051209300700004810090",
                    id="1.2 001ebdd0faf7",
                ),
                pytest.param(
                    "000070400040300270758000100000265040600704003070813000007000526062007080003050000",
                    id="1.2 815a2690da29",
                ),
                pytest.param(
                    "009000000070900640020157009008596320003702500057831900400378010032005090000000700",
                    id="1.2 84a799f72a6c",
                ),
                pytest.param(
                    "000207950871050020200000040700103004090000030600809005080000002030010569016302000",
                    id="1.2 9b7715d9457b",
                ),
            ],
        )
        def test_easy_puzzles(self, example: str):
            assert Solver(puzzle.Grid.construct(example)).solve()

        @pytest.mark.parametrize(
            "example",
            [
                # Test Cases from: https://raw.githubusercontent.com/grantm/sudoku-exchange-puzzle-bank/refs/heads/master/medium.txt
                pytest.param(
                    "802600009000058000006000401090406005020000040600203090205000900000970000100002804",
                    id="1.7 00010f10503b",
                    marks=pytest.mark.xfail(strict=True),
                ),
                pytest.param(
                    "100009570798040000600002000012000008000000000500000320000300005000070416061200003",
                    id="1.7 000293df085f",
                    marks=pytest.mark.xfail(strict=True),
                ),
                pytest.param(
                    "002806100000090000300000007003000200600704008820000045000010000140080063030050080",
                    id="1.5 00031bba2da0",
                ),
                pytest.param(
                    "000030000092040008016800200500003700000080000008700009001004970400020160000050000",
                    id="1.5 00058871b3f3",
                ),
                pytest.param(
                    "090030020005806100730000085007109800000403000010000050000000000580000079900501002",
                    id="1.7 000922b5dcb8",
                ),
                pytest.param(
                    "060000020000000000290000053000000000607108205008326700100465007000000000005907800",
                    id="2.0 001132c3c9e4",
                ),
                pytest.param(
                    "053000420007508600008020900000050000200000004090784010104000807000000000002607100",
                    id="2.3 00145ea935d0",
                ),
                pytest.param(
                    "100900030000020005540700009800500060050108040010004008300007082900030000070009003",
                    id="2.0 001be3153642",
                ),
                pytest.param(
                    "009006070800020500040301000004000030000187000020000100000703050006040003090600800",
                    id="1.5 00351a0e84f8",
                ),
                pytest.param(
                    "070000020030809050680000071900030004800704009004501700006403100000205000000010000",
                    id="2.3 735adc770cd3",
                ),
                pytest.param(
                    "601708405090000010008020600000000000063000850000602000005080900070060080206000103",
                    id="1.7 74dc277dc5cb",
                    marks=pytest.mark.xfail(strict=True),
                ),
                pytest.param(
                    "029006004000000020847001600070560030900000006050084010008700465010000000700300290",
                    id="1.5 9cd4b1145022",
                ),
                pytest.param(
                    "003400090098073001200000000080002700020000080006300020000000009900860370050001600",
                    id="2.3 000ff78ac1f4",
                ),
            ],
        )
        def test_medium_puzzles(self, example: str):
            assert Solver(puzzle.Grid.construct(example)).solve()
