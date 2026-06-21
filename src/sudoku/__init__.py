import sys

from sudoku import puzzle, solver


def main() -> None:
    in_puzzle = sys.argv[1]
    grid = puzzle.Grid.construct(in_puzzle)
    solve = solver.Solver(grid)

    print("Initial Puzzle")
    print(grid.render())
    print()

    try:
        solve.solve()
    except solve.Unsolvable:
        print("Unable to solve")
        pass
    except puzzle.Unit.Invalid as ex:
        print(f"Uh-oh, added a Duplicate! {str(ex)}")
    else:
        print("Solved!")

    print(grid.render())

    print("")
    print(solve.report_diagnostics())
