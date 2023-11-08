#!/usr/bin/env python3

"""
@author Shuji Kosuge
"""
import argparse
from glazesugar.CSP import CSP, Var, Domain, Add, Alldifferent
from glazesugar.Sugar import Solver

"""
Magic Square
    input:
        N : Square Size
    example:
        N = 3
        solution = 
            0   1   2
          ┌───┬───┬───┐
        0 │ 4 │ 3 │ 8 │ 
          ├───┼───┼───┤
        1 │ 9 │ 5 │ 1 │
          ├───┼───┼───┤
        2 │ 2 │ 7 │ 6 │
          └───┴───┴───┘
"""

def main():
    parser = argparse.ArgumentParser(description="Magic Square Solver")
    parser.add_argument("-n", help="square size (default: 3)")
    args = parser.parse_args()

    csp = CSP()
    N = int(args.n) or 3
    xs = {}
    for i in range(N):
        for j in range(N):
            x = csp.int(Var(f"INT_{i}_{j}"), Domain(1, N*N))
            xs[f"INT_{i}_{j}"] = x

    linesum = sum(i for i in range(1, N*N+1)) // N
    for i in range(N):
        xi = []
        for j in range(N):
            xi.append(xs[f"INT_{i}_{j}"])
        csp.add(Add(*xi) == linesum)

    for j in range(N):
        xj = []
        for i in range(N):
            xj.append(xs[f"INT_{i}_{j}"])
        csp.add(Add(*xj) == linesum)

    xd1 = []
    xd2 = []
    for i in range(N):
        for j in range(N):
            if i == j:
                xd1.append(xs[f"INT_{i}_{j}"])
            if i+j-1 == N-2:
                xd2.append(xs[f"INT_{i}_{j}"])
    csp.add(Add(*xd1) == linesum)
    csp.add(Add(*xd2) == linesum)

    csp.add(Alldifferent(*xs))

    solver = Solver(csp)
    result = solver.find()
    print(csp.output())
    if result:
        for x in xs:
            print(f"{x}: {solver.solution(x)}")


if __name__ == "__main__":
    main()


