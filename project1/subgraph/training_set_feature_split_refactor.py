import networkx as nx
import pickle
import math
import random
import csv


# Generate this file for training the classifier.
# The first and second column are src and dest. They are not used as features but for checking results
# The 3rd column is classification 0 or 1. e.g 1 if the edge exists, 0 otherwise.
# The rest of the columns are features on that edge.
SPLIT_GRAPH = "data/neighbor_split/split_graph_"
TRAIN_SET_WITH_FEATURES = 'data/train_set_with_features.csv'
TEST_SET_WITH_FEATURES = 'data/test_set_with_features.csv'
TEST_SET = "data/test-public.txt"
banned_edges = []

dg = 0
udg = 0
pageranks = 0
# adar = {}
cluster_coefficients = 0
LIMIT = 2000

def load_graph(graph_path):
    return nx.read_gpickle(graph_path)


def generateFeatures():
    featureTotal = []
    testFeatureTotal = []
    for i in range(1,2001):
        print "loading graph..."
        global dg
        dg = load_graph("%s%d" % (SPLIT_GRAPH,i ) )
        global udg
        udg = dg.to_undirected()
        # feature - PageRank of the nodes
        print "loaded..."
        global pageranks
        pageranks = nx.pagerank(dg)
        global cluster_coefficients
        cluster_coefficients = nx.clustering(udg)

        # adar = {}
        # adar_iter = nx.adamic_adar_index(udg, udg.edges())
        # for s,d,k in adar_iter:
        #     print "asdf"
        #     adar[(int(s),int(d))] = k
        #     adar[(int(d),int(s))] = k
        # print adar


        # TODO - feature - HITS hubs and authorities values for nodes
        # hits = nx.hits(dg)

        featuresTrue = featureFromTrueEdge(LIMIT)
        print "feature true done"
        featuresFalse = featureFromFalseEdge(LIMIT)
        featureTotal.append(featuresTrue)
        featureTotal.append(featuresFalse)

        current_train_src,current_train_dst = banned_edges[i-1]
        testFeatureTotal.append( combineFeaturesForTestSet(current_train_src,current_train_dst,i) )
        print "%d iteration" % (i)
        #print featureTotal
    saveFeatures(TRAIN_SET_WITH_FEATURES, featureTotal)
    saveFeaturesTest(TEST_SET_WITH_FEATURES,testFeatureTotal)


# get features of true edges
def featureFromTrueEdge(limit):
    features = []
    edges_per_node_limit = max(5,int( limit / len(dg.nodes()) ))
    total = 0
    for src in dg.nodes():
        i = 0
        if (total >= limit):
            break
        for dest in dg.neighbors(src):
            if (total >= limit) or (i >= edges_per_node_limit):
                break
            features.append(combineFeatures(src, dest, 1))
            i += 1
            total += 1
    return features



# get features of false edges
# input n: the  number of false edge should be same as the real one
def featureFromFalseEdge(n):
    features = []
    sampled_l = []
    nodes = dg.nodes()
    total = 0
    edges_per_node_limit = max(5,int(n / len(dg.nodes())))
    #-1 for the formula -1 for the hidden edge
    total_possible_combination = len(dg.nodes()) * (len(dg.nodes()) - 2)
    print "%d possible comb "% (total_possible_combination)

    #print "%d %dedges so far "% (len(sampled_l),len(dg.edges()))
    # if len(sampled_l) + len(dg.edges()) == total_possible_combination:
    #     break
    for src in nodes:
        i = 0
        if (total >= n):
            break
        for dest in nodes:
            if ( (src != dest) and (dg.has_edge(src, dest) != True) and ( (int(src),int(dest)) not in banned_edges ) and (int(src),int(dest)) not in sampled_l):
                sampled_l.append( (src,dest) )
                i += 1
                total += 1
                #print i
            elif (total >= n) or (i >= edges_per_node_limit):
                break

    for edge in sampled_l:
        features.append(combineFeatures(edge[0], edge[1], 0))
        
        #print i
        
    return features




# combine nodeFeature of src, nodeFeature of dest, and edgeFeatures
# main code to add or reduce feature
def combineFeatures(src, dest, isTrueEdge):
    srcFeatures = getNodeFeature(src, pageranks, cluster_coefficients)
    destFeatures = getNodeFeature(dest, pageranks, cluster_coefficients)
    edgeFeatures = getEdgeFeature(src, dest)
    # save the ith edge feature
    # format:{(src,dest): classfication 0, src features, dest features, edge features}
    return str(src) + '\t' + str(dest) + '\t' + str(
        isTrueEdge) + '\t' + srcFeatures + '\t' + destFeatures + '\t' + edgeFeatures

# combine nodeFeature of src, nodeFeature of dest, and edgeFeatures
def combineFeaturesForTestSet(src, dest, key):
    srcFeatures = getNodeFeature(src, pageranks, cluster_coefficients)
    destFeatures = getNodeFeature(dest, pageranks, cluster_coefficients)
    edgeFeatures = getEdgeFeature(src, dest)
    # save the ith edge feature
    # format:{(src,dest): classfication 0, src features, dest features, edge features}
    return str(key) + '\t' + srcFeatures + '\t' + destFeatures + '\t' + edgeFeatures    


