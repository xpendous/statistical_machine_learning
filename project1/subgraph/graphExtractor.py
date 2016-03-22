__author__ = 'viva'

import networkx as nx
import pickle
import math

FULL_TRAIN_GRAPH = "data/train_graph_full.txt"
TEST_SET = "data/test-public.txt"
SPLIT_GRAPH = "data/neighbor_split/split_graph_"


l_test_edges = []

def load_graph(graph_path):
    return nx.read_gpickle(graph_path)

def split_graph():
	i = 0
	for src,dest in l_test_edges:
		i += 1
		tmp_graph = nx.DiGraph()
		print i
		add_neighbors(tmp_graph,src)
		add_neighbors(tmp_graph,dest)
		nx.write_gpickle(tmp_graph,"%s%d" % (SPLIT_GRAPH,i ) )



#add the first level neighbor and the edges between them
def add_neighbors(tmp_graph,src):
	for node in g.neighbors(src):
		#add the first level neighbor
		tmp_graph.add_edge(src,node)
		#add the edges between them
		for neighbors_of_node in g.neighbors(node):
			if ( (neighbors_of_node in g.neighbors(src) ) or (neighbors_of_node == src) ):
				tmp_graph.add_edge(node,neighbors_of_node)





# get features of true edges
def load_edge_from_test():
	with open(TEST_SET) as f:
		# escape column head
		next(f)
		for line in f:
			ids = [int(id) for id in line.split("\t")]
			if len(ids) == 3:
				# src<-dest(follower) represent as (src,dest) here
				src = ids[1]
				dest = ids[2]
				l_test_edges.append((int(src),int(dest)))

g = load_graph(FULL_TRAIN_GRAPH)
load_edge_from_test()
split_graph()