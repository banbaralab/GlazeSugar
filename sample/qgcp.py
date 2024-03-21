#!/usr/bin/env python3

"""
Queen Graph Coloring Problem
    example:
        N = 5
        solution =
            0   1   2   3   4
          ┌───┬───┬───┬───┬───┐
        0 │ 1 │ 2 │ 3 │ 4 │ 5 │
          ├───┼───┼───┼───┼───┤
        1 │ 4 │ 5 │ 1 │ 2 │ 3 │
          ├───┼───┼───┼───┼───┤
        2 │ 2 │ 3 │ 4 │ 5 │ 1 │
          ├───┼───┼───┼───┼───┤
        3 │ 5 │ 1 │ 2 │ 3 │ 4 │
          ├───┼───┼───┼───┼───┤
        4 │ 3 │ 4 │ 5 │ 1 │ 2 │
          └───┴───┴───┴───┴───┘

@author S. Kosuge
"""
import argparse
from glazesugar.CSP import CSP, Var, Domain, Alldifferent
from glazesugar.Sugar import Solver


def main():
    parser = argparse.ArgumentParser(description="Queen Graph Coloring Problem Solver")
    parser.add_argument("-n", help="square size (default: 5)", default=5)
    args = parser.parse_args()

    N = int(args.n)

    csp = CSP()

    xs = {}
    for i in range(N):
        for j in range(N):
            xs[f"INT_{i}_{j}"] = csp.int(Var(f"INT_{i}_{j}"), Domain(1, N))

    for i in range(N):
        csp.add(Alldifferent(*[xs[f"INT_{i}_{j}"] for j in range(N)]))

    for j in range(N):
        csp.add(Alldifferent(*[xs[f"INT_{i}_{j}"] for i in range(N)]))

    for u in range(2*N-1):
        csp.add(Alldifferent(*[xs[f"INT_{i}_{u-i}"] for i in range(N) if 0 <= u - i < N]))

    for d in range(-N+1, N):
        csp.add(Alldifferent(*[xs[f"INT_{i}_{i-d}"] for i in range(N) if 0 <= i - d < N]))

    for j in range(N):
        csp.add(xs[f"INT_0_{j}"] == j+1)

    solver = Solver(csp)
    result = solver.find()
    if result:
        print(solver.solution())


if __name__ == "__main__":
    main()


