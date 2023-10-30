#!/usr/bin/env python3

"""
@author Shuji Kosuge
"""

from glazesugar import *

"""
main
"""


def main():
    # csp = CSP.CSP()
    # x = csp.int(CSP.Var("x"), CSP.Domain(0, 7))
    # y = csp.int(CSP.Var("y"), CSP.Domain(0, 7))
    # # csp.add(Eq(Add(x, y), 7)) # x + y = 7
    # # csp.add(Eq(Add(Mul(x, 2), Mul(y, 4)), 20))  # (x * 2) + (y * 4) = 20
    # csp.add(x + y == 7)
    # csp.add((x * 2) + (y * 4) == 20)
    # solver = Sugar.Solver(csp)
    # result = solver.find()
    print(CSP.Domain([0]))
    print(CSP.Domain([2, 5]))
    print(CSP.Domain([1,3,4,2,3,4]))

    # print(CSP.Domain([0, 4]))
    # if result:
    #     print(solver.solution())
        # print(f"{x} = {solver.solution(x)}")
        # print(f"{x} = {solver.solution(y)}")
        # print(f"{solver.solution(x,y)}")


if __name__ == "__main__":
    main()
