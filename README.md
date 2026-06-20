# Sudoku Solver

This is my attempt at a Sudoku Solver.

It will not attempt to do SEARCH or BACKTRACKING or BRUTEFORCE, only human-like
strategies will be implemented here.

The solver carries a lot of state around, including many objects that aren't easily
hashable, and therefore don't lend themselves well to backtracking algorithms.

I'm interested in what real strategies exist that people would use in practice.

## Motivation

There are two!

1. I don't get a change to write that much code anymore being in a leadership position, so I was keen to slap something together that wasn't too dissimilar to advent of code (which I really enjoy). Sudoku solver sits in the realm of being fairly simple, but still requires some thinking and learning about different strategies.

2. When I do get to write code it's often driven by AI. I really just wanted to write some code for the sake of writing code. I disabled all AI and AI-driven autocomplete for this project so I could actually *think* and make my own mistakes. Feels good man.

## Strategies

So far the strategies implemented are:

    - Naked Singles (a square has only a single possibility)
    - Hidden Singles (a possibility only exists in one candidate square)

These two seem to be enough to solve most (all?) puzzles in the EASY category.

[There is a great corpus of puzzles](https://github.com/grantm/sudoku-exchange-puzzle-bank) on
@grantm Sudoku Exchange Puzzle Bank github page, and I've used that corpus to populate
the pytest test examples.

## Running the solver

    ```sh
    uv run sudoku PUZZLESTRING
    ```
