from Game.Maps.MapDirection import MapDirection
from Game.Maps.Map import Map
import heapq

class PathFinder():
    '''
    This class is responsible for finding the path between two points in the map.
    '''

    def __init__(self, map: Map) -> None:
        self.__map = map

    def is_valid_tile(self, tile: tuple[int, int]) -> bool:
        # TODO: add check for river
        x, y = tile
        if x < 0 or x >= self.__map.width or y < 0 or y >= self.__map.height:
            return False
        return True

    def find_path(self, start: tuple[int, int], end: tuple[int, int]) -> list[MapDirection]:
        (start_x, start_y) = self.__map.convert_pixel_to_tile(*start)
        (end_x, end_y) = self.__map.convert_pixel_to_tile(*end)

        # perform A* to find the path
        queue = [(0, (start_x, start_y))]  # priority queue with (cost, tile) tuples
        visited = set()
        parent = {}
        found = False
        while queue:
            current = heapq.heappop(queue)[1]  # get the tile with the lowest cost
            if current == (end_x, end_y):
                found = True
                break
            visited.add(current)
            for direction in MapDirection:
                next_tile = (current[0] + direction.value[0], current[1] + direction.value[1])
                if self.is_valid_tile(next_tile) and next_tile not in visited:
                    parent[next_tile] = (current, direction)
                    cost = abs(end_x - next_tile[0]) + abs(end_y - next_tile[1])  # heuristic
                    heapq.heappush(queue, (cost, next_tile))

        if not found:
            return []

        # move from end to start to get the path
        path = []
        current = (end_x, end_y)
        while current != (start_x, start_y):
            path.append(parent[current][1])
            current = parent[current][0]

        # reverse the path
        return path[::-1]

            