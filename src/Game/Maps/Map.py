import pygame
from ..MapElements.River import River


class Map:
    def __init__(self, surface_parameters: tuple[int, int], surface_destination: tuple[int, int]) -> None:
        # visible map width and height
        self.width, self.height = surface_parameters
        # create mesh of width 20 pixels and height 20 pixels
        # that will devide full_map
        self.tile_num_horizontal = 60
        self.tile_num_vertical = self.tile_num_horizontal * (3 / 4)
        self.side = int(self.width // self.tile_num_horizontal)
        self.full_map_width = 4 * 200
        self.full_map_height = 3 * 200
        self.mesh = [[pygame.rect.Rect(i * self.side, j * self.side, self.side, self.side)
                      for j in range(self.full_map_height)]
                     for i in range(self.full_map_width)]
        # calculate index of the mesh tile that is the middle of the map
        self.middle = [self.full_map_width // 2, self.full_map_height // 2]
        self.current_map_upper_left = [self.middle[0] - 120, self.middle[1] - 90]
        self.current_map_lower_right = [self.middle[0] + 120, self.middle[1] + 90]
        # create map that will make middle of the map black and around it white
        self.colors = {}
        self.horizontal_move_sum = 0
        self.vertical_move_sum = 0
        self.rivers = []
        river1 = River([0, 0], [self.full_map_width, self.full_map_height], 1)
        self.rivers.append(river1)
        river2 = River([0, self.full_map_height], [self.full_map_width, 0], 1)
        self.rivers.append(river2)
        self.__update_mesh()

    def __update_mesh(self) -> None:
        self.side = int(self.width // self.tile_num_horizontal)
        self.mesh = [[pygame.rect.Rect(i * self.side, j * self.side, self.side, self.side)
                      for j in range(self.full_map_height)]
                     for i in range(self.full_map_width)]

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill('Light Green')
        visible_horizontal_tiles = surface.get_width() // self.side
        visible_vertical_tiles = surface.get_height() // self.side
        # Calculate the indices of the middle portion of the map
        mid_i_start = max(self.middle[0] - visible_horizontal_tiles, 0)
        mid_i_end = min(self.middle[0] + visible_horizontal_tiles, self.full_map_width)
        mid_j_start = max(self.middle[1] - visible_vertical_tiles, 0)
        mid_j_end = min(self.middle[1] + visible_vertical_tiles, self.full_map_height)

        # Calculate the offset to the middle of the map
        offset_x = self.middle[0] * self.side - surface.get_width() // 2
        offset_y = self.middle[1] * self.side - surface.get_height() // 2

        # Clearing the colors dictionary
        self.colors = {}
        # Drawing the objects on the map
        for river in self.rivers:
            river.draw(self.colors)

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
        self.horizontal_move_sum += diff_x
        self.vertical_move_sum += diff_y
        side = int(self.side)
        if abs(self.horizontal_move_sum) >= side:
            tiles_to_move = int(self.horizontal_move_sum // side)
            self.middle[0] -= tiles_to_move
            self.horizontal_move_sum -= tiles_to_move * side
            half_horizontal = self.tile_num_horizontal // 2
            if self.middle[0] < self.current_map_upper_left[0] + half_horizontal:
                self.middle[0] = int(self.current_map_upper_left[0] + half_horizontal)
            elif self.middle[0] > self.current_map_lower_right[0] - half_horizontal:
                self.middle[0] = int(self.current_map_lower_right[0] - half_horizontal)
        if abs(self.vertical_move_sum) >= side:
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
        if (self.current_map_upper_left[0] - 4 >= 0 and
                self.current_map_upper_left[1] - 3 >= 0 and
                self.current_map_lower_right[0] + 4 < self.full_map_width and
                self.current_map_lower_right[1] + 3 < self.full_map_height
        ):
            self.current_map_upper_left[0] -= 4
            self.current_map_upper_left[1] -= 3
            self.current_map_lower_right[0] += 4
            self.current_map_lower_right[1] += 3
            self.colors[(self.current_map_upper_left[0], self.current_map_upper_left[1])] = "Purple"
            self.colors[(self.current_map_lower_right[0], self.current_map_lower_right[1])] = "Purple"

    def update_rivers(self):
        rivers_to_append = []
        for i in range(len(self.rivers)):
            if self.rivers[i].push_river_state():
                pushed_point = self.rivers[i].get_pushed_point()
                for j in range(len(self.rivers)):
                    if j == i:
                        continue
                    point_position = self.rivers[j].contains_or_touches(pushed_point)
                    if point_position >= 0:
                        self.rivers[i].block_river()
                        self.rivers[j].set_river_limit(point_position)
                        beginning = [pushed_point[0], pushed_point[1]]
                        end = self.__calculate_new_river_end(self.rivers[i], self.rivers[j], pushed_point)
                        rivers_to_append.append(River(beginning,end, self.rivers[i].get_strength + self.rivers[j].get_strength))
        self.rivers += rivers_to_append
    def __calculate_new_river_end(self, river1: River, river2: River, colision_point: tuple[int, int]) -> tuple[int, int]:
        end1 = river1.get_default_end()
        end2 = river2.get_default_end()
        versor1 = (end1[0] - colision_point[0], end1[1] - colision_point[1])
        versor2 = (end2[0] - colision_point[0], end2[1] - colision_point[1])
        bigger_parameter = versor1[0]
        if versor1[0] < versor1[1]:
            bigger_parameter = versor1[1]
        versor1 = (versor1[0] * river1.get_strength / bigger_parameter, versor1[1] * river1.get_strength / bigger_parameter)
        bigger_parameter = versor2[0]
        if versor2[0] < versor2[1]:
            bigger_parameter = versor2[1]
        versor2 = (versor2[0] * river2.get_strength / bigger_parameter, versor2[1] * river2.get_strength / bigger_parameter)
        combined_vector = (versor1[0] + versor2[0], versor1[1] + versor2[1])
        current_position = [colision_point[0], colision_point[1]]
        while(current_position[0] >= 0 and current_position[0] <= self.full_map_width and current_position[1] >= 0 and current_position[1] <= self.full_map_height):
            current_position[0] += combined_vector[0]
            current_position[1] += combined_vector[1]
        current_position[0] = int(current_position[0])
        current_position[1] = int(current_position[1])
        return current_position