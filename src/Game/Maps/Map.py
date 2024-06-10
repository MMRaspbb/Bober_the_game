import copy

import pygame
from ..MapElements.River import River
from ..MapElements.Bobrs.RegularBobr import RegularBobr
from ..MapElements.Bobrs.GathererBobr import GathererBobr
from ..MapElements.Bobrs.BuilderBobr import BuilderBobr
from ..MapElements.Bobrs.GardenerBobr import GardenerBobr
from ..MapElements.resources.ForestResource import ForestResource
from ..MapElements.resources.StoneResource import StoneResource
from ..MapElements.resources.FoodResource import FoodResource
from ..MapElements.buildings.Dam import Dam
from ..Maps.MapDirection import MapDirection
from ..Utils.RiverNodesCreator import RiverNodesCreator

from ..MapElements.buildings.Base import Base

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
        self.base_selected = False
        self.selected_builder = None
        self.elements_to_draw = []

        # BOBRS
        self.bobrs = [GathererBobr("G1", self.middle[0] - 15, self.middle[1] - 10),
                      GathererBobr("G2", self.middle[0] + 15, self.middle[1] - 10),
                      GardenerBobr("G3", self.middle[0] - 15, self.middle[1] + 10),
                      BuilderBobr("G4", self.middle[0] + 15, self.middle[1] + 10)]
        
        # PRICES
        self.bobr_price = {"food": 5}
        self.dam_price = {"wood": 10}
        self.farm_price = {"wood": 10, "stone": 5}

        self.price_over_coursor = None
        # DAMS
        self.dams = []

        self.skeleton_dam = None
        self.skeleton_farm = None

        # BUILDINGS
        self.buildings = []
        self.base = Base(self.middle[0], self.middle[1])
        self.buildings.append(self.base)
        

        # RIVERS
        self.rivers = []

        # RESOURCES
        self.resources = []

        self.resources.append(ForestResource(self.middle[0], self.middle[1] + 20))
        self.resources.append(StoneResource(self.middle[0] + 10, self.middle[1] + 10))
        self.resources.append(FoodResource(self.middle[0] - 10, self.middle[1] - 10))

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
            "wood": 999,
            "stone": 999,
            "food": 999
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
        for river in self.rivers:
            for river_x, river_y, river_img in river.get_representation():
                if (river_x >= mid_i_start and river_x < mid_i_end and river_y >= mid_j_start and river_y < mid_j_end):
                    self.__draw_image(surface, river_img, river_x, river_y, offset_x, offset_y)

        for dam in self.dams:
            for dam_x, dam_y, dam_img in dam.get_representation():
                if (dam_x >= mid_i_start and dam_x < mid_i_end and dam_y >= mid_j_start and dam_y < mid_j_end):
                    self.__draw_image(surface, dam_img, dam_x, dam_y, offset_x, offset_y)

        for resource in self.resources:
            for resource_x, resource_y, resource_img in resource.get_representation():
                if (resource_x >= mid_i_start and resource_x < mid_i_end and resource_y >= mid_j_start and resource_y < mid_j_end):
                    self.__draw_image(surface, resource_img, resource_x, resource_y, offset_x, offset_y)

        base_x, base_y, base_img = self.base.get_representation()[0]
        if (base_x >= mid_i_start and base_x < mid_i_end and base_y >= mid_j_start and base_y < mid_j_end):
            base_img = pygame.transform.scale(base_img, (self.side * 8, self.side * 8))
            self.__draw_image(surface, base_img, base_x, base_y, offset_x, offset_y, base_img.get_width() // 2, base_img.get_height() // 2)


        self.draw_base_menu()

        skeletons_to_draw = self.draw_skeleton()    
        for skeleton in skeletons_to_draw:
            skeleton_x, skeleton_y, skeleton_img = skeleton
            if (skeleton_x >= mid_i_start and skeleton_x < mid_i_end and skeleton_y >= mid_j_start and skeleton_y < mid_j_end):
                self.__draw_image(surface, skeleton_img, skeleton_x, skeleton_y, offset_x, offset_y, 1)


        wood_text = pygame.font.SysFont('Arial', 20).render(f"Wood: {self.curr_resources['wood']}", True, (0, 0, 0))
        stone_text = pygame.font.SysFont('Arial', 20).render(f"Stone: {self.curr_resources['stone']}", True, (0, 0, 0))
        food_text = pygame.font.SysFont('Arial', 20).render(f"Food: {self.curr_resources['food']}", True, (0, 0, 0))
        surface.blit(wood_text, (10, 10))
        surface.blit(stone_text, (10, 30))
        surface.blit(food_text, (10, 50))

        for bobr in self.bobrs:
            pos, img = bobr.get_representation()
            if (pos[0] >= mid_i_start and pos[0] < mid_i_end and pos[1] >= mid_j_start and pos[1] < mid_j_end):
                rect = self.mesh[pos[0]][pos[1]].copy()
                rect.move_ip(-offset_x, -offset_y)
                img = pygame.transform.scale(img, (self.side * 4, self.side * 4))
                self.__draw_image(surface, img, pos[0], pos[1], offset_x, offset_y, img.get_width() // 2, img.get_height() // 2)
        

        self.draw_price(surface)

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
                if resource.get_name in ["wood", "stone"] and resource.is_position_in_resource(bobr.position[0], bobr.position[1]) and isinstance(bobr, GathererBobr):
                    resource.set_bobr(bobr)
                    self.curr_resources[resource.get_name] += resource.adjust_work_counter()
                    break
                elif resource.get_name == "food" and resource.is_position_in_resource(bobr.position[0], bobr.position[1]) and isinstance(bobr, GardenerBobr):
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
        if self.base.is_position_in_base(i, j):
            self.base_selected = True
            return None
        else:
            self.base_selected = False

        for resource in self.resources:
            if resource.is_position_in_resource(i, j):
                if resource.bobr_in():
                    resource.bobr.is_selected = True
                    return resource.bobr
        
        for element in self.__map_elements():
            if element.position == (i, j):
                element.is_selected = True
                if isinstance(element, BuilderBobr):
                    self.selected_builder = element

                return element
            
        print(self.selected_builder)
        return None
            
            

            

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
            self.rivers[i].push_river_state()
   

    def place_skeleton(self):
        if self.skeleton_dam is not None:
            for river in self.rivers:
                collide_point = river.contains_or_touches(self.skeleton_dam.position)
                if collide_point != -1 and self.river_reroute(river, self.skeleton_dam.position, self.skeleton_dam):
                    self.dams.append(copy.deepcopy(self.skeleton_dam))
                    break
        self.skeleton_dam = None
        if self.skeleton_farm is not None and self.__pay(self.farm_price):
            self.resources.append(copy.deepcopy(self.skeleton_farm))
        self.skeleton_farm = None
        self.price_over_coursor = None
 
    def __pay(self, price: dict) -> bool:
        for resource, amount in price.items():
            if self.curr_resources[resource] < amount:
                return False
        for resource, amount in price.items():
            self.curr_resources[resource] -= amount
        return True
    
    def river_reroute(self, river: River,  collide_point: tuple[int, int], dam: Dam) -> bool:
        #river = self.find_dominant_river(collide_point)
        river_points = river.get_river_points()
        collide_index = river.contains_or_touches(collide_point)
        print(collide_index)
        previous_river_point = river_points[collide_index - 1]

        vector = (river_points[collide_index][0] - previous_river_point[0], river_points[collide_index][1] - previous_river_point[1])
        dam_orientation = dam.get_orientation()
        if vector == dam_orientation.value or vector == dam_orientation.get_opposite(dam_orientation) or vector == dam_orientation.get_double_next(dam_orientation).value or vector == dam_orientation.get_double_previous(dam_orientation).value or not self.__pay(self.dam_price):
            return False
        bounce_vector = dam.get_bounced_direction(vector).value
        end_x = river_points[collide_index][0]
        end_y = river_points[collide_index][1]
        while end_x != 0 and end_x != self.full_map_width and end_y != 0 and end_y != self.full_map_height:
            end_x += bounce_vector[0]
            end_y += bounce_vector[1]

        new_river_points = River.delineate_river((river_points[collide_index][0], river_points[collide_index][1]), (end_x, end_y), 10, 1)

        river.set_river_state(collide_index)
        river.modify_river_end_points(new_river_points, 0)

        # self.reroute_river_subs_and_fix_dominant(river, collide_point, new_river_points)
        return True

    def draw_base_menu(self):
        if self.base_selected:
            self.selected_button = None
            buttons = self.base.draw_base_menu(self.width, self.bobr_price)  # Draw the menu outside the loop
            pygame.display.update()  # Update the display after drawing the menu
            while True:
                event = pygame.event.wait()  # Wait for an event
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Check if the left mouse button was clicked
                    x, y = event.pos
                    button_clicked = False
                    for i, button in enumerate(buttons):
                        if button.collidepoint(x, y):
                            print(f'Button {i} was clicked')
                            self.selected_button = i  # Store the index of the selected button
                            button_clicked = True
                            self.base_selected = False  # Close the menu if a button was clicked
                            break
                    if not button_clicked:
                        self.base_selected = False  # Close the menu if clicked outside
                    pygame.display.update()  # Update the display after an event
                    if not self.base_selected:
                          # Exit the loop
                        break
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            if self.__pay(self.bobr_price) and self.selected_button is not None:
                match self.selected_button:
                    case 0: # Builder
                        self.bobrs.append(BuilderBobr("builder", self.base.position[0] + 5, self.base.position[1]))
                    case 1:
                        self.bobrs.append(GathererBobr("gatherer", self.base.position[0] + 5, self.base.position[1]))
                    case 2:
                        self.bobrs.append(GardenerBobr("gardener", self.base.position[0] + 5, self.base.position[1]))
    
    def draw_skeleton(self):
        skeletons_to_draw = []
        if self.selected_builder is not None:
            x, y = pygame.mouse.get_pos()
            x -= self.surface_destination[0]
            y -= self.surface_destination[1]
            i, j = self.convert_pixel_to_tile(x, y)
            if self.__calculate_distance_in_tiles((i, j), self.selected_builder.position) <= 5:
                over_river = False
                self.skeleton_farm = FoodResource(i, j)
                farm_representation = self.skeleton_farm.get_representation()
                self.skeleton_farm = None
                for river in self.rivers:
                    if river.contains_or_touches((i, j)) >= 0:
                        over_river = True
                        if self.skeleton_dam is None or self.skeleton_dam.position != (i, j):
                            self.skeleton_dam = Dam(i, j)
                            price_string = ""
                            for price_name, price in self.dam_price.items():
                                price_string += f"{price_name[0].capitalize()}: {price} "
                            self.price_over_coursor = price_string
                            break
                # check if any of the farm tiles are over the river and does not collide with any other resource
                if not any([river.contains_or_touches((x, y)) >= 0 for x, y, _ in farm_representation]) and not over_river:
                    if self.__check_if_farm_colides_with_resource(farm_representation):
                        if self.skeleton_farm is None or self.skeleton_farm.position != (i, j):
                            self.skeleton_farm = FoodResource(i, j)
                            price_string = ""
                            for price_name, price in self.farm_price.items():
                                price_string += f"{price_name[0].capitalize()}: {price} "
                            self.price_over_coursor = price_string
                if not over_river:
                    self.skeleton_dam = None
            else:
                self.skeleton_dam = None
                self.skeleton_farm = None
                self.price_over_coursor = None
                
        if self.skeleton_dam is not None:
            skeletons_to_draw += self.skeleton_dam.get_representation()

        elif self.skeleton_farm is not None:
            skeletons_to_draw += self.skeleton_farm.get_representation()

        return skeletons_to_draw

    def draw_price(self, surface: pygame.Surface):
        if self.price_over_coursor is not None:
            price_text = pygame.font.SysFont('Arial', 20).render(self.price_over_coursor, True, (0, 0, 0))
            surface.blit(price_text, (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1] - 30))

    def __check_if_farm_colides_with_resource(self, farm_representation: list) -> bool:
        for x, y, _ in farm_representation:
            if any([resource.is_position_in_resource(x, y) for resource in self.resources]):
                return False
        return True
    def __draw_image(self, surface: pygame.Surface, image: pygame.Surface, x: int, y: int, offset_x: int, offset_y: int, rect_offset_x = 0, rect_offset_y = 0) -> None:
        rect = self.mesh[x][y].copy()
        rect.move_ip(-offset_x, -offset_y)
        surface.blit(image, (rect.topleft[0] - rect_offset_x, rect.topleft[1] - rect_offset_y))
      