import numpy as np

class Coordinate2d:
    """Container class for 2d coordinates."""

    def __init__(self, x_part, y_part):
        self.__x = x_part
        self.__y = y_part

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_idx(self, idx):
        if idx == 0:
            return self.get_x()
        elif idx == 1:
            return self.get_y()
        else:
            raise ValueError("Unknown index value.")

    def __repr__(self):
        return "(X: {:8.2f}, Y: {:8.2f})".format(self.get_x(),
                                                 self.get_y())

    def __add__(self, other):
        if isinstance(other, Coordinate2d):
            self.__x = self.__x + other.get_x()
            self.__y = self.__y + other.get_y()
        else:
            # assume it is numeric
            self.__x = self.__x + other
            self.__y = self.__y + other

    def __sub__(self, other):
        self.__add__(-other)