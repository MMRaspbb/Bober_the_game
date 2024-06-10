from Game.Maps.MapDirection import MapDirection
from Game.MapElements.Bobrs.GathererBobr import GathererBobr
from Game.Maps.Map import Map
import pygame
import heapq

class PathFinder():
    '''
    This class is responsible for finding the path between two points in the map.
    '''

    def __init__(self, map: Map) -> None:
        self.__map = map
        self.bobr_range = 1000

    def is_valid_tile(self, tile: tuple[int, int]) -> bool:
        # TODO: add check for river
        x, y = tile
        # all_rivers = [(river[0], river[1]) for river in [full_river.get_representation() for full_river in self.__map.rivers]]

        if x < 0 or x >= self.__map.width or y < 0 or y >= self.__map.height:
                return False
    
        # if tile in all_rivers:
        for river in self.__map.rivers:
            if river.contains_or_touches(tile) != -1:
                return False
            
        for resource in self.__map.resources:
            if resource.is_position_in_resource(*tile) and resource.bobr_in() and not resource.bobr.is_selected:
                return False
                
        return True

    def find_path(self, start: tuple[int, int], end: tuple[int, int]) -> list[MapDirection]:
        start_x, start_y = start[0] - self.__map.surface_destination[0], start[1] - self.__map.surface_destination[1]
        end_x, end_y = end[0] - self.__map.surface_destination[0], end[1] - self.__map.surface_destination[1]
        (start_x, start_y) = self.__map.convert_pixel_to_tile(start_x, start_y)
        (end_x, end_y) = self.__map.convert_pixel_to_tile(end_x, end_y)

        # perform A* to find the path
        queue = [(0, (start_x, start_y))]  # priority queue with (cost, tile) tuples
        visited = set()
        parent = {}
        found = False
        to_break = False
        counter = 0
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
                elif counter == self.bobr_range:
                    to_break = True
                else:
                    counter += 1

            if to_break:
                break

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

            