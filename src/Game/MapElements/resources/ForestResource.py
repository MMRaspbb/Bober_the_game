from .AbstractResource import AbstractResource

class ForestResource(AbstractResource):
    '''
    Forest Resource
    '''
    
    def __init__(self, x: int, y: int) -> None:
        self.__name = "wood"
        self.__work_needed = 300
        self.__reward = 1
        self.__resource_size = 5

        super().__init__(x, y, self.__work_needed, self.__reward, self.__name)

    def is_position_in_resource(self, x: int, y: int) -> bool:
        '''
        Check if position is in resource
        '''
        return self.get_x <= x < self.get_x + self.__resource_size and self.get_y <= y < self.get_y + self.__resource_size
    
    def get_representation(self) -> list:
        '''
        Get Resource representation
        '''
        representation = []
        for i in range(self.__resource_size):
            for j in range(self.__resource_size):
                representation.append([self.position[0] + i, self.position[1] + j, 'darkgreen'])
        return representation
    