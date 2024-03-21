# GlazeSugar

![著者](https://img.shields.io/badge/author-Kosuge-blueviolet)
![バージョン](https://img.shields.io/badge/version-0.0.1-blue)

Python Interface of Sugar.

## REQUIREMENTS
+ [sugar](https://gitlab.com/cspsat/prog-sugar)
+ [kissat](https://github.com/arminbiere/kissat)


## Installation
```commandline
git clone https://gitlab.com/cspsat/prog-sugar
git clone https://github.com/arminbiere/kissat
cd kissat
./configure && make test
cd ..
pip install .
```

## Usage
### commandline
```commandline
$ python
>>> from glazesugar import CSP, Sugar
>>> a = csp.bool(CSP.Bool("a"))
>>> b = csp.bool(CSP.Bool("b"))
>>> csp.add(CSP.And(a, b))
>>> solver = Sugar.Solver(csp)
>>> solver.find()
True
>>> csp.add(CSP.Not(a))
>>> solver.find()
False
```

###
```commandline
python toy.py
```

```python:toy.py
# toy.py
from glazesugar import *

csp = CSP.CSP()
x = csp.int(CSP.Var("x"), CSP.Domain(-11, 7))
y = csp.int(CSP.Var("y"), CSP.Domain(0, 7))

csp.add(x + y == 7)
csp.add((x * 2) + (y * 4) == 20)
solver = Sugar.Solver(csp)
result = solver.find()
print(csp.output())
if result:
    print(solver.solution())
```
