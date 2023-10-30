#!/usr/bin/env python3

"""
@author Shuji Kosuge
"""
from glazesugar.CSP import CSP, Var, Domain, Alldifferent, Imp, TRUE, FALSE
from glazesugar.Sugar import Solver

"""
Hidato(Number Snake)
    input:
        positions
        instance
        numbers
        
    example:
           0 1 2
        0 |6| | |    |6|7|9|
        1 | |2|8| -> |5|2|8|
        2 |1| | |    |1|4|3|
"""

def main():
    csp = CSP()

    # positions: x integer
    #            y integer
    positions = []
    for i in range(3):
        for j in range(3):
            positions.append([i, j])

    # instance: x integer
    #           y integer
    #           num integer
    instance = [
        [0, 0, 6],
        [1, 1, 2],
        [1, 2, 8],
        [2, 0, 1]
    ]

    numbers = 9

    xs = {}
    for p in positions:
        x = csp.int(Var(f"INT_{p[0]}_{p[1]}"), Domain(1, numbers))
        xs[f"INT_{p[0]}_{p[1]}"] = x

    for data in instance:
        csp.add(xs[f"INT_{data[0]}_{data[1]}"] == data[2])

    csp.add(Alldifferent(*xs))

    for p1 in positions:
        for p2 in positions:
            if p1 == p2:
                continue
            if (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 <= 2:
                csp.add(Imp((xs[f"INT_{p1[0]}_{p1[1]}"] + 1) == xs[f"INT_{p2[0]}_{p2[1]}"], TRUE()))
            else:
                csp.add(Imp((xs[f"INT_{p1[0]}_{p1[1]}"] + 1) == xs[f"INT_{p2[0]}_{p2[1]}"], FALSE()))

    print(csp.output())
    solver = Solver(csp)
    result = solver.find()

    if result:
        for x in xs:
            print(f"{x}: {solver.solution(x)}")
        for i in range(3):
            print()
            for j in range(3):
                print(solver.solution(xs[f"INT_{i}_{j}"]), end=" ")

if __name__ == "__main__":
    main()


