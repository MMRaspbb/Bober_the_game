from .AbstractBobr import AbstractBobr
import pygame

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
    
    
    def get_representation(self):
        
        # load builder.png from resources
        img = pygame.image.load("src/resources/builder.png")
        if self.is_selected:
            img.fill((255, 0, 0, 255), special_flags=pygame.BLEND_RGB_MULT)
        return self.position, img

