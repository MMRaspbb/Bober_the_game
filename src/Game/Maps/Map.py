import pygame

class Map:
    def __init__(self, surface_parameters: tuple[int, int], surface_destination: tuple[int, int]) -> None:
        self.full_map_width = 4 * 1000
        self.full_map_height = 3 * 1000
        # visible map width and height
        self.width, self.height = surface_parameters
        # create mesh of width 20 pixels and height 20 pixels
        # that will devide full_map
        self.side = self.width // 20
        self.mesh = [[pygame.rect.Rect(i * self.side, j * self.side, self.side, self.side) 
                      for j in range(self.full_map_height // self.side)] 
                      for i in range(self.full_map_width // self.side)]
        # calculate index of the mesh tile that is the middle of the map
        self.middle = (self.full_map_width // (2 * self.side), self.full_map_height // (2 * self.side))
        # create map that will make middle of the map black and around it white
        self.colors = {self.middle: 'Black',
                       (self.middle[0] - 1, self.middle[1]): 'White',
                       (self.middle[0] + 1, self.middle[1]): 'White',
                       (self.middle[0], self.middle[1] - 1): 'White',
                       (self.middle[0], self.middle[1] + 1): 'White',
                       (self.middle[0] - 1, self.middle[1] - 1): 'White',
                       (self.middle[0] - 1, self.middle[1] + 1): 'White',
                       (self.middle[0] + 1, self.middle[1] - 1): 'White',
                       (self.middle[0] + 1, self.middle[1] + 1): 'White'}
    
        #self.__update_mesh()

    def __update_mesh(self) -> None:
        self.side = int(self.width // 20)
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
        offset_x = self.middle[0] * self.side - 800 // 2
        offset_y = self.middle[1] * self.side - 600 // 2

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

