__author__ = 'viva'

import geography
import econ
import pop
from itertools import combinations
from sklearn.metrics.pairwise import paired_distances

from math import hypot

import numpy as np
import matplotlib.pyplot as plt

pop = pop.suburb_pop()

econ = econ.suburb_econ()
geo = geography.suburb_geo()

suburbs = []
for item in geo:
    suburbs.append(item)

cos_values = []
ecld_dist = []
level_dist = []
gnlz_dist = []

for (suburb_one, suburb_two) in combinations(suburbs, 2):
    # economy test
    cos_values.append(1 - paired_distances(econ[suburb_one], econ[suburb_two], metric="cosine")[0])

    # population test
    # cos_values.append(1 - paired_distances(pop[suburb_one], pop[suburb_two], metric="cosine")[0])

    # euclidean distance
    # hypot(x2 - x1, y2 - y1)
    (x_one, y_one) = geo[suburb_one][0]
    (x_two, y_two) = geo[suburb_two][0]
    dist = hypot(x_one - x_two, y_one - y_two)
    ecld_dist.append(dist)

    '''
    # generalized distance based on euclidean distance
    # polar distance to GPO
    polar_dist_one = geo[suburb_one][1][0]
    polar_dist_two = geo[suburb_two][1][0]

    level_one = 0
    level_two = 0
    if 0 <= polar_dist_one < 10:
        level_one = 0
    elif 10 <= polar_dist_one < 20:
        level_one = 1
    elif 20 <= polar_dist_one < 30:
        level_one = 2
    else:
        level_one = 3

    if 0 <= polar_dist_two < 10:
        level_two = 0
    elif 10 <= polar_dist_two < 20:
        level_two = 1
    elif 20 <= polar_dist_two < 30:
        level_two = 2
    else:
        level_two = 3

    level_diff = abs(level_one - level_two)

    if level_diff == 0:
        dist *= 0.9
    else:
        dist *= pow(1.2, level_diff)

    level_dist.append(dist)

    # DHS area, Primary Care Partnership and LGA
    DPL_one = geo[suburb_one][2]
    DPL_two = geo[suburb_two][2]

    len_intersect = len(set(DPL_one).intersection(DPL_two))
    dist *= pow(0.8, len_intersect)
    dist *= pow(1.1, 3 - len_intersect)
    gnlz_dist.append(dist)
    '''


fil = open('data.txt', 'w')
print >> fil, str(cos_values).replace('[', '').replace(']', '')
print >> fil, str(ecld_dist).replace('[', '').replace(']', '')

# print >> fil, str(gnlz_dist).replace('[', '').replace(']', '')




# visualize the data
colors = np.random.rand(len(cos_values))

plt.figure(1)
plt.scatter(ecld_dist, cos_values, alpha=0.5, c=colors)

# plt.figure(2)
# plt.scatter(level_dist, cos_values, alpha=0.5, c=colors)
# plt.figure(3)
# plt.scatter(gnlz_dist, cos_values, alpha=0.5, c=colors)

plt.show()

