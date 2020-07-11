from sortedcontainers import SortedDict

import workingMemory as wm

class BaseSimulator:

    def __init__(self):
        self.currentTime = 0.0
        self.eventList = SortedDict()

    def addEvent(self, time, funcName, args):
        self.eventList[time] = [funcName, args]

    def deleteEvents(self, timeList):
        try:
            for key in timeList:
                self.eventList.pop(key)
        except KeyError:
            return

    def completeRun(self):
        try:
            while self.eventList.peekitem(0):
                self.currentTime, funcCall = self.eventList.peekitem(0)
                funcCall[0](funcCall[1])
                self.eventList.popitem(0)
        except IndexError:
            return

    def run(self, timeLimit = 0):
        try:
            while self.eventList.peekitem(0):
                currentTime, funcCall = self.eventList.peekitem(0)
                if 'timeLimit' in locals():
                    if currentTime >= timeLimit:
                        return
                funcCall[0](funcCall[1])
                self.currentTime = currentTime
                self.eventList.popitem(0)
        except IndexError:
            return


class Simulator(BaseSimulator):
    def __init__(self, config = dict()):
        BaseSimulator.__init__(self)
        if config:
            self.memory = wm.WorkingMemory(config)
        else:
            self.memory = wm.WorkingMemory()
        self.memory.createGraph()

    def addMemoryElement(self, value):
        oldDecayTimes, newDecayTimes = self.memory.addElement(value, self.currentTime)
        self.deleteEvents(list(oldDecayTimes))
        for key, value in newDecayTimes.items():
            self.addEvent(key, self.memory.deleteElement, value)

    def reset(self, config):
        BaseSimulator.__init__(self)
        self.memory.createGraph(config = config)
