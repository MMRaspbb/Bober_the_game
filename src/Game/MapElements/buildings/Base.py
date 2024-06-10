from .AbstractBuilding import AbstractBuilding
from ...Maps.MapDirection import MapDirection
from ..Rotatable import Rotatable
import pygame

class Base(AbstractBuilding):
    '''
    Dam building
    '''
    
    def __init__(self, x: int, y: int) -> None:
        AbstractBuilding.__init__(self, x, y)
        self.color = "orange"
        self.__base_size = 2
    
    def get_representation(self) -> list:
        img = pygame.image.load("src/resources/base.png")

        return [[self.position[0], self.position[1], img]]
                
    
    def build(self, current_resoruces: dict[str, int]) -> bool:
        '''
        Build dam
        '''
        return False
    
    def is_position_in_base(self, x: int, y: int) -> bool:
        '''
        Check if position is in base
        '''
        return self.position[0] - self.__base_size <= x < self.position[0] + self.__base_size and self.position[1] - self.__base_size <= y < self.position[1] + self.__base_size
        
 
    def draw_base_menu(self, window_width: int, bobr_price: int) -> list:
        '''
        Draw white menu with three options
        '''

        menu_width = 150
        menu_x = window_width - menu_width 
        menu_y = 0

        font = pygame.font.SysFont('comicsans', 15)

        price_string = ""
        for price_name, price in bobr_price.items():
            price_string += f"   {price_name[0].capitalize()}: {price}"


        buttons = []
        for i, option in enumerate(['Budowniczy', 'Zbieracz', 'Ogrodnik']):
            rect = pygame.Rect(menu_x, menu_y + 33 * i, menu_width, 33)
            pygame.draw.rect(pygame.display.get_surface(), (255, 255, 255), rect)
            pygame.draw.rect(pygame.display.get_surface(), (0, 0, 0), rect, 2)  # Thinner border
            text = font.render(option + price_string, 1, (0, 0, 0))
            text_rect = text.get_rect(center=rect.center)  # Center the text in the rectangle
            pygame.display.get_surface().blit(text, text_rect)
            buttons.append(rect)

        pygame.display.update()

        return buttons