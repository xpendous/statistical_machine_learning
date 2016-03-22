import pickle
from sklearn import metrics
from sklearn.feature_selection import VarianceThreshold
from sklearn.decomposition import RandomizedPCA
from sklearn import preprocessing
from sklearn import manifold
import unicodedata
import csv
import matplotlib.pyplot as plt

# education
# category = 'socio_demographic'
# suburb1 = 'Malvern'
# suburb2 = 'Waterways'
top_industry = 'Top industry'
second_industry = '2nd top industry - persons'
third_industry = '3rd top industry - persons'
top_occup = 'Top occupation'
secont_occup = '2nd top occupation - persons'
third_occup = '3rd top occupation - persons'


def load():
    f = open('socio_demographic', 'rb')
    dg = pickle.load(f)
    f.close()
    return dg


def load_all():
    f = open('feature_all', 'rb')
    dg = pickle.load(f)
    f.close()
    return dg


def get_demographic():
    return load()


def get_all_feature():
    return load_all()


# generate feature matrix after feature selection, creation and normalisation 
# return: maxtir 
# format: [[observation 1's feature vector],[observation 2's feature vector],...]
def generate_normalized_matrix(dg):
    dicts = generate_feature_ids(dg)
    matrix = []
    for key, value in dg.iteritems():
        #################
        # feature selection
        #################
        # feature set 0: baseline - use full feature
        dg_by_suburb = set_feature_id(dg[key], dicts)
        # feature set 2: feature selection
        new_feature_set = feature_selection(dg_by_suburb)
        # feature set 3: MDS
        feature_vec_suburb = generate_feature_vector_by_dict(new_feature_set)
        matrix.append(feature_vec_suburb)
    # remove low variance
    X = feature_remove_low_variance(matrix)
    # save feature csv
    write_csv(X)

    # data normalisation
    return get_normaisation(X)


# parameter: 
# X: normalized feature matrix
# return: {suburb1:[feature vec], suburb2:[feature vec],...}
def generate_matrix_with_surburb(dg, X):
    X_with_suburb = dict()
    i = 0
    for key, value in dg.iteritems():
        X_with_suburb[key] = X[i]
        i += 1
    return X_with_suburb


# 15:29
# generate pca features
def generate_feature_by_suburb(suburb):
    # dg_suburb_dict = dict()
    feature_vector = dict()
    dg = load()
    dicts = generate_feature_ids(dg)
    # set feature id for industry and occupation
    for key, value in dg.iteritems():
        feature_vector[key] = generate_feature_vector_by_dict(set_feature_id(value, dicts))

    # select_feature_1(feature_vector.values())
    # parameter: feature set for all suburbs
    new_features = select_feature_2(feature_vector.values())
    # add suburb names back to new feature list of list
    i = 0
    for key, value in feature_vector.iteritems():
        feature_vector[key] = new_features[i]
        i += 1

    feature_suburb1 = generate_feature_vector_by_list(feature_vector[suburb1])
    feature_suburb2 = generate_feature_vector_by_list(feature_vector[suburb2])

    return [feature_suburb1, feature_suburb2]


# generate pca features
def generate_feature_2_by_suburb(suburb1, suburb2):
    # dg_suburb_dict = dict()
    feature_vector = dict()
    dg = load()
    # set feature id list
    dicts = generate_feature_ids(dg)
    # set feature id for industry and occupation
    for key, value in dg.iteritems():
        feature_vector[key] = generate_feature_vector_by_dict(set_feature_id(value, dicts))

    # select_feature_1(feature_vector.values())
    # parameter: feature set for all suburbs
    new_features = select_feature_2(feature_vector.values())
    # add suburb names back to new feature list of list
    i = 0
    for key, value in feature_vector.iteritems():
        feature_vector[key] = new_features[i]
        i += 1

    feature_suburb1 = generate_feature_vector_by_list(feature_vector[suburb1])
    feature_suburb2 = generate_feature_vector_by_list(feature_vector[suburb2])

    return [feature_suburb1, feature_suburb2]


# assgin id to each industry and occupation: 
# e.g.['Professional, Scientific and Technical Services','Health Care and Social Assistance','Retail Trade'...]=[0,1,2,3...]
def generate_feature_ids(dg):
    industry_dict = dict()
    occupation_dict = dict()
    for key, value in dg.iteritems():
        append_dict(industry_dict, value[top_industry])
        append_dict(industry_dict, value[second_industry])
        append_dict(industry_dict, value[third_industry])
        append_dict(occupation_dict, value[top_occup])
        append_dict(occupation_dict, value[secont_occup])
        append_dict(occupation_dict, value[third_occup])

    return [industry_dict, occupation_dict]