# get feature of node
def getNodeFeature(node, pageranks, cluster_coefficients):
    # feature - number of followers
    in_degree = dg.in_degree(node)
    # feature - number of followees
    out_degree = dg.out_degree(node)
    # feature - ratio
    ratio = math.log(1 + (1 + in_degree / (1 + out_degree)))
    # feature - clustering coefficients

    return '\t'.join([str(item) for item in [in_degree, out_degree, ratio, pageranks.get(node), cluster_coefficients[node]]])


# get feature of edge
def getEdgeFeature(src, dest):
    # get similarity by two nodes' follower sets
    src_followers = getFollowers(src)
    dest_followers = getFollowers(dest)

    # get similarity by two nodes' followee sets
    src_followees = getFollowees(src)
    dest_followees = getFollowees(dest)

    srcNeighbor = src_followers + src_followees
    destNeighbor = dest_followers + dest_followees
    simNeighbor = getSimilarity(srcNeighbor, destNeighbor)



    
    one_NN = one_neighbour_source_dest(src_followees,dest_followers)
    #out out #in
    # first_level_folowee = []
    # for first_level in src_followees:
    #     if first_level in dest_followers:
    #         first_level_folowee.append(first_level)
    # two_NN = two_neighbour_source_dest(src_followees,first_level_folowee ,dest_followers)
    # #out out out in
    # first_level_foloweex = []

    # for first_level in src_followees:
    #     first_level_foloweex.append(first_level)  

    # second_level_foloweex = []
    # final_first = []
    # for first_level in first_level_foloweex:
    #     for folowee in getFollowees(first_level):
    #         if folowee in dest_followers:
    #             final_first.append(first_level)
    #             second_level_foloweex.append(folowee)
 


              
    # three_NN = three_neighbour_source_dest(src_followees,final_first, second_level_foloweex ,dest_followers)


    return '\t'.join( [str(item) for item in [simNeighbor[0], simNeighbor[1],simNeighbor[2],simNeighbor[3] , one_NN] ] ) 


def getSimilarity(src, dest):
    # feature - Jaccard similarity by two nodes' follower sets
    jaccard = jaccard_similarity(src, dest)
    # feature - cosine similarity by two nodes' follower sets
    cosine = cosine_similarity(src, dest)
    common_neighbors = common_neighbours(src,dest)
    p_a = preferential_attachment(src,dest)

    return [jaccard, cosine,common_neighbors,p_a]


# 1: (src, dest) edge; 0: not
# src is A, dest(follower) is B given A<-B
def getClassification(src, dest):
    dg.has_edge(src, dest)


def getFollowers(node):
    # followers of node n
    in_edges = dg.in_edges(node)
    # nodes of followers
    return [in_edge[0] for in_edge in in_edges]


def getFollowees(node):
    out_edges = dg.out_edges(node)
    # nodes of followees
    return [out_edge[1] for out_edge in out_edges]


# Jaccard similarity by compare two nodes' follower/followee sets
def jaccard_similarity(set1, set2):
    if len(set1) == 0 and len(set2) == 0:
        return 0
    return len(set(set1) & set(set2)) / len( set(set1) | set(set2) ) 

def preferential_attachment(set1,set2):
    return len(set1)*len(set2)

# input: e.g. set: [12,3,4]
def cosine_similarity(set1, set2):
    if len(set1) == 0 and len(set2) == 0:
        return 0
    return len(set(set1) & set(set2)) / len( set(set1) ) * len ( set(set2) )

def common_neighbours(set1,set2):
    if len(set1) ==0 and len(set2) ==0:
        return 0
    return len( set(set1) & set(set2) )


def one_neighbour_source_dest(src_out,dst_in):
    return w_i(src_out) * w_i(dst_in)

def two_neighbour_source_dest(src_out,dst_out,dst_in):
    return w_i(src_out) * w_i(dst_out) * w_i(dst_in)

def three_neighbour_source_dest(src_out,dst_out,dst_out_2,dst_in):
    return w_i(src_out) * w_i(dst_out) * w_i(dst_in) * w_i(dst_out_2)

#kNN weighting of one edge, more connection less weight like a celebrity 
#input list of the neighbour can be in or out
#helper function
def w_i(neighbour_node_l):
    if len(neighbour_node_l) == 0:
        return 1
    return 1/math.sqrt( 1 + ( len(neighbour_node_l) ) )



def square_rooted(x):
    return round(math.sqrt(sum([a * a for a in x])), 3)


def saveFeaturesTest(path_feature, features):
    f = open(path_feature, "w")
    writer = csv.writer(f)
    for row in features:
        writer.writerow([row])
    f.close()

def saveFeatures(path_feature,features):
    f = open(path_feature, "w")
    writer = csv.writer(f)
    for i in range(0,len(features)):
        for row in features[i]:
                writer.writerow([row])
    f.close()

############################
# make sure the test set edges is not considered as negative
def store_banned_edges():
    with open(TEST_SET) as f:
        # escape column head
        next(f)
        for line in f:
            ids = [int(id) for id in line.split("\t")]
            if len(ids) == 3:
                # src<-dest(follower) represent as (src,dest) here
                src = ids[1]
                dest = ids[2]
                banned_edges.append((int(src),int(dest)))

if __name__ == '__main__':
    print "storing banned edges"
    store_banned_edges()
    print "generating features..."
    generateFeatures()

