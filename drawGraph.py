import networkx as nx
import json
import numpy as np
import matplotlib.pyplot as plt

import workingMemory as wm

class DrawGraph:

    def drawMemory(self, label):
        nparr = np.array(self.memory.graph2D)
        G = nx.from_numpy_matrix(nparr)
        pos = nx.circular_layout(G)
        #labels = [json.dumps(x) for x in list(self.memory.elementSet.values())]
        elements = dict(self.memory.elementSet)
        elements.update((x, [y["value"], round(y["decayTime"], 2)]) for x, y in elements.items())
        #G.add_nodes_from(labels)
        nx.draw(G, pos, labels = elements, with_labels = True)
        nx.draw_networkx_nodes(G, pos, node_size = 10000, node_color='powderblue')
        nx.draw_networkx_edge_labels(G, pos, edge_labels = nx.get_edge_attributes(G, 'weight'))
        plt.suptitle("t = " + str(label), fontsize = 14, fontweight = 'bold', x = 1, y = 0, ha = 'right', va = 'bottom')
        plt.axis("off")
        plt.show()

    def updateMemory(self, memory):
        self.memory = memory

    def __init__(self, memoryInstance):
        self.memory = memoryInstance

#memory = wm.WorkingMemory(config)
#memory.createGraph(testInput)
#memory.deleteElement(5)
#dg = DrawGraph(memory)
#dg.drawMemory(0)
