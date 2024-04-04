import pygame
from .Maps.Map import Map
from sys import exit
from pygame.locals import RESIZABLE

class GameLoop:
    screen = pygame.display.set_mode((800, 600), RESIZABLE)
    pygame.display.set_caption("Bober")
    clock = pygame.time.Clock()

    surface_parameters = (800, 600)
    surface = pygame.Surface(surface_parameters)
    surface_destination = (0,0)
    surface.fill('Light Green')

    map = Map(surface_parameters, surface_destination)

    def initialize(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.VIDEORESIZE:
                    self.fix_surface_position()
            self.screen.blit(self.surface, self.surface_destination)
            self.map.draw(self.surface)
            pygame.display.update()
            self.clock.tick(30)
            
    def fix_surface_position(self):
        width, height = pygame.display.get_surface().get_size()
        normalized_width = width / 4
        normalized_height = height / 3
        if normalized_width > normalized_height:
            self.surface_parameters = (normalized_height * 4, height)
            self.surface_destination = (width / 2 - normalized_height * 2, 0)
        else:
            self.surface_parameters = (width, normalized_width * 3)
            self.surface_destination = (0, height / 2 - normalized_width * 1.5)
        self.surface = pygame.Surface(self.surface_parameters)
        self.surface.fill('Light Green')
        self.map.update_surface_parameters(self.surface_parameters, self.surface_destination)