from .AbstractBobr import AbstractBobr
import pygame

class GathererBobr(AbstractBobr):
    '''
    Regular Bobr class
    '''
    
    def __init__(self, name: str, x: int, y: int):
        super().__init__(name, x, y)
        self.color = "purple"
    
    
    def get_representation(self) -> dict:
        '''
        Get Bobr representation
        '''
        img = pygame.image.load("src/resources/gatherer.png")
        if self.is_selected:
            img.fill((255, 0, 0, 255), special_flags=pygame.BLEND_RGB_MULT)
        return self.position, img
    