import calendar
import time
import random
import collections
import math
import queue
from minStrong import *

defaultConfig = {"numNodes" : 7,
        "maxDelayTime" : 1000,
        "createEdgeThreshold" : 0.7,
        "edgeWeightMax" : 10}

class WorkingMemory:
    def generateRandomNumber(self):
        return float(random.random())

    def __generateMatrix(self, size):
        self.graph2D = [[0] * size for _ in range(size)]

    def createGraph(self, baseInput = 0, config = dict()):
        # Takes an array as input and generates a random graph according to the config
        if config:
            self.config = config
        self.__generateMatrix(self.config["numNodes"])
        self.elementSet = collections.OrderedDict()
        if baseInput in locals():
            self.addElement(baseInput)
        #for i, val in enumerate(baseInput):
        #    self.addElement(i, val)

    def _generateEdges(self, i):
        for key in self.elementSet.keys():
            randomNo = self.generateRandomNumber()
            if randomNo <= self.config["createEdgeThreshold"]:
                # Generate an edge with a random integer weight if lucky
                edgeWeight = math.ceil(self.generateRandomNumber() * self.config["edgeWeightMax"])
                self.graph2D[i][key] = edgeWeight
                self.graph2D[key][i] = edgeWeight

    def _addDecayToElement(self, i):
        bfs_q = queue.SimpleQueue()
        height = 0
        visited = set()
        bfs_q.put([i, height])
        self.elementSet[i]["decayTime"] += self.generateRandomNumber() * (self.config["maxDelayTime"])
        oldDecayTimers = set()
        newDecayTimers = dict()
        while not bfs_q.empty():
            currentElement = bfs_q.get()
            if currentElement[0] in visited:
                continue
            if currentElement[1] > 0:
                oldDecayTimers.add(self.elementSet[currentElement[0]]["decayTime"])
            # If there isn't a decay generated for this element, make a new one, else use the current one
            decayTimer = self.elementSet[currentElement[0]]["decayTime"]
            sumEdgeWeights = sum(self.graph2D[currentElement[0]])
            # decayTime = r + sum(ew) * (1 / e^(distance))
            newTime = decayTimer + math.ceil(sumEdgeWeights * (1 / math.exp(currentElement[1])))
            self.elementSet[currentElement[0]]["decayTime"] = newTime
            visited.add(currentElement[0])
            newDecayTimers[newTime] = currentElement[0]
            for index, elem in enumerate(self.graph2D[currentElement[0]]):
                if elem > 0:
                    bfs_q.put([index, currentElement[1] + 1])
        return (oldDecayTimers, newDecayTimers)

    def _nextIndex(self):
#        if len(self.elementSet) >= self.config["numNodes"]:#
#            return next(iter(self.elementSet))
#        else:
#            return len(self.elementSet)
#            return (next(iter(self.elementSet)) + 1)
        strongest_connected_graph = minStrong(self.graph2D)

        #no connections
        if not strongest_connected_graph:
            if not self.elementSet:
                return 0
            return (next(iter(self.elementSet)) + 1) % self.config['numNodes']

        #smallest index not in the strongest components
        for i in range(self.config['numNodes']):
            if i not in strongest_connected_graph:
                return i;

        #overflow case: oldest element (in element set)
        return next(iter(self.elementSet))

    def addElement(self, value, currentTime = 0):
        index = self._nextIndex()

        self._generateEdges(index)
        self.elementSet[index] = {"value" : value,
                "decayTime" : currentTime}
        oldDecayTimers, newDecayTimers = self._addDecayToElement(index)
        return oldDecayTimers, newDecayTimers

    def deleteElement(self, index):
        for i in range(len(self.graph2D)):
            self.graph2D[i][index] = 0
            self.graph2D[index][i] = 0
            try:
                self.elementSet.pop(index)
            except KeyError:
                continue

    def getGraph(self):
        return self.graph2D

    def getElements(self):
        return self.elementSet

    def recall(self, value):
        strongest_connected_graph = minStrong(self.graph2D)

        #no connections: only remeber last element
        if not strongest_connected_graph:
            if not self.elementSet:
                return False
            if value == self.elementSet[next(reversed(self.elementSet))]:
                return True

        #remeber elements part of strongest connected components
        for index in self.elementSet:
            if(value == self.elementSet[index]['value']):
                return True

        return False

        #remeber elements part of strongest connected components
        for currValue in self.elementSet.values():
            if(value == currValue['value']): #self.elementSet[index]['value']):
                return True



    def __init__(self, config = defaultConfig):
        self.graph2D = None # Stores the adjacency matrix
        self.elementSet = None # Stores data about the elements and their order
        self.config = config # Local config copy

#wm = WorkingMemory(config)
#wm.createGraph(testInput)
#print(wm.getGraph())
#print(wm.getElements())
