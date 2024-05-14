from abc import ABC, abstractmethod

class AbstractBuilding(ABC):
    '''
    Abstract class for building
    '''

    def __init__(self, x: int, y: int) -> None:
        self.__x = x
        self.__y = y
    
    @property
    def position(self) -> tuple:
        '''
        Building position getter
        '''
        return (self.__x, self.__y)
    

    @abstractmethod
    def get_representation(self) -> list:
        '''
        Get building representation
        '''
        pass
    
    @abstractmethod
    def build(self, current_resoruces: dict[str, int]) -> bool:
        '''
        Build building
        '''
        pass