import pygame

class Map:
    # TODO: przekazac aktualna wys,szer oraz polozenie backgroundu
    lower_left = [-360, -270]
    upper_right = [360, 270]
    visible_lower_left = [-36, -27]
    visible_upper_right = [36, 27]
    position_color = dict()

    position_color[(0, 0)] = "Red"
    position_color[(1, 1)] = "Green"
    position_color[(2, 2)] = "Blue"
    position_color[(3, 3)] = "Yellow"

    def __init__(self, surface_parameters: tuple[int, int], surface_destination: tuple[int, int]) -> None:
        self.width, self.height = surface_parameters
        self.surface_destination = surface_destination
        self.mesh = [[pygame.rect.Rect(0, 0, 0, 0) for _ in range(self.visible_upper_right[0] - self.visible_lower_left[0])] for _ in range(self.visible_upper_right[1] - self.visible_lower_left[1])]
        self.__update_mesh()

    def __update_mesh(self) -> None:
        side = self.width / (self.visible_upper_right[0] - self.visible_lower_left[0])
        for i in range(self.visible_lower_left[1], self.visible_upper_right[1]):
            for j in range(self.visible_lower_left[0], self.visible_upper_right[0]):
                self.mesh[i][j] = pygame.rect.Rect((j + self.visible_upper_right[0]) * side, (i + self.visible_upper_right[1]) * side, side, side)

    def draw(self, surface: pygame.Surface) -> None:
        for i in range(self.visible_lower_left[1], self.visible_upper_right[1]):
            for j in range(self.visible_lower_left[0], self.visible_upper_right[0]):
                if (i, j) in self.position_color:
                    pygame.draw.rect(surface, self.position_color[(i, j)], self.mesh[i + self.visible_upper_right[1]][j + self.visible_upper_right[0]])


    def update_surface_parameters(self, surface_parameters: tuple, surface_destination: tuple) -> None:
        self.width, self.height = surface_parameters
        self.surface_destination = surface_destination
        self.__update_mesh()

    def expand_borders(self):
        self.lower_left[0] -= 4
        self.lower_left[1] -= 3
        self.upper_right[0] += 4
        self.upper_right[1] += 3

