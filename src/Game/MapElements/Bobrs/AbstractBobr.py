from abc import ABC, abstractmethod
from Game.Maps.MapDirection import MapDirection
from ..Selectable import Selectable

class AbstractBobr(ABC, Selectable):
    '''
    Abstract class for Bobr
    '''

    def __init__(self, name: str, x: int, y: int) -> None:
        super().__init__()
        self.__name = name
        self.__x = x
        self.__y = y
        self.__path = []

    @property
    def get_x(self) -> int:
        '''
        Get x coordinate
        '''
        return self.__x
    
    @property
    def get_y(self) -> int:
        '''
        Get y coordinate
        '''
        return self.__y

    def move(self) -> None:
        '''
        Move Bobr in given direction
        '''
        if self.__path:
            direction = self.__path.pop(0)
            self.__x += direction.value[0]
            self.__y += direction.value[1]

    def set_path(self, path: list[MapDirection]) -> None:
        '''
        Set path for Bobr
        '''
        self.__path = path


    @property
    def name(self) -> str:
        '''
        Bobr name getter
        '''
        return self.__name
    
    @property
    def position(self) -> tuple:
        '''
        Bobr position getter
        '''
        return (self.__x, self.__y)
    

    @abstractmethod
    def get_representation(self) -> dict:
        '''
        Get Bobr representation
        {(x, y): color}
        '''
        pass
    

