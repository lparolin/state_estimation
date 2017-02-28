"""Contains simplified models."""
from utils import Coordinate2d

class TrueModel:
    def __init__(self, initial_position, initial_speed, sample_time):
        self.__position = initial_position
        self.__speed = initial_speed
        self.__sample_time = sample_time

    def __update_single_coordinate(self, position, speed, acceleration):
        """Updates the state of the system along a single dimension"""
        # update matrix along a coordinate x or y
        # A = [a11  a12; a21 a22]
        a11 = 1.0
        a12 = self.__sample_time
        a21 = 0.0
        a22 = 1.0

        # input matrix along a coordinate B = b1 b2
        b1 = (self.__sample_time**2) / 2.0
        b2 = 1

        new_position = a11*position + a12*speed + b1 * acceleration
        new_speed = a21*position + a22*speed + b2 * acceleration
        return (new_position, new_speed)

    def get_state(self):
        return (self.get_position.get_x(),
                self.get_speed.get_x(),
                self.get_speed.get_y(),
                self.get_position.get_y()
                )

    def set_state(self, state):
        self.__position = \
            Coordinate2d(state[0], state[2])
        self.__speed = \
            Coordinate2d(state[1], state[3])

    def get_position(self):
        return self.__position

    def get_speed(self):
        return self.__speed

    def update_state(self, acceleration):
        """Update state of the system"""
        new_data = []
        for idx in (0, 1):
            new_data.append(
                self.__update_single_coordinate(
                    self.get_position().get_idx(idx),
                    self.get_speed().get_idx(idx),
                    acceleration.get_idx(idx)
                    )
                )
        new_position_x = new_data[0][0]
        new_speed_x = new_data[0][1]
        new_position_y = new_data[1][0]
        new_speed_y = new_data[1][1]
        self.__position = Coordinate2d(
            new_position_x,
            new_position_y)
        self.__speed = Coordinate2d(
            new_speed_x,
            new_speed_y)

class NumericalDifferentiation:
    def __init__(self, sample_time):
        self.__sample_time = sample_time

    def get_estimation(self, current_position, previous_position):
        delta_position = current_position - previous_position
        estimated_speed_x = delta_position.get_x() / self.__sample_time
        estimated_speed_y = delta_position.get_y() / self.__sample_time


class Observer(TrueModel):
    def __init__(self, initial_position, initial_speed, sample_time, gain):
        super(Observer, self).__init__(initial_position, initial_speed, sample_time)
        self.__gain = gain

    def get_estimated_position(self):
        return self.__position

    def get_estimated_speed(self):
        return self.__speed

    def get_estimation(self, acceleration, position):
        previous_estimated_position = self.get_estimated_speed()
        super(Observer, self).update_state(acceleration)
        # now we need to include the effect of knowing the position
        # in order to improve the estimate state
        # gain is [l11, l12; l21 l22; l31 l32; l41 l42]
        estimation_error = position - previous_estimated_position
        old_state = self.get_state()
        new_state = [old_state[idx] +
                     self.__gain[idx][0] * estimation_error.get_x() +
                     self.__gain[idx][1] * estimation_error.get_y()
                     for idx in range(4)]
        self.set_state(new_state)
        return self.get_state()
