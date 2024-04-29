

class Selectable():
    def __init__(self) -> None:
        self.__is_selected = False

    @property
    def is_selected(self) -> bool:
        '''
        Getter for is_selected
        '''
        return self.__is_selected
    
    @is_selected.setter
    def is_selected(self, value: bool) -> None:
        '''
        Setter for is_selected
        '''
        self.__is_selected = value
