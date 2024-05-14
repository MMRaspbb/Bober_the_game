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
                for j in range (-2, 3):
                    representation.append([self.position[0] + i, self.position[1] + j, self.color])
        elif self.get_orientation() == MapDirection.EAST or self.get_orientation() == MapDirection.WEST:
            for i in range(-2, 3):
                for j in range (-1, 2):
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