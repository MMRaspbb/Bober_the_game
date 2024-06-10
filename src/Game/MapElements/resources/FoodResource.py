from .AbstractResource import AbstractResource
import pygame

class FoodResource(AbstractResource):
    '''
    Forest Resource
    '''
    
    def __init__(self, x: int, y: int) -> None:
        self.__name = "food"
        self.__work_needed = 400
        self.__reward = 2
        self.__resource_size = 5

        super().__init__(x, y, self.__work_needed, self.__reward, self.__name)
    
    @staticmethod
    def get_resource_size() -> int:
        '''
        Get resource size
        '''
        return 5

    def is_position_in_resource(self, x: int, y: int) -> bool:
        '''
        Check if position is in resource
        '''
        return self.get_x <= x < self.get_x + self.__resource_size and self.get_y <= y < self.get_y + self.__resource_size
    
    def get_representation(self) -> list:
        '''
        Get Resource representation
        '''
        img = pygame.image.load("src/resources/farmland.png")
        representation = []
        for i in range(self.__resource_size):
            for j in range(self.__resource_size):
                representation.append([self.position[0] + i, self.position[1] + j, img])
        return representation
    