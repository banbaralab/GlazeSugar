from glazesugar import *

csp = CSP.CSP()
x = csp.int(CSP.Var("x"), CSP.Domain(-11, 7))
y = csp.int(CSP.Var("y"), CSP.Domain(0, 7))

csp.add(x + y == 7)
csp.add(x * y == 1)
csp.minimize(x)
solver = Sugar.Solver(csp)
result = solver.find(byCommand=True)
#print(csp.output())
if result:
    print(solver.solution())