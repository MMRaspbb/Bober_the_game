from Game.Utils.RiverNodesCreator import RiverNodesCreator
import pygame


class River:
    def __init__(self, beginning: list[int, int], end: list[int, int]) -> None:
        self.river_points = self.delineate_river(beginning, end, 10, 1)
        self.river_state = 0


    @staticmethod
    def delineate_river(beginning, end, interpolation_nodes_distance, river_segment_length):
        riverNodeCreator = RiverNodesCreator()
        nodes = riverNodeCreator.node_creator(beginning, end, 10, interpolation_nodes_distance,
                                              river_segment_length)
        river_points = []
        for i in range(1, len(nodes)):
            x1, y1 = nodes[i - 1]
            x2, y2 = nodes[i]
            versor = ((x2 - x1) / river_segment_length, (y2 - y1) / river_segment_length)
            for j in range(river_segment_length):
                river_points.append((x1 + versor[0] * j, y1 + versor[1] * j))

        return river_points

    def push_river_state(self) -> bool:  # returns if the river was pushed or just stayed in place
        if (self.river_state < len(self.river_points) - 1):
            self.river_state += 1
            return True
        return False

    def get_pushed_point(self) -> tuple[int, int]:
        return self.river_points[self.river_state]

    def get_default_end(self) -> tuple[int, int]:
        return self.river_points[-1]

    def contains_or_touches(self, point: tuple[int, int]) -> int:

        river_points = self.river_points
        versors = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]
        for versor in versors:
            point_to_check = (point[0] + versor[0], point[1] + versor[1])
            for i in range(self.river_state):
                if river_points[i] == point_to_check:
                    return i
        return -1

    def get_representation(self) -> list:
        result = []
        river_points = self.river_points
        img = pygame.image.load("src/resources/water.png")
        for i in range(self.river_state):
            result.append([int(river_points[i][0]), int(river_points[i][1]), img])
            result.append([int(river_points[i][0] + 1), int(river_points[i][1]), img])
            result.append([int(river_points[i][0] - 1), int(river_points[i][1]), img])
            result.append([int(river_points[i][0]), int(river_points[i][1] + 1), img])
            result.append([int(river_points[i][0]), int(river_points[i][1] - 1), img])
            if i + 1 < len(river_points):
                versor = (river_points[i + 1][0] - river_points[i][0], river_points[i + 1][1] - river_points[i][1])
                if (versor[0] > 0):
                    if (versor[1] > 0):
                        result.append([int(river_points[i][0]), int(river_points[i][1] + 2), img])
                    elif (versor[1] < 0):
                        result.append([int(river_points[i][0]), int(river_points[i][1] - 2), img])

        return result

    def modify_river_end_points(self, new_river_points: list[tuple[int, int]], begin_index: int) -> None:
        updated_points = []
        for i in range(self.river_state):
            updated_points.append(self.river_points[i])
        for i in range(begin_index, len(new_river_points)):
            updated_points.append(new_river_points[i])
        self.__river_state_limiter = len(updated_points) - 1
        self.river_points = updated_points

    def get_river_points(self) -> list[tuple[int, int]]:
        return self.river_points

    def set_river_state(self, state: int) -> None:
        self.river_state = state
