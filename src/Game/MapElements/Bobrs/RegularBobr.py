from .AbstractBobr import AbstractBobr
from ..BuildingEnum import BuildingEnum

class RegularBobr(AbstractBobr):
    '''
    Regular Bobr class
    '''
    
    def __init__(self, name: str, x: int, y: int):
        super().__init__(name, x, y)
        self.color = "Brown"
    
    def build(self, mouse_x: int, mouse_y: int, building: BuildingEnum) -> None:
        '''
        Build building on Bobr position
        '''
        pass
    
    def get_representation(self) -> dict:
        '''
        Get Bobr representation
        '''
        if super().is_selected:
            return [super().position[0], super().position[1], "Red"]
        return [super().position[0], super().position[1], self.color]