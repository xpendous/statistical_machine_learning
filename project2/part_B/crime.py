__author__ = 'viva'

__author__ = 'viva'
import parser
from sklearn import manifold
from sklearn.cluster import KMeans

import numpy as np

import matplotlib.pyplot as plt

# crime features analysis

self_defined = ['Personal income <$400/week, %', 'Mental Health',
                'Did not complete year 12, %', 'Unemployed, %',
                '% dwellings which are public housing',
                '2012 ERP age 15-24, %', '2012 ERP age 25-44, %']

features = parser.get_features()

suburbs = []
for item in features:
    suburbs.append(item)


def suburb_crime():
    suburb_crime_features_raw = {}
    suburb_crime_values = {}

    for item in features:
        suburb_crime_features_raw[item] = features[item]

    for key in suburb_crime_features_raw:

        for key1, value1 in suburb_crime_features_raw[key].iteritems():
            if key1 in self_defined:
                # if '% change, 2007-2012' in key1:
                try:
                    suburb_crime_values[key].append(float(value1))
                except ValueError:
                    try:
                        suburb_crime_values[key].append(0.0)
                    except KeyError:
                        suburb_crime_values[key] = [0.0]
                except KeyError:
                    try:
                        suburb_crime_values[key] = [float(value1)]
                    except ValueError:
                        suburb_crime_values[key] = [0.0]

    return suburb_crime_values


if __name__ == "__main__":
    coords = manifold.MDS(n_components=2).fit([value for key, value in suburb_crime().iteritems()]).embedding_

    n_cluster = 4
    k_means = KMeans(init='k-means++', n_clusters=n_cluster, n_init=10)
    k_means.fit(coords)
    k_means_labels = k_means.labels_
    k_means_cluster_centers = k_means.cluster_centers_
    k_means_labels_unique = np.unique(k_means_labels)

    colors = ['#4EACC5', '#FF9C34', '#4E9A06', "#F0F8FF", "#800000", "#D2691E", "#FFFACD", "#FA8072", "#D2691E"]

    for k, col in zip(range(n_cluster), colors):
        my_members = k_means_labels == k
        cluster_center = k_means_cluster_centers[k]
        plt.plot(coords[my_members, 0], coords[my_members, 1], 'w',
                 markerfacecolor=col, marker='o', markersize=20)
        plt.plot(cluster_center[0], cluster_center[1], 'x', markerfacecolor=col,
                 markeredgecolor='red', markersize=20, markeredgewidth=2)

    # plt.figure(1)
    # plt.scatter(coords[:, 0], coords[:, 1], alpha=0.5)

    for label, x, y in zip(suburbs, coords[:, 0], coords[:, 1]):
        plt.annotate(
            label,
            xy=(x, y), xytext=(-20, 20),
            textcoords='offset points', ha='right', va='bottom',
            bbox=dict(boxstyle='round,pad=0.5', fc='white', alpha=0.5),
            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

    plt.show()
