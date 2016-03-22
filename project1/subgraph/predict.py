from sklearn.ensemble import RandomForestClassifier
from sklearn import cross_validation
from sklearn.metrics import accuracy_score
from numpy import genfromtxt, savetxt
import numpy as np


PREDICTION = 'data/prediction-2000-debug.csv'
CPU_CORE = 2
TRAIN_SET_WITH_FEATURES = 'data/train_set_with_features.csv'
TEST_SET_WITH_FEATURES = 'data/test_set_with_features.csv'


# TRAIN_SET_WITH_FEATURES = 'data/train_set_with_features.csv'
# TEST_SET_WITH_FEATURES = 'data/test_set_with_features.csv'

# STEP 1: Read in the training examples.
def readTrainingFeature():
    # A classfication is 1 (for a known true edge) or 0 (for a false edge).
    classifications = [] 
    # Each training example is an array of features.
    training_features = [] 
    for line in open(TRAIN_SET_WITH_FEATURES):
        fields = [float(x) for x in line.split('\t')]
        classification = fields[2]
        feature = fields[3:]

        classifications.append(classification)  
        training_features.append(feature)
    return [classifications,training_features]


# STEP 2: Train a classifier.
def trainModel(classifications,training_features):
    # n_estimators: The number of trees in the forest
    clf = RandomForestClassifier(n_estimators = 500, oob_score = True, n_jobs=CPU_CORE)
    clf = clf.fit(training_features, classifications)
    return clf



def kFold(classifications,training_features):
    print len(training_features)
    clf = RandomForestClassifier(n_estimators = 500, oob_score = True, n_jobs=CPU_CORE)
    # K-Fold cross validation. 10 folds.
    cv = cross_validation.KFold(len(training_features), n_folds=10)#, indices=False)
    scores = cross_validation.cross_val_score(clf, training_features, classifications, cv=10)
    print scores


# TODO - REMOVE
def kFold0(classifications,training_features):
    print len(training_features)
    clf = RandomForestClassifier(n_estimators = 500, oob_score = True, n_jobs=CPU_CORE)
    # K-Fold cross validation. 10 folds.
    cv = cross_validation.KFold(len(training_features), n_folds=10)#, indices=False)

    target = np.array(classifications)# [x for x in classifications])
    train = np.array( training_features)#[x for x in training_features])
    scores = cross_validation.cross_val_score(clf, training_features, classifications, cv=10)


    #iterate through the training and test cross validation segments and
    #run the classifier on each one, aggregating the results into a list
    results = []
    for traincv, testcv in cv:
        #print 'ffffffff'
        #print traincv
        probas = clf.fit(train[traincv], target[traincv]).predict_proba(train[testcv])
        #print probas

        print accuracy_score(train[testcv],probas)
        results.append([x[1] for x in probas])
    #print results

    # get the mean of the cross-validated results
    #mean =  str( np.array(results).mean() )

    mean = np.array(results).mean()
    print mean
    #return mean




# STEP 3: Predict
# Score the candidates.
def predict(clf):
    BATCH_SIZE = 100
    ids = []
    examples = []
    predictions = []
    for line in open(TEST_SET_WITH_FEATURES):
        fields = [float(feature) for feature in line.split("\t")]
        ids.append(fields[0])
        example_features = fields[1:]
        examples.append(example_features)


    
    print '##########'
    predictions = clf.predict_proba(examples) 

    predict_file = open(PREDICTION,"w") 
    print >> predict_file, "Id,Prediction"
    for i in xrange(len(predictions)):
        #print ",".join([str(x) for x in [int(ids[i]), predictions[i][1]]])
        predicted_probs = [str(x) for x in [int(ids[i]), predictions[i][1]]]

        print >> predict_file, ",".join([str(x) for x in [int(ids[i]), predictions[i][1]]])



#trains = []
#trains = readTrainingFeature()
#kFold(trains[0],trains[1])

#TODO - add later
trains = []
trains = readTrainingFeature()
clf = trainModel(trains[0],trains[1])
predict(clf)
