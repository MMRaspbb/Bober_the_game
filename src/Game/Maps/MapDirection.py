from enum import Enum

class MapDirection(Enum):
    '''
    Enum for map directions
    '''
    NORTH = (0, 1)
    NORTH_EAST = (1, 1)
    EAST = (1, 0)
    SOUTH_EAST = (1, -1)
    SOUTH = (0, -1)
    SOUTH_WEST = (-1, -1)
    WEST = (-1, 0)
    NORTH_WEST = (-1, 1)

    def next(self, current_direction: 'MapDirection') -> 'MapDirection':
        '''
        Get next direction
        '''
        directions = [list(MapDirection)[i] for i in range(8)]
        index = directions.index(current_direction)
        return directions[(index + 1) % 8]
    
    def previous(self, current_direction: 'MapDirection') -> 'MapDirection':
        '''
        Get previous direction
        '''
        directions = [list(MapDirection)[i] for i in range(8)]
        index = directions.index(current_direction)
        return directions[(index - 1) % 8]
    def get_opposite(self, current_direction: 'MapDirection') -> 'MapDirection':
        directions = [list(MapDirection)[i] for i in range(8)]
        index = directions.index(current_direction)
        return directions[(index + 4) % 8]
    def get_double_next(self, current_direction: 'MapDirection') -> 'MapDirection':
        directions = [list(MapDirection)[i] for i in range(8)]
        index = directions.index(current_direction)
        return directions[(index + 2) % 8]

    def get_double_previous(self, current_direction: 'MapDirection') -> 'MapDirection':
        directions = [list(MapDirection)[i] for i in range(8)]
        index = directions.index(current_direction)
        return directions[(index - 2) % 8]

    @staticmethod
    def tuple_to_map_direction(vector) -> 'MapDirection':
        for direction in MapDirection:
            if direction.value == vector:
                return direction
        raise ValueError(f"No MapDirection found for tuple {vector}")
        
