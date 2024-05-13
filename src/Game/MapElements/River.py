from Game.Utils.RiverNodesCreator import RiverNodesCreator


class River:
    def __init__(self, beginning: list[int, int], end: list[int, int]) -> None:
        self.__beginning = beginning
        self.__end = end
        self.__interpolation_nodes_distance = 10
        self.__river_segment_length = 1
        self.__delineate_river()
        if end[0] < beginning[0]:
            self.river_points.reverse()
        self.river_state = 0
        self.__river_state_limiter = len(self.river_points) - 1

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
        return self.river_points[self.river_state]

    def get_default_end(self) -> tuple[int, int]:
        return self.river_points[-1]
    @property
    def get_strength(self) -> int:
        return self.__strength
    def contains_or_touches(self, point: tuple[int, int]) -> bool:
        # temporary solution, can be solved quicker with binary search

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
        for i in range(self.river_state):
            result.append([int(river_points[i][0]), int(river_points[i][1]), 'blue'])
            result.append([int(river_points[i][0] + 1), int(river_points[i][1]), 'blue'])
            result.append([int(river_points[i][0] - 1), int(river_points[i][1]), 'blue'])
            result.append([int(river_points[i][0]), int(river_points[i][1] + 1), 'blue'])
            result.append([int(river_points[i][0]), int(river_points[i][1] - 1), 'blue'])
            if i + 1 < len(river_points):
                versor = (river_points[i + 1][0] - river_points[i][0], river_points[i + 1][1] - river_points[i][1])
                if (versor[0] > 0):
                    if (versor[1] > 0):
                        result.append([int(river_points[i][0]), int(river_points[i][1] + 2), 'blue'])
                    elif (versor[1] < 0):
                        result.append([int(river_points[i][0]), int(river_points[i][1] - 2), 'blue'])

        return result
    def modify_river_end_points(self, new_river_points: list[tuple[int, int]], begin_index: int) -> None:
        updated_points = []
        for i in range(self.river_state):
            updated_points.append(self.river_points[i])
        for i in range(begin_index, len(new_river_points)):
            updated_points.append(new_river_points[i])
        self.__river_state_limiter = len(updated_points)
        self.river_points = updated_points
    def get_river_points(self) -> list[tuple[int, int]]:
        return self.river_points