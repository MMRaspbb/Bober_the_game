import pygame
from sys import exit
from pygame.locals import RESIZABLE

class GameLoop:
    screen = pygame.display.set_mode((800, 600), RESIZABLE)
    pygame.display.set_caption("Bober")
    clock = pygame.time.Clock()

    game_window_parameters = (800, 600)
    background = pygame.Surface(game_window_parameters)
    background_destination = (0,0)
    background.fill('Light Green')

    def initialize(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.VIDEORESIZE:
                    self.fix_background_position()
            self.screen.blit(self.background, self.background_destination)

            pygame.display.update()
            self.clock.tick(60)
    def fix_background_position(self):
        width, height = pygame.display.get_surface().get_size()
        normalized_width = width / 4
        normalized_height = height / 3
        if normalized_width > normalized_height:
            self.game_window_parameters = (normalized_height * 4, height)
            self.background_destination = (width / 2 - normalized_height * 2, 0)
        else:
            self.game_window_parameters = (width, normalized_width * 4)
            self.background_destination = (0, height / 2 - normalized_width * 2)
        self.background = pygame.Surface(self.game_window_parameters)
        self.background.fill('Light Green')