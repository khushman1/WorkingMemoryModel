import calendar
import time
import random
import collections
import math
import queue

class WorkingMemory:

    def generateRandomNumber(self):
        return float(random.random())

    def createGraph(self, graphInput):
        # Takes an array as input and generates a random graph according to the config
        self.graph2D = [[0]*len(graphInput) for _ in range(len(graphInput))]
        self.elementSet = collections.OrderedDict()
        for i, val in enumerate(graphInput):
            self.addElement(i, val)

    def _generateEdges(self, i):
        for key in self.elementSet.keys():
            if self.generateRandomNumber() <= self.config["createEdgeThreshold"]:
                # Generate an edge with a random integer weight if lucky
                edgeWeight = math.floor(self.generateRandomNumber() * self.config["edgeWeightMax"])
                self.graph2D[i][key] = edgeWeight
                self.graph2D[key][i] = edgeWeight

    def _addDecayToElement(self, i):
        bfs_q = queue.SimpleQueue()
        height = 0
        visited = set()
        bfs_q.put([i, height])
        while not bfs_q.empty():
            currentElement = bfs_q.get()
            if currentElement[0] in visited:
                continue
            # If there isn't a decay generated for this element, make a new one, else use the current one
            decayTimer = self.generateRandomNumber() * self.config["maxDelayTime"] if self.elementSet[currentElement[0]]["decayTime"] == 0 else self.elementSet[currentElement[0]]["decayTime"]
            sumEdgeWeights = sum(self.graph2D[currentElement[0]])
            # decayTime = r + sum(ew) * (1 / e^(distance))
            self.elementSet[currentElement[0]]["decayTime"] = (decayTimer + sumEdgeWeights * (1 / math.exp(currentElement[1])))
            visited.add(currentElement[0])
            for index, elem in enumerate(self.graph2D[currentElement[0]]):
                if elem > 0:
                    bfs_q.put([index, currentElement[1] + 1])
        return

    def addElement(self, index, value):
        self._generateEdges(index)
        self.elementSet[index] = {"value" : value,
                "decayTime" : 0}
        self._addDecayToElement(index)


    def getGraph(self):
        return self.graph2D

    def getElements(self):
        return self.elementSet

    def __init__(self, config):
        self.graph2D = None # Stores the adjacency matrix
        self.elementSet = None # Stores data about the elements and their order
        self.config = config # Local config copy
        

graphInput = [1,2,3,4,5,6,7]

config = {"numNodes" : 7,
        "maxDelayTime" : 1000,
        "createEdgeThreshold" : 0.5,
        "edgeWeightMax" : 10}

wm = WorkingMemory(config)
wm.createGraph(graphInput)
print(wm.getGraph())
print(wm.getElements())
