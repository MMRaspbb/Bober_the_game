import pygame

class Map:
    def __init__(self, surface_parameters: tuple[int, int], surface_destination: tuple[int, int]) -> None:
        self.lower_left = [-360, -270]
        self.upper_right = [360, 270]
        self.visible_lower_left = [-36, -27]
        self.visible_upper_right = [36, 27]
        self.position_color = {
            (0, 0): "Red",
            (1, 1): "Green",
            (2, 2): "Blue",
            (3, 3): "Yellow"
        }
        self.side = 0
        self.vertical_move_sum = 0
        self.horizontal_move_sum = 0
        self.width, self.height = surface_parameters
        self.surface_destination = surface_destination
        self.mesh = [[pygame.rect.Rect(0, 0, 0, 0) for _ in range(self.visible_upper_right[0] - self.visible_lower_left[0])] for _ in range(self.visible_upper_right[1] - self.visible_lower_left[1])]
        self.__update_mesh()

    def __update_mesh(self) -> None:
        self.side = self.width / (self.visible_upper_right[0] - self.visible_lower_left[0])
        for i in range(self.visible_lower_left[1], self.visible_upper_right[1]):
            for j in range(self.visible_lower_left[0], self.visible_upper_right[0]):
                self.mesh[i][j] = pygame.rect.Rect((j + self.visible_upper_right[0]) *
                                                    self.side, (i + self.visible_upper_right[1]) * self.side,
                                                    self.side,
                                                    self.side)

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill('Light Green')
        for i in range(self.visible_lower_left[1], self.visible_upper_right[1]):
            for j in range(self.visible_lower_left[0], self.visible_upper_right[0]):
                if (i, j) in self.position_color:
                    print(i+ self.visible_upper_right[1], j + self.visible_upper_right[0])
                    # TODO: fix self.mest index error
                    pygame.draw.rect(surface, self.position_color[(i, j)], self.mesh[i - self.visible_upper_right[0]][j - self.visible_upper_right[1]])

    def move_map(self, diff_x: int, diff_y: int) -> None:
        self.horizontal_move_sum += diff_x
        self.vertical_move_sum += diff_y
        side = int(self.side)
        tiles_to_move = 0
        if self.horizontal_move_sum >= side:
            tiles_to_move = self.horizontal_move_sum // side
            self.horizontal_move_sum -= tiles_to_move * side
            self.visible_lower_left[0] += tiles_to_move
            self.visible_upper_right[0] += tiles_to_move
        elif self.horizontal_move_sum <= -side:
            tiles_to_move = -self.horizontal_move_sum // side
            self.horizontal_move_sum += tiles_to_move * side
            self.visible_lower_left[0] -= tiles_to_move
            self.visible_upper_right[0] -= tiles_to_move
        
        if self.vertical_move_sum >= side:
            tiles_to_move = self.vertical_move_sum // side
            self.vertical_move_sum -= tiles_to_move * side
            self.visible_lower_left[1] += tiles_to_move
            self.visible_upper_right[1] += tiles_to_move
        elif self.vertical_move_sum <= -side:
            tiles_to_move = -self.vertical_move_sum // side
            self.vertical_move_sum += tiles_to_move * side
            self.visible_lower_left[1] -= tiles_to_move
            self.visible_upper_right[1] -= tiles_to_move

    def update_surface_parameters(self, surface_parameters: tuple, surface_destination: tuple) -> None:
        self.width, self.height = surface_parameters
        self.surface_destination = surface_destination
        self.__update_mesh()

    def expand_borders(self):
        self.lower_left[0] -= 4
        self.lower_left[1] -= 3
        self.upper_right[0] += 4
        self.upper_right[1] += 3

