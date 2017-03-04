"""Contains simplified models."""
from utils import Coordinate2d


class TrueModel:
    """LTI system describing the movement of a point mass in 2D.

    Input to the system is acceleration in 2D and output is the
    position of the system. State is determined by position and velocity
    of the particle.
    See also utils.Coordinate2d
    """

    def __init__(self, initial_position, initial_speed, sample_time):
        """Initialize the model.

        initial_position and initial_speed are Coordinate2d objects.
        sample_time is a floating number.
        """
        self.__position = initial_position
        self.__speed = initial_speed
        self.__sample_time = sample_time

    def __update_single_coordinate(self, position, speed, acceleration):
        """Update the state of the system along a single dimension."""
        # update matrix along a coordinate x or y
        # A = [a11  a12; a21 a22]
        a11 = 1.0
        a12 = self.__sample_time
        a21 = 0.0
        a22 = 1.0

        # input matrix along a coordinate B = b1 b2
        b1 = (self.__sample_time * self.__sample_time) / 2.0
        b2 = self.__sample_time

        new_position = a11*position + a12*speed + b1 * acceleration
        new_speed = a21*position + a22*speed + b2 * acceleration
        return (new_position, new_speed)

    def get_state(self):
        """Return state of the system as 4D tuple."""
        return (self.get_position().get_x(),
                self.get_speed().get_x(),
                self.get_position().get_y(),
                self.get_speed().get_y()
                )

    def set_state(self, state):
        """Set internal state of the system."""
        self.__position = \
            Coordinate2d(state[0], state[2])
        self.__speed = \
            Coordinate2d(state[1], state[3])

    def get_position(self):
        """Return position as Coordinate2d."""
        return self.__position

    def get_speed(self):
        """Return speed as Coordinate2d."""
        return self.__speed

    def update_state(self, acceleration):
        """Update state of the system."""
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

    def get_sample_time(self):
        """Return sample time."""
        return self.__sample_time


class Observer(TrueModel):
    """Luenberger observer of the true model.

    The class is implemented a subclass of true model in order to rely
    on existing code.
    """

    def __init__(self, initial_position, initial_speed, sample_time, gain):
        """Initialize the observer.

        Input as in True model.
        gain is the gain of the observer. Defined as tuple
        [l11, l12; l21 l22; l31 l32; l41 l42]
        """
        super(Observer, self).__init__(initial_position, initial_speed,
                                       sample_time)
        self.__gain = gain

    def get_estimation(self, acceleration, position):
        """Get estimate from obsever."""
        previous_estimated_position = self.get_position()
        self.update_state(acceleration)
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
