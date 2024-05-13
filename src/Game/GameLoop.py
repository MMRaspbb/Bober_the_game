import pygame
from .Maps.Map import Map
from .Utils.PathFinder import PathFinder
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
    pathfinder = PathFinder(map)

    mouse_right_down = False
    mouse_left_clicked = False
    mouse_left_down = False
    selected_elements = []

    def initialize(self):
        frames_passed = 0
        while True:
            self.__event_handler()
            self.screen.blit(self.surface, self.surface_destination)

            # maybe temporary update:
            self.map.update_rivers()

            self.map.draw(self.surface)
            self.map.move_bobrs()
            if frames_passed % 1 == 0:
                self.map.expand_borders()



            pygame.display.update()
            self.clock.tick(30)
            frames_passed += 1


    def __event_handler(self) -> None:
        for event in pygame.event.get():
            self.__on_drag_event(event)
            self.__on_area_select_event(event)
            self.__on_select_event(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.VIDEORESIZE:
                self.fix_surface_position()

    def __on_drag_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                self.mouse_right_down = True
        if event.type == pygame.MOUSEMOTION:
            if self.mouse_right_down:
                self.map.move_map(event.rel[0], event.rel[1])
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                self.mouse_right_down = False

    def __on_area_select_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if not self.mouse_left_down:
                    self.elements_start_pos = event.pos
                    self.mouse_left_down = True
                if self.selected_elements:
                    move_vector = (event.pos[0] - self.elements_end_pos[0], event.pos[1] - self.elements_end_pos[1])
                    for element in self.selected_elements:
                        path = self.pathfinder.find_path(element.position, (element.position[0] + move_vector[0], element.position[1] + move_vector[1]))
                        element.set_path(path)
                        element.is_selected = False
                    self.selected_elements = []

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if event.pos != self.element_start_pos and self.mouse_left_down:
                    self.elements_end_pos = event.pos
                    self.selected_elements = self.map.get_area_selection(self.elements_start_pos, self.elements_end_pos)
                    self.mouse_left_down = False
                else:
                    self.mouse_left_down = False

    def __on_select_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if not self.mouse_left_clicked:
                    self.element_start_pos = event.pos
                    element = self.map.get_selection(event.pos[0], event.pos[1])
                    if element: 
                        self.mouse_left_clicked = True
                        self.selected_element = element
                else:
                    self.element_end_pos = event.pos
                    path = self.pathfinder.find_path(self.element_start_pos, self.element_end_pos)
                    self.selected_element.set_path(path)
                    self.selected_element.is_selected = False
                    self.mouse_left_clicked = False
                    self.selected_element = None
        
 

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