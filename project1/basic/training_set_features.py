
import networkx as nx
import pickle
import math
import random
import csv


# Generate this file for training the classifier.
# The first and second column are src and dest. They are not used as features but for checking results
# The 3rd column is classification 0 or 1. e.g 1 if the edge exists, 0 otherwise.
# The rest of the columns are features on that edge.
TRAIN_SET = 'data/pair_set_train.txt'
TRAIN_GRAPH = 'data/graph_train.txt'
TRAIN_SET_WITH_FEATURES = 'data/train_features.csv'


def loadGraph():
    return pickle.load(open(TRAIN_GRAPH))


def generateFeatures():
    featureTotal = []
    featuresTrue = featureFromTrueEdge()
    featuresFalse = featureFromFalseEdge(len(featuresTrue))
    featureTotal.append(featuresTrue)
    featureTotal.append(featuresFalse)
    saveFeatures(TRAIN_SET_WITH_FEATURES, featureTotal)


# get features of true edges
def featureFromTrueEdge():
    features = []
    with open(TRAIN_SET) as f:
        for line in f:
            ids = [int(id) for id in line.split("\t")]
            if len(ids) == 2:
                # src<-dest(follower) represent as (src,dest) here
                src = ids[0]
                dest = ids[1]
                features.append(combineFeatures(src, dest, 1))
    return features


# get features of false edges
# input n: the  number of false edge should be same as the real one
def featureFromFalseEdge(n):
    features = []
    nodes = dg.nodes()
    i = 0
    while i < n:
        edge = generateFalseEdge(nodes)
        features.append(combineFeatures(edge[0], edge[1], 0))
        i += 1
    return features


# combine nodeFeature of src, nodeFeature of dest, and edgeFeatures
def combineFeatures(src, dest, isTrueEdge):
    srcFeatures = getNodeFeature(dg, src, pageranks)
    destFeatures = getNodeFeature(dg, dest, pageranks)
    edgeFeatures = getEdgeFeature(dg, src, dest)
    # save the ith edge feature
    # format:{(src,dest): classfication 0, src features, dest features, edge features}
    return str(src) + '\t' + str(dest) + '\t' + str(
        isTrueEdge) + '\t' + srcFeatures + '\t' + destFeatures + '\t' + edgeFeatures


# get feature of node
def getNodeFeature(dg, node, pageranks):
    # feature - number of followers
    in_degree = dg.in_degree(node)
    # feature - number of followees
    out_degree = dg.out_degree(node)
    # feature - ratio
    ratio = math.log(1 + (1 + in_degree / (1 + out_degree)))
    # feature - clustering coefficients
    return '\t'.join([str(item) for item in [in_degree, out_degree, ratio, pageranks.get(node)]])


# get feature of edge
def getEdgeFeature(dg, src, dest):
    # get similarity by two nodes' follower sets
    src_followers = getFollowers(dg, src)
    dest_followers = getFollowers(dg, dest)
    simFollower = getSimilarity(src_followers, dest_followers)
    # get similarity by two nodes' followee sets
    src_followees = getFollowees(dg, src)
    dest_followees = getFollowees(dg, dest)
    simFollowee = getSimilarity(src_followees, dest_followees)

    return '\t'.join([str(item) for item in [simFollower[0], simFollower[1], simFollowee[0], simFollowee[1]]])


def getSimilarity(src, dest):
    # feature - Jaccard similarity by two nodes' follower sets
    jaccard = jaccard_similarity(src, dest)
    # feature - cosine similarity by two nodes' follower sets
    cosine = cosine_similarity(src, dest)
    return [jaccard, cosine]


# Randomly pick up two  nodes which cannot constructs edge(src, dest)
def generateFalseEdge(nodes):
    while True:
        src = random.choice(nodes)
        dest = random.choice(nodes)
        if (src != dest) and (dg.has_edge(src, dest) != True):
            break
    return [src, dest]

# 1: (src, dest) edge; 0: not
# src is A, dest(follower) is B given A<-B
def getClassification(src, dest):
    dg.has_edge(src, dest)


def getFollowers(dg, node):
    # followers of node n
    in_edges = dg.in_edges(node)
    # nodes of followers
    return [in_edge[0] for in_edge in in_edges]


def getFollowees(dg, node):
    out_edges = dg.out_edges(node)
    # nodes of followees
    return [out_edge[1] for out_edge in out_edges]


# Jaccard similarity by compare two nodes' follower/followee sets
def jaccard_similarity(set1, set2):
    if len(set1) == 0 and len(set2) == 0:
        return 0
    return len(set(set1) & set(set2)) / len(set(set1) | set(set2))


# input: e.g. set: [12,3,4]
def cosine_similarity(set1, set2):
    if len(set1) == 0 or len(set2) == 0:
        return 0
    numerator = sum(a * b for a, b in zip(set1, set2))
    denominator = square_rooted(set1) * square_rooted(set2)
    return round(numerator / float(denominator), 3)


def square_rooted(x):
    return round(math.sqrt(sum([a * a for a in x])), 3)


def saveFeatures(path_feature, features):
    f = open(path_feature, "w")
    writer = csv.writer(f)
    for i in range(2):
        for row in features[i]:
            writer.writerow([row])
    f.close()


if __name__ == '__main__':
    print "loading graph..."
    dg = loadGraph()
    # feature - PageRank of the nodes
    print "loaded..."
    pageranks = nx.pagerank(dg)
    # TODO - feature - HITS hubs and authorities values for nodes
    # hits = nx.hits(dg)
    print "generating features..."
    generateFeatures()

