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
"""


def main():
    csp = CSP()

    order = 5

    xs = []
    for n in range(order):
        x = csp.int(Var(f"INT_{n}"), Domain(0, order - 1))
        xs.append(x)

    csp.add(Alldifferent(*xs))

    # vectors:  x1 integer
    #           x2 integer
    vectors = []
    for n1 in range(order - 1):
        for n2 in range(n1 + 1, order):
            vectors.append([n1, n2])
    for v1 in range(len(vectors) - 1):
        for v2 in range(v1 + 1, len(vectors)):
            if vectors[v1][0] == vectors[v2][0]:
                continue
            ax = vectors[v1][1] - vectors[v1][0]
            ay = xs[vectors[v1][1]] - xs[vectors[v1][0]]
            bx = vectors[v2][1] - vectors[v2][0]
            by = xs[vectors[v2][1]] - xs[vectors[v2][0]]
            length_a = ay * ay + ax * ax
            length_b = by * by + bx * ax
            csp.add(Imp(length_a == length_b, ay != by))

    print(csp.output())
    solver = Solver(csp)
    result = solver.find()
    if result:
        for x in xs:
            print(f"{x}: {solver.solution(x)}")
        for i in range(order):
            print()
            for j in range(order):
                if j == solver.solution(xs[i]):
                    print(1, end=" ")
                else:
                    print(0, end=" ")


if __name__ == "__main__":
    main()
