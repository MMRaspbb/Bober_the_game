import random
from math import sqrt
from src.Game.Utils.RiverNodesCreator import RiverNodesCreator


class River:
    def __init__(self, beginning: list[int, int], end: list[int, int], strength: int) -> None:
        self.__beginning = beginning
        self.__end = end
        self.__backward_flow = False
        if end[0] < beginning[0]:
            self.__backward_flow = True
        self.__interpolation_nodes_distance = 10
        self.__river_segment_length = 1
        self.__delineate_river()
        self.river_state = 0
        self.__river_state_limiter = len(self.river_points) - 1
        self.__strength = strength

    def __delineate_river(self) -> None:
        riverNodeCreator = RiverNodesCreator()
        nodes = riverNodeCreator.node_creator(self.__beginning, self.__end, 10, self.__interpolation_nodes_distance,
                                              self.__river_segment_length)
        self.river_points = []
        for i in range(1, len(nodes)):
            x1, y1 = nodes[i - 1]
            x2, y2 = nodes[i]
            versor = ((x2 - x1) / self.__river_segment_length, (y2 - y1) / self.__river_segment_length)
            for j in range(self.__river_segment_length):
                self.river_points.append((x1 + versor[0] * j, y1 + versor[1] * j))
    def push_river_state(self) -> bool: #returns if the river was pushed or just stayed in place
        if (self.river_state < self.__river_state_limiter):
            self.river_state += 1
            return True
        return False

    def block_river(self) -> None:
        self.__river_state_limiter = self.river_state
    def set_river_limit(self, limit: int) -> None:
        self.__river_state_limiter = limit
        if(self.river_state > self.__river_state_limiter):
            self.river_state = self.__river_state_limiter

    def get_pushed_point(self) -> tuple[int, int]:
        if self.__backward_flow:
            return self.river_points[-1 - self.river_state]
        else:
            return self.river_points[self.river_state]

    def get_default_end(self) -> tuple[int, int]:
        return self.river_points[-1]
    @property
    def get_strength(self) -> int:
        return self.__strength
    def contains_or_touches(self, point: tuple[int, int]) -> bool:
        # temporary solution, can be solved quicker with binary search

        river_points = self.river_points
        if self.__backward_flow:
            river_range = range(len(river_points) - 1, len(river_points) - 1 - self.river_state, -1)
        else:
            river_range = range(self.river_state)
        versors = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]
        for versor in versors:
            point_to_check = (point[0] + versor[0], point[1] + versor[1])
            for i in river_range:
                if river_points[i] == point_to_check:
                    return i
        return -1
    def decolor_excess(self, colors: dict) -> None: #Probably temporary as we will stop using colors in the future
        river_points = self.river_points
        river_excess = 0
        if self.__backward_flow:
            river_excess = range(self.river_state, self.__river_state_limiter)
        else:
            river_excess = range(self.river_state + 1, self.__river_state_limiter)
        for i in river_excess:
            print("siema")
            colors.pop((river_points[i][0],river_points[i][1]))
            # colors.pop((river_points[i][0] + 1, river_points[i][1]))
            # colors.pop((river_points[i][0] - 1, river_points[i][1]))
            # colors.pop((river_points[i][0], river_points[i][1] + 1))
            # colors.pop((river_points[i][0], river_points[i][1] - 1))
            # if i + 1 < len(river_points):
            #     versor = (river_points[i + 1][0] - river_points[i][0], river_points[i + 1][1] - river_points[i][1])
            #     if (versor[0] > 0):
            #         if (versor[1] > 0):
            #             colors.pop((river_points[i][0], river_points[i][1] + 2))
            #         elif (versor[1] < 0):
            #             colors.pop((river_points[i][0], river_points[i][1] - 2))

    def draw(self, colors: dict) -> None:
        river_points = self.river_points
        river_range = 0
        if self.__backward_flow:
            river_range = range(len(river_points) - 1, len(river_points) - 1 - self.river_state, -1)
        else:
            river_range = range(self.river_state)
        for i in river_range:
            colors[river_points[i]] = 'blue'
            colors[(river_points[i][0] + 1, river_points[i][1])] = 'blue'
            colors[(river_points[i][0] - 1, river_points[i][1])] = 'blue'
            colors[(river_points[i][0], river_points[i][1] + 1)] = 'blue'
            colors[(river_points[i][0], river_points[i][1] - 1)] = 'blue'
            if i + 1 < len(river_points):
                versor = (river_points[i + 1][0] - river_points[i][0], river_points[i + 1][1] - river_points[i][1])
                if (versor[0] > 0):
                    if (versor[1] > 0):
                        colors[(river_points[i][0], river_points[i][1] + 2)] = 'blue'
                    elif (versor[1] < 0):
                        colors[(river_points[i][0], river_points[i][1] - 2)] = 'blue'
