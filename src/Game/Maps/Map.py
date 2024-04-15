import pygame

class Map:
    def __init__(self, surface_parameters: tuple[int, int], surface_destination: tuple[int, int]) -> None:
        self.full_map_width = 4 * 500
        self.full_map_height = 3 * 500
        # visible map width and height
        self.width, self.height = surface_parameters
        # create mesh of width 20 pixels and height 20 pixels
        # that will devide full_map
        self.tile_num_horizontal = 60
        self.tile_num_vertical = self.tile_num_horizontal *(3/4)
        self.side = self.width // self.tile_num_horizontal
        self.mesh = [[pygame.rect.Rect(i * self.side, j * self.side, self.side, self.side) 
                      for j in range(self.full_map_height // self.side)] 
                      for i in range(self.full_map_width // self.side)]
        # calculate index of the mesh tile that is the middle of the map
        self.middle = [self.full_map_width // (2 * self.side), self.full_map_height // (2 * self.side)]
        self.current_map_upper_left = [self.middle[0] - 120, self.middle[1] - 90]
        self.current_map_lower_right = [self.middle[0] + 120, self.middle[1] + 90]
        # create map that will make middle of the map black and around it white
        self.colors = {tuple(self.middle): 'Black',
                       (self.middle[0] - 1, self.middle[1]): 'White',
                       (self.middle[0] + 1, self.middle[1]): 'White',
                       (self.middle[0], self.middle[1] - 1): 'White',
                       (self.middle[0], self.middle[1] + 1): 'White',
                       (self.middle[0] - 1, self.middle[1] - 1): 'White',
                       (self.middle[0] - 1, self.middle[1] + 1): 'White',
                       (self.middle[0] + 1, self.middle[1] - 1): 'White',
                       (self.middle[0] + 1, self.middle[1] + 1): 'White',
                       (self.middle[0] - 31, self.middle[1] - 23): 'Red',
                       (self.middle[0] - 31, self.middle[1] + 22): 'Blue',
                       (self.middle[0] + 30, self.middle[1] - 23): 'Pink',
                       (self.middle[0] + 30, self.middle[1] + 22): 'Yellow',
                       (0,0): 'Black',
                       (self.full_map_width // self.side - 1, self.full_map_height // self.side - 1): 'Black',
                       (0, self.full_map_height // self.side - 1): 'Black',
                       (self.full_map_width // self.side - 1, 0): 'Black'}
        self.horizontal_move_sum = 0
        self.vertical_move_sum = 0
        self.__update_mesh()

    def __update_mesh(self) -> None:
        self.side = int(self.width // self.tile_num_horizontal)
        self.mesh = [[pygame.rect.Rect(i * self.side, j * self.side, self.side, self.side) 
                      for j in range(self.full_map_height // self.side)] 
                      for i in range(self.full_map_width // self.side)]
        

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill('Light Green')
        # Calculate the indices of the middle portion of the map
        mid_i_start = max(self.middle[0] - surface.get_width() // self.side, 0)
        mid_i_end = min(self.middle[0] + surface.get_width() // self.side, self.full_map_width // self.side)
        mid_j_start = max(self.middle[1] - surface.get_height() // self.side, 0)
        mid_j_end = min(self.middle[1] + surface.get_height() // self.side, self.full_map_height // self.side) 

        # Calculate the offset to the middle of the map
        offset_x = self.middle[0] * self.side - surface.get_width() // 2
        offset_y = self.middle[1] * self.side - surface.get_height() // 2

        # Iterate over the tiles in the middle portion of the map
        for i in range(mid_i_start, mid_i_end):
            for j in range(mid_j_start, mid_j_end):
                if (i, j) in self.colors:
                    rect = self.mesh[i][j].copy()  # Make a copy of the rectangle to avoid modifying the original

                    # Adjust the position of the rectangle by the offset to the middle of the map
                    rect.move_ip(-offset_x, -offset_y)

                    color = self.colors.get((i, j))
                    pygame.draw.rect(surface, color, rect)

    def move_map(self, diff_x: int, diff_y: int) -> None:
        # print(diff_x, diff_y)
        # print(self.middle)
        self.horizontal_move_sum += diff_x
        self.vertical_move_sum += diff_y
        side = int(self.side)
        # if abs(self.horizontal_move_sum) >= side:
        #     tiles_to_move = self.horizontal_move_sum // side
        #     if tiles_to_move + self.middle[0] >= 0 and self.middle[0] <= self.full_map_width // side:
        #         self.horizontal_move_sum -= tiles_to_move * side
        #         self.middle[0] -= tiles_to_move
        #         if self.middle[0] < 0:
        #             self.middle[0] = 0
        #         elif self.middle[0] >= self.full_map_height // side:
        #             self.middle[0] = self.full_map_height // side
        # if abs(self.vertical_move_sum) >= side:
        #     tiles_to_move = self.vertical_move_sum // side
        #     if tiles_to_move + self.middle[1] >= 0 and self.middle[1] <= self.full_map_height // self.side:
        #         self.vertical_move_sum -= tiles_to_move * side
        #         self.middle[1] -= tiles_to_move
        #         if self.middle[1] < 0:
        #             self.middle[1] = 0
        #         elif self.middle[1] >= self.full_map_height // self.side:
        #             self.middle[1] = self.full_map_height // self.side
        #TODO : rzucić middle na int
        if abs(self.horizontal_move_sum) >= side:
            tiles_to_move = int(self.horizontal_move_sum // side)
            self.middle[0] -= tiles_to_move
            self.horizontal_move_sum -= tiles_to_move * side
            if self.middle[0] < self.current_map_upper_left[0] + self.tile_num_horizontal // 2:
                self.middle[0] = int(self.current_map_upper_left[0] + self.tile_num_horizontal // 2)
            elif self.middle[0] > self.current_map_lower_right[0] - self.tile_num_horizontal // 2:
                self.middle[0] = int(self.current_map_lower_right[0] - self.tile_num_horizontal // 2)
        elif abs(self.vertical_move_sum) >= side:
            tiles_to_move = int(self.vertical_move_sum // side)
            self.middle[1] -= tiles_to_move
            self.vertical_move_sum -= tiles_to_move * side
            if self.middle[1] < self.current_map_upper_left[1] + self.tile_num_vertical // 2:
                self.middle[1] = int(self.current_map_upper_left[1] + self.tile_num_vertical // 2)
            elif self.middle[1] > self.current_map_lower_right[1] - self.tile_num_vertical // 2:
                self.middle[1] = int(self.current_map_lower_right[1] - self.tile_num_vertical // 2)
    def update_surface_parameters(self, surface_parameters: tuple, surface_destination: tuple) -> None:
        self.width, self.height = surface_parameters
        self.surface_destination = surface_destination
        self.__update_mesh()

    def expand_borders(self):
        self.lower_left[0] -= 4
        self.lower_left[1] -= 3
        self.upper_right[0] += 4
        self.upper_right[1] += 3

