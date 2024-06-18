from .AbstractBobr import AbstractBobr
import pygame

class GardenerBobr(AbstractBobr):
    '''
    Gardener Bobr class
    '''
    
    def __init__(self, name: str, x: int, y: int):
        super().__init__(name, x, y)
        self.color = "dark blue"
    
    
    def get_representation(self) -> dict:
        '''
        Get Bobr representation
        '''
        img = pygame.image.load("src/resources/gardener.png")
        if self.is_selected:
            img.fill((255, 0, 0, 255), special_flags=pygame.BLEND_RGB_MULT)
        return self.position, img