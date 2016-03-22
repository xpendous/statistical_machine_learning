
import networkx as nx
import pickle
import csv
import training_set_features

# Generate this file for predict
# The first  column are is edge id. 
# The rest of the columns are features on that edge.

# TEST_GRAPH = 'data/graph.txt'

TEST_SET = 'data/pair_set_test.txt'
TEST_GRAPH = 'data/graph_prop.txt'
TEST_SET_WITH_FEATURES = 'data/test_features.csv'


# get features of true edges
def featureFromEdge():
    features = []
    with open(TEST_SET) as f:
        # escape column head
        next(f)
        for line in f:
            ids = [int(id) for id in line.split("\t")]
            if len(ids) == 3:
                # src<-dest(follower) represent as (src,dest) here
                key = ids[0]
                src = ids[1]
                dest = ids[2]
                features.append(combineFeatures(src, dest, key))
    return features


# combine nodeFeature of src, nodeFeature of dest, and edgeFeatures
def combineFeatures(src, dest, key):
    print src
    print dest
    srcFeatures = training_set_features.getNodeFeature(dg, src, pageranks)
    destFeatures = training_set_features.getNodeFeature(dg, dest, pageranks)
    edgeFeatures = training_set_features.getEdgeFeature(dg, src, dest)
    # save the ith edge feature
    # format:{(src,dest): classfication 0, src features, dest features, edge features}
    return str(key) + '\t' + srcFeatures + '\t' + destFeatures + '\t' + edgeFeatures


def saveFeatures(path_feature, features):
    f = open(path_feature, "w")
    writer = csv.writer(f)
    for row in features:
        writer.writerow([row])
    f.close()


if __name__ == '__main__':
    print "loading proportional or entire graph..."
    dg = pickle.load(open(TEST_GRAPH))

    print "loaded..."

    # feature - PageRank of the nodes
    pageranks = nx.pagerank(dg)

    # TODO - feature - HITS hubs and authorities values for nodes
    # hits = nx.hits(dg)
    print "saving features..."
    saveFeatures(TEST_SET_WITH_FEATURES, featureFromEdge())

