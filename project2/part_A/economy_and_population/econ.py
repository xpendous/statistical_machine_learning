__author__ = 'viva'
import parser
from sklearn import manifold
import matplotlib.pyplot as plt

# econ features analysis

self_defined = ['m with no motor vehicle, %', 'Dwellings with no internet, %', 'Holds degree or higher, %',
                '2012 ERP age 25-44, %', '2012 ERP age 45-64, %',
                '2012 ERP age 15-19, %', '2012 ERP age 20-24, %']

features = parser.get_features()

suburbs = []
for item in features:
    suburbs.append(item)


def suburb_econ():
    suburb_econ_features_raw = {}
    suburb_econ_values = {}

    for item in features:
        suburb_econ_features_raw[item] = features[item]

    for key in suburb_econ_features_raw:

        for key1, value1 in suburb_econ_features_raw[key].iteritems():
            if key1 in self_defined:
                try:
                    suburb_econ_values[key].append(float(value1))
                except ValueError:
                    try:
                        suburb_econ_values[key].append(0.0)
                    except KeyError:
                        suburb_econ_values[key] = [0.0]
                except KeyError:
                    try:
                        suburb_econ_values[key] = [float(value1)]
                    except ValueError:
                        suburb_econ_values[key] = [0.0]

    return suburb_econ_values


if __name__ == "__main__":

    coords = manifold.MDS(n_components=2).fit([value for key, value in suburb_econ().iteritems()]).embedding_
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
