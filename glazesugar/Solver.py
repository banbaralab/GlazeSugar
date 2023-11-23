#!/usr/bin/env python3

"""
@author Shuji Kosuge
"""

import sys
import time
import threading
import multiprocessing
# from functools import singledispatchmethod


class Solution:
    def __init__(self, int_values, bool_values):
        self.intValues = int_values
        self.boolValues = bool_values

    def value(self, v):
        values = {}
        values.update(**self.intValues, **self.boolValues)
        return values[str(v)]


def current_time():
    return time.time()


class Timer:
    count = 0

    def __init__(self, timeout):
        self.timeout = timeout
        self.deadline = time.time() + timeout if timeout > 0 else 0
        self.timer_process = None
        self.timeout_task = None
        Timer.count += 1
        self.count = Timer.count
        print("Timer " + str(self.count) + " new")

    def current_time(self):
        return time.time()

    def rest_time(self):
        return self.deadline - time.time() if self.deadline > 0 else sys.maxsize

    def set_timeout_task(self, task):
        self.timeout_task = task

    def _timer_function(self):
        print("Timer " + str(self.count) + " start " + str(self.timeout))
        while time.time() < self.deadline:
            time.sleep(0.01)
        print("Timer " + str(self.count) + " interrupt")
        if self.timeout_task:
            self.timeout_task()
            self.timeout_task = None
        print("Timer " + str(self.count) + " end")

    def start(self):
        if self.deadline > 0:
            self.timer_process = multiprocessing.Process(target=self._timer_function)
            self.timer_process.start()

    def stop(self):
        print("Timer " + str(self.count) + " stop")
        self.timeout_task = None
        if self.timer_process:
            self.timer_process.terminate()
            self.timer_process.join()
            self.timer_process = None

    def raise_timeout(self):
        print("Timer " + str(self.count) + " timeout")
        if self.timeout_task:
            self.timeout_task()
            self.stop()
        raise TimeoutError("Timeout (" + str(self.timeout) + ") exceeded")

    def check_timeout(self):
        if self.rest_time() <= 0:
            self.raise_timeout()


class AbstractSolver:
    def __init__(self, csp):
        self.csp = csp
        self.options = {}
        self.timeout = 0
        self.timer = None
        self.solverInfo = {}
        self.solverStats = [{}]

    def startTimer(self, t):
        if t > 0:
            self.timeout = t
            self.timer = Timer(self.timeout)
            self.timer.start()

    def stopTimer(self):
        if self.timer is not None:
            self.timer.stop()
        self.timer = None

    def checkTimeout(self):
        if self.timer is not None:
            self.timer.checkTimeout()

    def setTimeoutTask(self, task):
        if self.timer is not None:
            self.timer.setTimeoutTask(task)

    def raiseTimeout(self):
        if self.timer is not None:
            self.timer.raiseTimeout()
        raise InterruptedError(f"Timeout ({self.timeout}) exceeded")

    def addSolverInfo(self, key, value):
        self.solverInfo[key] = value

    def shiftSolverStats(self):
        return self.solverStats.append({})

    def getSolverStat(self, name):
        return self.solverStats[-1].get(name, {})

    # memo: pythonは引数の違う同名関数を定義することができない
    def addSolverStat(self, *args):
        if len(args) == 3:
            return self.addSolverStat(args[0], {args[1]: args[2]})
        elif len(args) == 2:
            stat1 = self.getSolverStat(args[0])
            stat1.update(args[1])
            self.solverStats.append(self.solverStats[-1].copy())
            self.solverStats[-1][args[0]] = stat1
            # print(stat1)
        else:
            raise TypeError("addSolverStat() takes exactly 2 or 3 arguments (%d given)" % len(args))

    class measureTime:
        def __init__(self, solver, name, key):
            self.solver = solver
            self.name = name
            self.key = key

        def __enter__(self):
            self.start_time = time.process_time()
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            end_time = time.process_time()
            elapsed_time = end_time - self.start_time
            self.solver.addSolverStat(self.name, self.key, elapsed_time)

    def init(self):
        self.solverInfo = {}
        self.solverStats = [{}]

    def commit(self):
        pass

    def cancel(self):
        pass

    def find(self):
        # self.addSolverStat("csp", "variables", self.csp.variables.size)
        # self.addSolverStat("csp", "bools", self.csp.bools.size)
        # self.addSolverStat("csp", "constraints", self.csp.constraints.size)
        with self.measureTime(self, "time", "find"):
            self.init()
            result = self.findBody()
            self.addSolverStat("result", "find", 1 if result else 0)
        return result


    def findBody(self):
        pass

    def findNext(self):
        self.shiftSolverStats()
        with self.measureTime(self, "time", "findNext"):
            result = self.findNextBody()
            # self.addSolverStat("result", "find", 1 if result else 0)
        return result

    def findNextBody(self):
        pass

    def findOpt(self):
        self.addSolverStat("csp", "variables", self.csp.variables.size)
        self.addSolverStat("csp", "bools", self.csp.bools.size)
        self.addSolverStat("csp", "constraints", self.csp.constraints.size)
        # todo

    def findOptBody(self):
        pass

    def findOptBound(self,lb,ub):
        self.shiftSolverStats
        self.addSolverStat("csp", "lb", lb)
        self.addSolverStat("csp", "ub", ub)
        # todo measureTime

    def findOptBoundBody(self):
        pass

    def solution(self):
        pass

    def solutions(self):
        first = True
        lookahead = False
        hasNextFlag = False

        if first:
            hasNextFlag = self.find()
            first = False
            lookahead = True
        elif lookahead:
            hasNextFlag = self.findNext()
            lookahead = True
        else:
            hasNextFlag = self.findNext()
            lookahead = True

        if not hasNextFlag:
            raise # todo java.util.NoSuchElementException("next on empty iterator")
        else:
            lookahead = False
            return self.solution()

    def dump(self, fileName, format):
        pass

    def value(self, x):
        if isinstance(x, int):
            return self.solution.intValues(x)
        elif isinstance(x, bool):
            return self.solution.boolValues(x)

    def values(self, x, *xs):
        return [self.value(i) for i in xs].insert(0, self.value(x))

