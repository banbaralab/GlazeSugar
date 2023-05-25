#!/usr/bin/env python3

"""
@author Shuji Kosuge
version 1.0
"""

import sys
import time
import threading
from functools import singledispatchmethod

# todo: 引数の型によって返り値を変更
"""
todo:
https://yumarublog.com/python/overload/
__call__の特殊メソッドを使う

case class:
new 無しでもインスタンス化することができ、同じ属性値を持つケースクラスは等しいとみなされる

"""


class Solution:
    def __init__(self, int_values, bool_values):
        self.intValues = int_values
        self.boolValues = bool_values

    def value(self, v):
        values = {}
        values.update(**self.intValues, **self.boolValues)
        return values[str(v)]
    # todo : apply
    # 省略形で呼び出すことができる
    # 引数の型によって関数が変わる
    # @functools.singledispatch　を使う?
    # https://docs.python.org/ja/3/library/functools.html#functools.singledispatch
    # 1つ目の引数の型で呼び出す関数を決めているため，注意


TIMERCOUNT = 0


class Timer:
    def __init__(self, timeout):
        self.timeout = timeout
        self.deadline = self.currentTime + timeout if (timeout > 0) else 0
        self.timerThread = None
        self.mainThread = None
        self.timeoutTask = None
        global TIMERCOUNT
        TIMERCOUNT += 1
        self.count = TIMERCOUNT

        print(f"Timer {self.count} new")

    def currentTime(self):
        return time.time()

    def restTime(self):
        return self.deadline - self.currentTime if self.deadline > 0 else sys.maxsize

    def setTimeoutTask(self, task):
        self.timeoutTask = task

    def timerThreadBody(self):
        print(f"Timer {self.count} start {self.timeout}")
        while self.timerThread is not None or self.currentTime() < self.deadline:
            time.sleep(10)
        if self.timerThread is not None:
            self.timerThread = None
            print(f"Timer {self.count} interrupt")
            if self.timeoutTask is not None:
                self.timeoutTask()
                self.timeoutTask = None
            self.mainThread # todo pythonにスレッド割り込み機能はない
            print(f"Timer {self.count}  end")

    def start(self):
        self.mainThread = threading.current_thread()
        self.timerThread = None
        if self.deadline > 0:
            self.timerThread = threading.Thread(target=self.timerThreadBody())
            self.timerThread.start()


    def stop(self):
        print(f"Timer {self.count} stop")
        self.timeoutTask = None
        self.timerThread = None

    def raiseTimeout(self):
        print(f"Timer {self.count} timeout")
        if self.timeoutTask is not None:
            self.timeoutTask()
            self.stop()
        raise InterruptedError(f"Timeout {self.timeout} exceeded")

    def checkTimeout(self):
        if self.restTime <= 0:
            self.raiseTimeout()


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
        if name in self.solverStats[-1]:
            return self.solverStats # todo last(name)
        else:
            return {}

    # memo: pythonは引数の違う同名関数を定義することができない
    def addSolverStat(self, *args):
        if len(args) == 3:
            return self.addSolverStat(args[0], {args[1]: args[2]})
        elif len(args) == 2:
            stat1 = self.getSolverStat(args[0])
            stat1.update(args[1])
            self.solverStats.append(self.solverStats[-1].copy())
            self.solverStats[-1][args[0]] = stat1
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
        #todo measureTime

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

    @singledispatchmethod
    def value(self, x):
        pass

    @value.register
    def _(self, x:int):
        return self.solution.intValues(x)

    @value.register
    def _(self, p: bool):
        return self.solution.boolValues(p)

    def values(self, x, *xs):
        return [self.value(i) for i in xs].insert(0, self.value(x))

