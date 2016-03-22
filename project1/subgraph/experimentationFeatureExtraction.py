import matplotlib.pyplot as plt
import networkx as nx

SPLIT_GRAPH = "data/neighbor_split/split_graph_"

def load_graph(graph_path):
    return nx.read_gpickle(graph_path)



def generateFeatures():
	for i in range(1,2001):
		print "loading graph..."
		dg = load_graph("%s%d" % (SPLIT_GRAPH,i ) )
		nx.draw(dg)
		plt.show
		plt.savefig("graph/path%d.png"%(i))
		plt.clf()

generateFeatures()