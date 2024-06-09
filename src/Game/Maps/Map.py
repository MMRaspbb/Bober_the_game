import copy

import pygame
from ..MapElements.River import River
from ..MapElements.Bobrs.RegularBobr import RegularBobr
from ..MapElements.Bobrs.GathererBobr import GathererBobr
from ..MapElements.Bobrs.BuilderBobr import BuilderBobr
from ..MapElements.resources.ForestResource import ForestResource
from ..MapElements.resources.StoneResource import StoneResource
from ..MapElements.buildings.Dam import Dam

class Map:
    def __init__(self, surface_parameters: tuple[int, int], surface_destination: tuple[int, int]) -> None:
        pygame.font.init()
        # visible map width and height
        self.surface_destination = surface_destination
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

        self.selected_builder = None

        # BOBRS
        self.bobrs = [GathererBobr("G1", self.middle[0] - 15, self.middle[1] - 10),
                      GathererBobr("G2", self.middle[0] + 15, self.middle[1] - 10),
                      GathererBobr("G3", self.middle[0] - 15, self.middle[1] + 10),
                      BuilderBobr("G4", self.middle[0] + 15, self.middle[1] + 10)]
        
        # DAMS
        self.dams = []

        self.skeleton_dam = None

        # BUILDINGS
        self.buildings = []

        # RIVERS
        self.rivers = []

        # RESOURCES
        self.resources = []

        self.resources.append(ForestResource(self.middle[0], self.middle[1]))
        self.resources.append(StoneResource(self.middle[0] + 10, self.middle[1] + 10))

        self.rivers = []
        river1 = River([0, 0], [self.full_map_width, self.full_map_height])
        self.rivers.append(river1)
        river2 = River([0, self.full_map_height], [self.full_map_width, 0])
        self.rivers.append(river2)
        # river3 = River([self.full_map_width, 0], [0, self.full_map_height])
        # self.rivers.append(river3)
        river1.river_state = 400
        river2.river_state = 400

        self.curr_resources = {
            "wood": 0,
            "stone": 0,
        }

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
        elements_to_draw = []
        for river in self.rivers:
            elements_to_draw += river.get_representation()

        for dam in self.dams:
            elements_to_draw += dam.get_representation()

        for resource in self.resources:
            elements_to_draw += resource.get_representation()

        for element in self.__map_elements():
            elements_to_draw += [element.get_representation()]

        if self.selected_builder is not None:
            x, y = pygame.mouse.get_pos()
            x -= self.surface_destination[0]
            y -= self.surface_destination[1]
            i, j = self.convert_pixel_to_tile(x, y)
            if self.__calculate_distance_in_tiles((i, j), self.selected_builder.position) <= 5:
                over_river = False
                for river in self.rivers:
                    if river.contains_or_touches((i, j)) >= 0:
                        over_river = True
                        if self.skeleton_dam is None or self.skeleton_dam.position != (i, j):
                            print(self.skeleton_dam)
                            self.skeleton_dam = Dam(i, j)
                            break
                if not over_river:
                    print("else block")
                    self.skeleton_dam = None

    
            
        if self.skeleton_dam is not None:
            elements_to_draw += self.skeleton_dam.get_representation()

        for (x, y, color) in elements_to_draw:
            if (x >= mid_i_start and x < mid_i_end and y >= mid_j_start and y < mid_j_end):
                rect = self.mesh[x][y].copy()  # Make a copy of the rectangle to avoid modifying the original

                # Adjust the position of the rectangle by the offset to the middle of the map
                rect.move_ip(-offset_x, -offset_y)
                pygame.draw.rect(surface, color, rect)


        wood_text = pygame.font.SysFont('Arial', 20).render(f"Wood: {self.curr_resources['wood']}", True, (0, 0, 0))
        stone_text = pygame.font.SysFont('Arial', 20).render(f"Stone: {self.curr_resources['stone']}", True, (0, 0, 0))
        surface.blit(wood_text, (10, 10))
        surface.blit(stone_text, (10, 30))

    def rotate_skeleton_dam(self) -> int:
        if self.skeleton_dam is not None:
            self.skeleton_dam.rotate_clockwise()
        
    def __calculate_distance_in_tiles(self, point1: list[int], point2: list[int]) -> int:
        return int(((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5)

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

    def __map_elements(self) -> list:
        elements = self.bobrs
        return elements
    
    
    def update_bobrs(self) -> None:
        for bobr in self.bobrs:
            bobr.move()
        for resource in self.resources:
            for bobr in self.bobrs:
                if resource.is_position_in_resource(bobr.position[0], bobr.position[1]) and isinstance(bobr, GathererBobr):
                    resource.set_bobr(bobr)
                    self.curr_resources[resource.get_name] += resource.adjust_work_counter()
                    break
            else: 
                resource.set_bobr(None)      

    def convert_pixel_to_tile(self, x: int, y: int) -> tuple[int, int]:
        # calculate tile indices from pixel coordinates in regards to the middle of the map
        i = int((x + self.middle[0] * self.side) // self.side - self.tile_num_horizontal // 2 - 1)
        j = int((y + self.middle[1] * self.side) // self.side - self.tile_num_vertical // 2 - 1)
        return (i, j)

    def get_selection(self, x: int, y: int) -> object:
        x -= self.surface_destination[0]
        y -= self.surface_destination[1]
        (i, j) = self.convert_pixel_to_tile(x, y)
        for resource in self.resources:
            if resource.is_position_in_resource(i, j):
                if resource.bobr_in():
                    print("SELECTED BOBR IN RESOURCE")
                    resource.bobr.is_selected = True
                    return resource.bobr
        


        for element in self.__map_elements():
            if element.position == (i, j):
                element.is_selected = True
                if isinstance(element, BuilderBobr):
                    self.selected_builder = element
                return element
            

            

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
           
    def update_rivers(self):
        for i in range(len(self.rivers)):
            if self.rivers[i].push_river_state():
                pushed_point = self.rivers[i].get_pushed_point()
                for j in range(len(self.rivers)):
                    if j == i:
                        continue
                    point_position = self.rivers[j].contains_or_touches(pushed_point)
                    if point_position >= 0 and self.rivers[j].is_subriver_from > point_position:
                        dominant_river_points = self.rivers[j].get_river_points()
                        self.rivers[i].modify_river_end_points(dominant_river_points, point_position)
                        self.rivers[i].set_subriver_state(pushed_point)
    def place_skeleton_dam(self):
        print("I TRIED PLACING A DAM")
        if self.skeleton_dam is not None:
            self.dams.append(copy.deepcopy(self.skeleton_dam))
        self.skeleton_dam = None
    # def __calculate_new_river_end(self, river1: River, river2: River, colision_point: tuple[int, int]) -> tuple[int, int]:
    #     #not used could be usefull for bober dams
    #     end1 = river1.get_default_end()
    #     end2 = river2.get_default_end()
    #     versor1 = (end1[0] - colision_point[0], end1[1] - colision_point[1])
    #     versor2 = (end2[0] - colision_point[0], end2[1] - colision_point[1])
    #     bigger_parameter = versor1[0]
    #     if versor1[0] < versor1[1]:
    #         bigger_parameter = versor1[1]
    #     versor1 = (versor1[0] * river1.get_strength / bigger_parameter, versor1[1] * river1.get_strength / bigger_parameter)
    #     bigger_parameter = versor2[0]
    #     if versor2[0] < versor2[1]:
    #         bigger_parameter = versor2[1]
    #     versor2 = (versor2[0] * river2.get_strength / bigger_parameter, versor2[1] * river2.get_strength / bigger_parameter)
    #     combined_vector = (versor1[0] + versor2[0], versor1[1] + versor2[1])
    #     current_position = [colision_point[0], colision_point[1]]
    #     while(current_position[0] >= 0 and current_position[0] <= self.full_map_width and current_position[1] >= 0 and current_position[1] <= self.full_map_height):
    #         current_position[0] += combined_vector[0]
    #         current_position[1] += combined_vector[1]
    #     current_position[0] = int(current_position[0])
    #     current_position[1] = int(current_position[1])
    #     return current_position
    def river_reroute(self, river: River, collide_point: int, dam: Dam) -> None:
        river_points = river.get_river_points()
        previous_river_point = river_points[collide_point - 1]
        vector = (river_points[collide_point][0] - previous_river_point[0], river_points[collide_point][1] - previous_river_point[1])
        dam_orientation = dam.get_orientation()
        

        #tmp_river = River(collide_point)
        