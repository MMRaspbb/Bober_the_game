from .AbstractBuilding import AbstractBuilding
from ...Maps.MapDirection import MapDirection
from ..Rotatable import Rotatable


class Dam(AbstractBuilding, Rotatable):
    '''
    Dam building
    '''

    def __init__(self, x: int, y: int) -> None:
        AbstractBuilding.__init__(self, x, y)
        Rotatable.__init__(self, MapDirection.NORTH)
        self.color = "brown"

    def get_representation(self) -> list:
        representation = []

        if self.get_orientation() == MapDirection.NORTH or self.get_orientation() == MapDirection.SOUTH:
            for i in range(-1, 2):
                for j in range(-2, 3):
                    representation.append([self.position[0] + i, self.position[1] + j, self.color])
        elif self.get_orientation() == MapDirection.EAST or self.get_orientation() == MapDirection.WEST:
            for i in range(-2, 3):
                for j in range(-1, 2):
                    representation.append([self.position[0] + i, self.position[1] + j, self.color])
        elif self.get_orientation() == MapDirection.NORTH_EAST or self.get_orientation() == MapDirection.SOUTH_WEST:
            representation = [[self.position[0], self.position[1], self.color],
                              [self.position[0] + 1, self.position[1], self.color],
                              [self.position[0] - 1, self.position[1], self.color],
                              [self.position[0], self.position[1] + 1, self.color],
                              [self.position[0], self.position[1] - 1, self.color],
                              [self.position[0] + 1, self.position[1] + 1, self.color],
                              [self.position[0] - 1, self.position[1] - 1, self.color],
                              [self.position[0] + 2, self.position[1] + 2, self.color],
                              [self.position[0] - 2, self.position[1] - 2, self.color],
                              [self.position[0] + 2, self.position[1] + 1, self.color],
                              [self.position[0] - 2, self.position[1] - 1, self.color],
                              [self.position[0] + 1, self.position[1] + 2, self.color],
                              [self.position[0] - 1, self.position[1] - 2, self.color]]
        else:
            representation = [[self.position[0], self.position[1], self.color],
                              [self.position[0], self.position[1] + 1, self.color],
                              [self.position[0], self.position[1] - 1, self.color],
                              [self.position[0] + 1, self.position[1], self.color],
                              [self.position[0] - 1, self.position[1], self.color],
                              [self.position[0] + 1, self.position[1] - 1, self.color],
                              [self.position[0] - 1, self.position[1] + 1, self.color],
                              [self.position[0] + 2, self.position[1] - 2, self.color],
                              [self.position[0] - 2, self.position[1] + 2, self.color],
                              [self.position[0] + 1, self.position[1] - 2, self.color],
                              [self.position[0] - 1, self.position[1] + 2, self.color],
                              [self.position[0] + 2, self.position[1] - 1, self.color],
                              [self.position[0] - 2, self.position[1] + 1, self.color]]

        return representation

    def build(self, current_resoruces: dict[str, int]) -> bool:
        '''
        Build dam
        '''
        if current_resoruces['wood'] >= 10 and current_resoruces['stone'] >= 10:
            current_resoruces['wood'] -= 10
            current_resoruces['stone'] -= 10
            return True
        return False

    def get_bounced_direction(self, direction):
        direction = MapDirection.tuple_to_map_direction(direction)
        orientation = self.orientation
        if direction == MapDirection.NORTH:
            if orientation == MapDirection.NORTH_WEST or orientation == MapDirection.SOUTH_EAST:
                return MapDirection.WEST
            if orientation == MapDirection.NORTH_EAST or orientation == MapDirection.SOUTH_WEST:
                return MapDirection.EAST

        if direction == MapDirection.SOUTH:
            if orientation == MapDirection.NORTH_WEST or orientation == MapDirection.SOUTH_EAST:
                return MapDirection.EAST
            if orientation == MapDirection.NORTH_EAST or orientation == MapDirection.SOUTH_WEST:
                return MapDirection.WEST

        if direction == MapDirection.EAST:
            if orientation == MapDirection.NORTH_WEST or orientation == MapDirection.SOUTH_EAST:
                return MapDirection.SOUTH
            if orientation == MapDirection.NORTH_EAST or orientation == MapDirection.SOUTH_WEST:
                return MapDirection.NORTH

        if direction == MapDirection.WEST:
            if orientation == MapDirection.NORTH_WEST or orientation == MapDirection.SOUTH_EAST:
                return MapDirection.NORTH
            if orientation == MapDirection.NORTH_EAST or orientation == MapDirection.SOUTH_WEST:
                return MapDirection.SOUTH

        if direction == MapDirection.NORTH_WEST:
            if orientation == MapDirection.NORTH or orientation == MapDirection.SOUTH:
                return MapDirection.NORTH_EAST
            if orientation == MapDirection.EAST or orientation == MapDirection.WEST:
                return MapDirection.SOUTH_WEST

        if direction == MapDirection.NORTH_EAST:
            if orientation == MapDirection.NORTH or orientation == MapDirection.SOUTH:
                return MapDirection.NORTH_WEST
            if orientation == MapDirection.EAST or orientation == MapDirection.WEST:
                return MapDirection.SOUTH_EAST

        if direction == MapDirection.SOUTH_EAST:
            if orientation == MapDirection.NORTH or orientation == MapDirection.SOUTH:
                return MapDirection.SOUTH_WEST
            if orientation == MapDirection.EAST or orientation == MapDirection.WEST:
                return MapDirection.NORTH_EAST

        if direction == MapDirection.SOUTH_WEST:
            if orientation == MapDirection.NORTH or orientation == MapDirection.SOUTH:
                return MapDirection.SOUTH_EAST
            if orientation == MapDirection.EAST or orientation == MapDirection.WEST:
                return MapDirection.NORTH_WEST







