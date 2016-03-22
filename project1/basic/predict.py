

from sklearn.ensemble import RandomForestClassifier
import sys

# TEST_SET_WITH_FEATURES = test_set_features.TEST_SET_WITH_FEATURES

TEST_SET_WITH_FEATURES = 'data/test_features.csv'
TRAIN_SET_WITH_FEATURES = 'data/train_features.csv'
PREDICTIONS = 'data/predict.csv'


# STEP 1: Read in the training examples.
def readTrainingFeature():
    # A classfication is 1 (for a known true edge) or 0 (for a false edge).
    classifications = []
    # Each training example is an array of features.
    training_features = []
    print "reading features..."
    for line in open(TRAIN_SET_WITH_FEATURES):
        fields = [float(x) for x in line.split('\t')]
        classification = fields[2]
        feature = fields[3:]

        classifications.append(classification)
        training_features.append(feature)
    return [classifications, training_features]


# STEP 2: Train a classifier.
def trainModel(classifications, training_set_features):
    # n_estimators: The number of trees in the forest
    print "training model..."
    clf = RandomForestClassifier(n_estimators=100, oob_score=True)
    clf = clf.fit(training_set_features, classifications)
    return clf


# STEP 3: Predict
# Score the candidates.
def predict(clf):
    ids = []
    examples = []
    print "predicting..."
    for line in open(TEST_SET_WITH_FEATURES):
        fields = [float(feature) for feature in line.split("\t")]
        ids.append(fields[0])
        example_features = fields[1:]
        examples.append(example_features)
    print 'predictions to file...'
    predictions = clf.predict_proba(examples)
    predict = open(PREDICTIONS, "w")
    print >> predict, ",".join(["ID", "Prediction"])
    for i in xrange(len(predictions)):
        print >> predict, ",".join([str(x) for x in [int(ids[i]), predictions[i][1]]])


clf = trainModel(readTrainingFeature()[0], readTrainingFeature()[1])
predict(clf)
