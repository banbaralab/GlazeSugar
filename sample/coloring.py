#!/usr/bin/env python3

"""
@author Shuji Kosuge
"""
from glazesugar.CSP import CSP, Var, Domain
from glazesugar.Sugar import Solver



def main():
    csp = CSP()
    color = [1, 2, 3]
    nodes = [0, 1, 2, 3]
    edges = [(0, 1), (1, 2), (2, 3), (0, 2)]
    xs = []
    for n in nodes:
        x = csp.int(Var(f"INT_{n}"), Domain(color))
        xs.append(x)
    for e in edges:
        csp.add(xs[e[0]] != xs[e[1]])
    solver = Solver(csp)
    result = solver.find()
    if result:
        print(solver.solution())
        for x in xs:
            print(f"{x}: {solver.solution(x)}")


if __name__ == "__main__":
    main()


