from ..Maps.MapDirection import MapDirection

class Rotatable():
    def __init__(self, orientation: MapDirection):
        self.orientation = orientation

    def rotate_clockwise(self):
        self.orientation = self.orientation.next(self.orientation)

    def rotate_counter_clockwise(self):
        self.orientation = self.orientation.previous(self.orientation)

    def get_orientation(self):
        return self.orientation