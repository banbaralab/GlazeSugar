#!/usr/bin/env python3

"""
@author Shuji Kosuge
"""
from glazesugar.CSP import CSP, Var, Domain, Alldifferent
from glazesugar.Sugar import Solver

"""
Golomb Ruler
    input:
        order (numbers of marker)
        length

    example:
        order  = 4
        length = 6
        01  4 6
        ├┼──┼─┤
"""

def main():
    csp = CSP()
    order = 4
    length = 6
    xs = []
    for n in range(order):
        x = csp.int(Var(f"INT_{n}"), Domain(0, length))
        xs.append(x)

    csp.add(xs[0] == 0)
    csp.add(xs[-1] == length)

    csp.add(Alldifferent(*xs))
    # for n in range(order-1):
    #     csp.add(xs[n] < xs[n+1])

    alldiff = []
    for n1 in range(order-1):
        for n2 in range(n1+1, order):
            alldiff.append(xs[n2] - xs[n1])
    csp.add(Alldifferent(*alldiff))

    solver = Solver(csp)
    result = solver.find()
    print(csp.output())
    if result:
        for x in xs:
            print(f"{x}: {solver.solution(x)}")


if __name__ == "__main__":
    main()


