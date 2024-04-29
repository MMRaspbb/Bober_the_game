import math
import random
from scipy.interpolate import CubicSpline


class RiverNodesCreator:
    def node_creator(self, beginning: list[int, int], end: list[int, int], curvature_indicator: float, interpolation_nodes_distance: int, river_segment_length: int) -> list[
        tuple[int, int]]:
        angle = math.atan((end[1] - beginning[1]) / (end[0] - beginning[0]))
        invert = False
        switch_bae = False
        if angle > math.pi / 4 or angle < -math.pi / 4:
            invert = True
            beginning[0], beginning[1] = beginning[1], beginning[0]
            end[0], end[1] = end[1], end[0]
        if (beginning[0] > end[0]):
            beginning, end = end, beginning
            switch_bae = True
        x, y = self.__create_interpolation_nodes(beginning, end, curvature_indicator, interpolation_nodes_distance)
        interpolation = CubicSpline(x, y)
        x, y = self.__delinerate_river(river_segment_length, interpolation, beginning, end)

        if invert:
            for i in range(len(x)):
                x[i],y[i] = y[i],x[i]
        nodes = [(x[i],y[i]) for i in range(len(x))]
        return nodes

    def __create_interpolation_nodes(self, beginning: list[int, int], end: list[int, int],
                                     curvature_indicator: float, interpolation_nodes_distance: int):
        a = (beginning[1] - end[1]) / (beginning[0] - end[0])
        b = beginning[1] - a * beginning[0]
        linear_function = lambda x: a * x + b
        current_x = beginning[0] + interpolation_nodes_distance
        perpendicular_x = [beginning[0]]
        perpendicular_y = [beginning[1]]
        while (current_x < end[0]):
            rand_distance = random.random() * 2 - 1
            perpendicular_x.append(current_x)
            perpendicular_y.append(linear_function(current_x) + curvature_indicator * rand_distance)
            current_x += interpolation_nodes_distance
        if(perpendicular_x[-1] < end[0]):
            perpendicular_x.append(end[0])
            perpendicular_y.append(end[1])
        return perpendicular_x, perpendicular_y

    def __delinerate_river(self, segment_length: float, function, beginning: list[int, int] , end: list[int, int]):
        vectors = [(1, 0), (1,1), (0,1), (0, -1), (1, -1)]
        river_x = [beginning[0]]
        river_y = [beginning[1]]
        current_x = beginning[0]
        current_y = beginning[1]
        previous_vector = (2,2)
        while(current_x <= end[0] - segment_length):
            minim_distance = float('inf')
            minim_vector_index = 0
            for i in range(len(vectors)):
                distance = abs(function(current_x + vectors[i][0] * segment_length) - (current_y + vectors[i][1] * segment_length))
                if minim_distance > distance:
                    minim_distance = distance
                    minim_vector_index = i
            if vectors[minim_vector_index] == (-previous_vector[0], -previous_vector[1]):
                river_x.pop()
                river_y.pop()
                current_y -= previous_vector[1] * segment_length
                minim_distance = float('inf')
                minim_vector_index = 0
                for i in range(len(vectors)):
                    if vectors[i][0] == 0:
                        continue
                    distance = abs(function(current_x + vectors[i][0] * segment_length) - (current_y + vectors[i][1] * segment_length))
                    if minim_distance > distance:
                        minim_distance = distance
                        minim_vector_index = i
            current_x += vectors[minim_vector_index][0] * segment_length
            current_y += vectors[minim_vector_index][1] * segment_length
            river_x.append(current_x)
            river_y.append(current_y)
            previous_vector = vectors[minim_vector_index]

        return river_x, river_y
