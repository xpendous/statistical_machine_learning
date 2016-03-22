__author__ = 'viva'



__author__ = 'viva'
import parser
from sklearn import manifold
import matplotlib.pyplot as plt

'''
land_use = parser.features_by_category('land_use')

area_use = {}
for item in land_use:
    for key, value in land_use[item].iteritems():
        if '%' not in key:
            try:
                area_use[item].append(float(value))
            except KeyError:
                area_use[item] = [float(value)]
'''

population_2012_raw = parser.features_by_category('population_2012')
population_2007_raw = parser.features_by_category('population_2007')
population_change_raw = parser.features_by_category('population_change')


# features = parser.get_features()

suburbs = []
for item in population_2012_raw:
    suburbs.append(item)


def suburb_pop():
    suburb_pop_features_raw = {}
    suburb_pop_values = {}

    for item in population_2012_raw:
        suburb_pop_features_raw[item] = population_2012_raw[item]
        # suburb_pop_features_raw[item].update(population_2007_raw[item])
        # suburb_pop_features_raw[item].update(population_change_raw[item])

    for key in suburb_pop_features_raw:
        for key1, value1 in suburb_pop_features_raw[key].iteritems():
            if '%' in key1:
                try:
                    suburb_pop_values[key].append(float(value1))
                except ValueError:
                    try:
                        suburb_pop_values[key].append(0.0)
                    except KeyError:
                        suburb_pop_values[key] = [0.0]
                except KeyError:
                    try:
                        suburb_pop_values[key] = [float(value1)]
                    except ValueError:
                        suburb_pop_values[key] = [0.0]

    return suburb_pop_values


'''
    ave_suburb_pop_values = {}
    for item in suburb_pop_values:
        ave_suburb_pop_values[item] = [value / area_use[item][4] for value in suburb_pop_values[item]]
    return ave_suburb_pop_values
'''

if __name__ == "__main__":

    coords = manifold.MDS().fit([value for key, value in suburb_pop().iteritems()]).embedding_
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

