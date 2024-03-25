class Map:
    lower_left = [-36, -27]
    upper_right = [-36, 27]
    grass = dict()
    def expand_borders(self):
        self.lower_left[0] -= 4
        self.lower_left[1] -= 3
        self.upper_right[0] += 4
        self.upper_right[1] += 3

