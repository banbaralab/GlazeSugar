#!/usr/bin/env python3

"""
@author Shuji Kosuge
"""

from glazesugar import *

"""
 1 - - 2
 |   / |
 | /   |
 0     3
"""


def main():
    csp = CSP.CSP()
    color = [1, 2, 3]
    nodes = [0, 1, 2, 3]
    edges = [(0, 1), (1, 2), (2, 3), (0, 2)]
    xs = []
    for n in nodes:
        x = csp.int(CSP.Var(f"INT_{n}"), CSP.Domain(color))
        xs.append(x)
    for e in edges:
        csp.add(xs[e[0]] != xs[e[1]])
    solver = Sugar.Solver(csp)
    result = solver.find()
    if result:
        print(solver.solution())
        for x in xs:
            print(f"{x}: {solver.solution(x)}")


if __name__ == "__main__":
    main()
