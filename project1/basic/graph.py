
import networkx as nx
import pickle

TRAIN_SET = 'data/pair_set_train.txt'
PROPORTION_SET = 'data/pair_set_proportion.txt'
TRAIN_GRAPH = 'data/graph_train.txt'
PROPORTION_GRAPH = 'data/graph_prop.txt'



# construct the entire graph 
# This graph will be used to get features for training/validation/test set



def constructTrainGraph():
    line_num = 0
    g = nx.DiGraph()
    with open(TRAIN_SET) as f:
        for line in f:
            line_num += 1
            ids = [int(id) for id in line.split("\t")]
            # src<-dest(follower) represent as (src,dest) here
            g.add_edge(ids[0], ids[1])
            print line_num
    # save the graph
    pickle.dump(g, open(TRAIN_GRAPH, "w"))


def constructProportionGraph():

    line_num = 0
    g = nx.DiGraph()
    with open(PROPORTION_SET) as f:
        for line in f:
            line_num += 1
            ids = [int(id) for id in line.split("\t")]
            # src<-dest(follower) represent as (src,dest) here
            g.add_edge(ids[0], ids[1])
            print line_num
    # save the graph
    pickle.dump(g, open(PROPORTION_GRAPH, "w"))


if __name__ == '__main__':  
    constructTrainGraph()
    constructProportionGraph()
