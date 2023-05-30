#!/usr/bin/env python3

"""
@author Shuji Kosuge
"""

from glazesugar import *

"""
main
"""


def main():
    csp = CSP.CSP()
    x = csp.int("x", CSP.Domain(0, 7))
    y = csp.int("y", CSP.Domain(0, 7))
    # csp.add(Eq(Add(x, y), 7)) # x + y = 7
    # csp.add(Eq(Add(Mul(x, 2), Mul(y, 4)), 20))  # (x * 2) + (y * 4) = 20
    csp.add(x + y == 7)
    csp.add((x * 2) + (y * 4) == 20)
    solver = Sugar.Solver(csp)
    result = solver.find()
    if result:
        print(f"x = {solver.solution.value(x)}")
        print(f"y = {solver.solution.value(y)}")


if __name__ == "__main__":
    main()
