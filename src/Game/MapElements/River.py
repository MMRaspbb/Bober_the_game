import random
from math import sqrt

class River:
    def __init__(self, beginning: tuple[int, int], end: tuple[int, int]) -> None:
        self.beginning = beginning
        self.end = end
        self.__delineate_river()

    def __delineate_river(self):
        x1, y1 = self.beginning[0], self.beginning[1]
        x2, y2 = self.end[0], self.end[1]
        a = (y1 - y2) / (x1 - x2)
        b = y1 - a * x1
        horizontal_current = -self.end[0] if x1 > x2 else self.end[0]
        current_position = [x1, y1]
        nodes = [(x1, y1)]
        step = (x2 - x1) / sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        self.amplitude = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) / (0.5 * (x2 - x1))
        while (current_position[0] + step < horizontal_current):
            # follow the line passing through the beginning and the end
            # and add a random value to the y coordinate
            # to simulate the river's flow
            current_position[0] += step
            current_position[1] = a * current_position[0] + b
            random_value = random.uniform(-self.amplitude, self.amplitude)
            current_position[1] += random_value
            nodes.append((current_position[0], current_position[1]))

        nodes.append((self.end[0], self.end[1]))
        self.nodes = nodes

    def draw(self, colors : dict) -> None:
        for i in range(1, len(self.nodes)):
            x1, y1 = self.nodes[i - 1]
            x2, y2 = self.nodes[i]
            vector = (x2 - x1, y2 - y1)
            values_to_check = 50
            for j in range(values_to_check):
                x = x1 + j * vector[0] / values_to_check
                y = y1 + j * vector[1] / values_to_check
                colors[(int(x), int(y))] = 'blue'
        
        