# assgin id(value) to industry or occupation(key) only if it's not existed in the dict 
def append_dict(mydict, key):
    if mydict.has_key(key) is False:
        mydict[key] = len(mydict)
    return mydict


# set feature id by suburb
def set_feature_id(dg_suburb, dicts):
    industry_dict = dicts[0]
    occupation_dict = dicts[1]
    dg_suburb[top_industry] = industry_dict[dg_suburb[top_industry]]
    dg_suburb[second_industry] = industry_dict[dg_suburb[second_industry]]
    dg_suburb[third_industry] = industry_dict[dg_suburb[third_industry]]
    dg_suburb[top_occup] = occupation_dict[dg_suburb[top_occup]]
    dg_suburb[secont_occup] = occupation_dict[dg_suburb[secont_occup]]
    dg_suburb[third_occup] = occupation_dict[dg_suburb[third_occup]]

    return dg_suburb


def generate_feature_vector_by_dict(dg_suburb):
    feature = []
    for key, value in dg_suburb.iteritems():
        feature.append(digitalize_feature(value))
    return feature


def generate_feature_vector_by_list(features):
    feature = []
    for value in features:
        feature.append(digitalize_feature(value))
    return feature


def digitalize_feature(value):
    value = str(value)
    if value is None or value == 'n/a':
        value = 0.0
    # average the value with '<n' to n/2
    elif '<' in value:
        value = (float(value[1:])) / 2
    return float(value)


def get_eucld_sim(feature_suburb1, feature_suburb2):
    return metrics.pairwise.pairwise_distances(feature_suburb1, feature_suburb2, metric='euclidean')[0][0]


def get_cosine_sim(feature_suburb1, feature_suburb2):
    return 1 - metrics.pairwise.pairwise_distances(feature_suburb1, feature_suburb2, metric='cosine')[0][0]


# Removing features with low variance
# removes all zero-variance features which have the same value in all samples.
def feature_remove_low_variance(full_features):
    sel = VarianceThreshold(threshold=0)  # 2.1)
    X = sel.fit_transform(full_features)
    # matrix_with_surburb = generate_matrix_with_surburb(dg,X)
    # return matrix_with_surburb
    return X


# remove Top/2nd top/3rd top industry/occupation with propotion
def feature_selection(dg_by_suburb):
    population = dg_by_suburb['Number of Households'] * dg_by_suburb['Average persons per household']
    all = load_all
    #########
    # pearson correlation: highest, 0.52689533987229908
    #########
    del dg_by_suburb['Number of Households']
    del dg_by_suburb['Top industry, %']
    del dg_by_suburb['2nd top industry, %']
    del dg_by_suburb['3rd top industry, %']
    del dg_by_suburb['Top occupation, %']
    del dg_by_suburb['2nd top occupation, %']
    del dg_by_suburb['3rd top occupation, %']
    del dg_by_suburb['Occupied private dwellings']
    del dg_by_suburb['Population in non-private dwellings']
    del dg_by_suburb['Public Housing Dwellings']
    del dg_by_suburb['Dwellings with no motor vehicle']
    del dg_by_suburb['Dwellings with no internet']
    del dg_by_suburb['Equivalent household income <$600/week']
    #
    del dg_by_suburb['Requires assistance with core activities, %']
    del dg_by_suburb['% dwellings which are public housing']
    del dg_by_suburb['Personal income <$400/week, persons']
    del dg_by_suburb['Personal income <$400/week, %']
    del dg_by_suburb['Female-headed lone parent families']
    del dg_by_suburb['Male-headed lone parent families']
    del dg_by_suburb['Holds degree or higher, persons']
    del dg_by_suburb['Did not complete year 12, persons']
    del dg_by_suburb['Unemployed, persons']
    del dg_by_suburb['Volunteers, persons']
    del dg_by_suburb['Requires assistance with core activities, persons']
    del dg_by_suburb['Aged 75+ and lives alone, persons']
    del dg_by_suburb['Unpaid carer to person with disability, persons']
    del dg_by_suburb['Unpaid carer of children, persons']
    del dg_by_suburb['IRSD (min)']
    del dg_by_suburb['IRSD (max)']
    del dg_by_suburb['Unemployed, %']
    del dg_by_suburb['Unpaid carer of children, %']
    # del dg_by_suburb['Holds degree or higher, %']
    # del dg_by_suburb['Did not complete year 12, %']
    # del dg_by_suburb['% residing near PT']
    # del dg_by_suburb['Dwellings with no internet, %']
    # del dg_by_suburb['Female-headed lone parent families, %']
    #########
    # end
    #########


    '''
    del dg_by_suburb['Top industry']
    del dg_by_suburb['2nd top industry - persons']
    del dg_by_suburb['3rd top industry - persons']
    del dg_by_suburb['Top occupation']
    del dg_by_suburb['2nd top occupation - persons']
    del dg_by_suburb['3rd top occupation - persons']
    del dg_by_suburb['Occupied private dwellings, %']
    dg_by_suburb['Number of families, %'] = dg_by_suburb['Number of families'] / population
    del dg_by_suburb['Number of families']
    dg_by_suburb['Primary school students, %'] = dg_by_suburb['Primary school students'] / population
    del dg_by_suburb['Primary school students']
    dg_by_suburb['Secondary school students, %'] = dg_by_suburb['Secondary school students'] / population
    del dg_by_suburb['Secondary school students']
    dg_by_suburb['TAFE students, %'] = digitalize_feature(dg_by_suburb['TAFE students']) / population
    del dg_by_suburb['TAFE students']
    dg_by_suburb['University students, %'] = digitalize_feature(dg_by_suburb['University students']) / population
    del dg_by_suburb['University students']'''

    '''
    dg_by_suburb[', %'] = dg_by_suburb[''] / population
    del dg_by_suburb['']
    dg_by_suburb[', %'] = dg_by_suburb[''] / population
    del dg_by_suburb['']
    del dg_by_suburb['']
    del dg_by_suburb['']
    '''


    # print len(dg_by_suburb)
    return dg_by_suburb


