GraphExtractor = Extract Graph generate subgraphs based on first level neighbor of the test graph and edges between first level neighbor , it outputs a networkx pickle file

FULL_TRAIN_GRAPH: training graph
TEST_SET: test graph
SPLIT_GRAPH: location of subgraphs to be written

experimentationFeatureExtraction = draw the graph
SPLIT_GRAPH: Location of subgraphs

training_set_feature_split_refactor.py = Generate feature based on the split graphs pickle file. It outputs the feature for both test and training set
SPLIT_GRAPH: Location of subgraphs
TRAIN_SET_WITH_FEATURES: locaation for output of training feature
TEST_SET_WITH_FEATURES: locaation for output of test feature
TEST_SET: Location of test set to be predicted.
Parameter
LIMIT = 2000 (default)
Edit this to increase the number of edges extracted per node

normalization.py = normalize output to increase the ratio of true and false prediction.
FILENAME: output of normalized prediction.
PREDICTION: input for the prediction to be normalized

predictionValidator.py = calculate the ratio of positive (p>=50) and negative (p < 50) in the prediction.
FILENAME: prediction to be analyzed