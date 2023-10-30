#!/usr/bin/env python3

"""
@author Shuji Kosuge
"""
from glazesugar.CSP import CSP, Var, Domain, Alldifferent, Imp
from glazesugar.Sugar import Solver

"""
Costas Array
    input:
        order

    example:
        order  = 5
        
        solution = {0,2,3,1,4}
          0 1 2 3 4
        0 0─┬─┬─┬─┐
        1 ├─┼─┼─0─┤
        2 ├─0─┼─┼─┤
        3 ├─┼─0─┼─┤
        4 └─┴─┴─┴─0

pyCSP: https://www.csplib.org/Problems/prob076/models/CostasArray.py.html
"""


def main():
    csp = CSP()

    order = 5

    xs = []
    for n in range(1, order+1):
        x = csp.int(Var(f"INT_{n}"), Domain(1, order))
        xs.append(x)

    csp.add(Alldifferent(*xs))

    for d in range(1, order-1):
        alldiff = []
        for i in range(order - d):
            alldiff.append(xs[i]-xs[i+d])
        csp.add(Alldifferent(*alldiff))

    print(csp.output())
    solver = Solver(csp)
    result = solver.find()
    if result:
        for x in xs:
            print(f"{x}: {solver.solution(x)}")
        for i in range(order):
            print()
            for j in range(1, order+1):
                if j == solver.solution(xs[i]):
                    print(1, end=" ")
                else:
                    print(0, end=" ")


if __name__ == "__main__":
    main()