# PCA
def feature_reduction_pca(full_features):
    pca = RandomizedPCA(n_components=8, whiten=True).fit(full_features)
    return pca.transform(full_features)


# non-metric MDS
def feature_reduction_2(X):
    nmds = manifold.MDS(n_components=4, metric=False, dissimilarity="euclidean")
    return nmds.fit_transform(X)


# get cosine similarity
def get_proximity(suburb1, suburb2):
    dg = get_demographic()
    # dg = get_all_feature()
    # feature selelction and feature normalisation
    X = generate_normalized_matrix(dg)
    # feature reduction
    X = feature_reduction_pca(X)
    # A2: dimension reduction
    # todo: unnote. This is A2
    #feature_reduction(dg, X)

    X_with_suburb = generate_matrix_with_surburb(dg, X)

    feature_suburbs = [X_with_suburb[suburb1], X_with_suburb[suburb2]]

    #################
    # change proximity to get different similarity/disimlarity measures
    #################
    # cosine similarity
    # return get_cosine_sim(feature_suburbs[0],feature_suburbs[1])
    # euclidean distance
    return get_eucld_sim(feature_suburbs[0], feature_suburbs[1])


# TODO
# use different similarity/dismilarity

# input: matrix(list of list) of feature set
# format: [[observation 1's feature vector],[observation 2's feature vector],...]
# return: normalized matrix
def get_normaisation(X):
    # a=preprocessing.MinMaxScaler()
    # return a.fit_transform(X)

    return preprocessing.scale(X)


# MDS plot
def feature_reduction(dg, X):
    # mds = manifold.MDS(n_components=2, dissimilarity='euclidean')
    # return mds.fit_transform(X)

    suburbs = []
    for key, value in dg.iteritems():
        suburbs.append(key)

    coords = manifold.MDS(n_components=2, dissimilarity='euclidean').fit(X).embedding_
    plt.figure(1)
    plt.scatter(coords[:, 0], coords[:, 1], alpha=0.5)

    for label, x, y in zip(suburbs, coords[:, 0], coords[:, 1]):
        plt.annotate(
            label,
            xy=(x, y), xytext=(-20, 20),
            textcoords='offset points', ha='right', va='bottom',
            bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

    plt.show()


def write_csv(X):
    col = []
    for i in range(len(X[0])):
        col.append(str(i))
    f = open("features.csv", 'wb')
    writer = csv.writer(f)
    writer.writerow(col)
    writer.writerows(X)
    '''
    with open("features.csv", "wb") as f:
        writer = csv.writer(f)
        writer.writerow(col)
        writer.writerows(X)
    '''
    f.close()

# generate_suburb_feature(suburb1)

# vec1 = [4, 2, 0, 2, 4]
# vec2 = [2, 1, 0, 1, 2]
# print 1-metrics.pairwise.pairwise_distances(vec1, vec2, metric = 'cosine')[0][0]
