import geography
import demographic
import scipy
from itertools import combinations
from sklearn.metrics.pairwise import paired_distances
#from scipy import spatial
from math import hypot
import numpy as np
import matplotlib.pyplot as plt
import csv


suburbs = []
cos_values = []
ecld_dist = []
#################
# change csv file name to save different measure result
#################
#csv_name = 'demographic_baseline_cosine.csv'
#csv_name = 'demographic_baseline_eucld.csv'
csv_name = 'demographic_remove_features.csv'
# remove low variance features, use cosine similarity
#################
# change csv column title
#################
#column1= 'Cosine_simliarity'
column1= 'Duclidean_distance'


# get all (similarity, distance) pairs of any two suburbs
def get_sim_dist_pair():
    # get geograph    
    geo = geography.suburb_geo()
    suburbs = []
    for item in geo:
        suburbs.append(item)

    for (suburb_one, suburb_two) in combinations(suburbs, 2):
        # cosine similarity by any 2 suburbs
        sim=demographic.get_proximity(suburb_one,suburb_two)
        cos_values.append(sim)
        # distance 1: euclidean distance by any 2 suburbs
        # hypot(x2 - x1, y2 - y1)
        (x_one, y_one) = geo[suburb_one][0]
        (x_two, y_two) = geo[suburb_two][0]
        dist = hypot(x_one - x_two, y_one - y_two)
        ecld_dist.append(dist)
        #if sim>6 and dist<80:
        #    print str(sim)+'    '+str(dist)+'    '+suburb_one+'    '+suburb_two




def write_csv():
    # demographic with complete feature
    # the 1st column is cosine similarity
    # the 2nd column is distance
    rows = zip(cos_values,ecld_dist)
    f = open(csv_name, 'wb')
    writer = csv.writer(f)
    writer.writerow([column1, "Suburb_distance"])
    for row in rows:
        writer.writerow(row)
    f.close()


# get correlation coefficient
def get_corrcoef():
    #numpy.corrcoef(ecld_dist, cos_values)
    print scipy.stats.pearsonr(ecld_dist, cos_values)
    #(-0.39561991200997282, 2.4053873422782573e-43)
   

def plot():
    plt.figure(1)
    # plot scatter: x = distance, y = similarity
    plt.subplot(311)
    plt.scatter(ecld_dist, cos_values)
    plt.xlim(xmin=0)
    plt.ylim(ymax=1.05)
    plt.xlabel('distance(km)')
    plt.ylabel('cosine similarity')
    plt.show()

def analysis():
    # get data pair: (similarity, distance)
    get_sim_dist_pair()
    write_csv()
    get_corrcoef()
    #2D plot
    dg = demographic.get_demographic()
    # feature selelction and feature normalisation
    X = demographic.generate_normalized_matrix(dg)
    demographic.feature_reduction(dg,X)


analysis()

