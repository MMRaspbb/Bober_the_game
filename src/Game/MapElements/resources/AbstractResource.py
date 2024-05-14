from abc import ABC, abstractmethod

class AbstractResource(ABC):
    '''
    Abstract class for Resource
    '''

    def __init__(self, x: int, y: int, work_needed: int, reward: int, name: str) -> None:
        super().__init__()
        self.__name = name
        self.__x = x
        self.__y = y
        self.__bobr = None
        self.__work_counter = 0
        self.__work_needed = work_needed
        self.__reward = reward

    def bobr_in(self) -> bool:
        '''
        Check if Bobr is in Resource
        '''
        return self.__bobr is not None
    
    @property
    def get_name(self) -> str:
        '''
        Name getter
        '''
        return self.__name
    
    @property
    def get_reward(self) -> int:
        '''
        Reward getter
        '''
        return self.__reward
    
    def set_bobr(self, bobr) -> None:
        '''
        Set Bobr in Resource
        '''
        self.__bobr = bobr

    @property
    def get_x(self):
        '''
        X getter
        '''
        return self.__x
    
    @property
    def get_y(self):
        '''
        Y getter
        '''
        return self.__y

    @property
    def bobr(self):
        '''
        Bobr getter
        '''
        return self.__bobr

    @property
    def position(self) -> tuple:
        '''
        Resource position getter
        '''
        return (self.__x, self.__y)

    @abstractmethod
    def get_representation(self) -> dict:
        '''
        Get Resource representation
        {(x, y): color}
        '''
        pass

    def __get_if_work_done(self) -> int:
        '''
        Get resources if work is done
        '''
        if self.__work_counter >= self.__work_needed:
            self.__work_counter = 0
            return self.__reward
        return 0

    def adjust_work_counter(self) -> int:
        '''
        Adjust work counter
        '''
        if self.bobr_in():
            self.__work_counter += 1
        return self.__get_if_work_done()

    @abstractmethod
    def is_position_in_resource(self, x: int, y: int) -> bool:
        '''
        Check if position is in resource
        '''
        pass
    
