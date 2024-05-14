from .AbstractBobr import AbstractBobr

class BuilderBobr(AbstractBobr):
    '''
    Regular Bobr class
    '''
    
    def __init__(self, name: str, x: int, y: int):
        super().__init__(name, x, y)
        self.color = "orange"

    def build(self):
        '''
        Build building
        '''
        pass
    
    
    def get_representation(self) -> dict:
        '''
        Get Bobr representation
        '''
        if super().is_selected:
            return [super().position[0], super().position[1], "Red"]
        return [super().position[0], super().position[1], self.color]