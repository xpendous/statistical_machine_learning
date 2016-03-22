__author__ = 'viva'

import parser
import math

pi = math.pi

directions = ['Northern', 'Southern', 'Eastern', 'Western']
remoteness = ['Major', 'Inner', 'Outer', 'Remote', 'Very']

angles = {'E': 0, 'ENE': pi / 8, 'NE': pi / 4, 'NNE': pi * 3 / 8,
          'N': pi / 2, 'NNW': pi * 5 / 8, 'NW': pi * 3 / 4, 'WNW': pi * 7 / 8,
          'W': pi, 'WSW': -pi * 7 / 8, 'SW': -pi * 3 / 4, 'SSW': -pi * 5 / 8,
          'S': -pi / 2, 'SSE': -pi * 3 / 8, 'SE': -pi / 4, 'ESE': -pi / 8}

community = parser.features_by_category('community')
geography = parser.features_by_category('geography')

suburb_geo_values = {}


def suburb_geo():

    for item in geography:

        # pure polar and euclidean distance
        polar_coords = geography[item]['Location'].split(' ')[0:2]
        polar_angle = angles[polar_coords[1]]
        polar_distance = polar_coords[0].split('km')[0]

        x_coords = float(polar_distance) * math.cos(polar_angle)
        y_coords = float(polar_distance) * math.sin(polar_angle)

        suburb_geo_values[item] = [(x_coords, y_coords), (float(polar_distance), polar_angle),
                                   [geography[item]['DHS Area'], geography[item]['Primary Care Partnership'],
                                    geography[item]['LGA']]]

    return suburb_geo_values


if __name__ == "__main__":
    print suburb_geo()

