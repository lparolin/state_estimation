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
            X = self.__x + other.get_x()
            Y = self.__y + other.get_y()
        else:
            # assume it is numeric
            X = self.__x + other
            Y = self.__y + other

        return Coordinate2d(X, Y)

    def __eq__(self, other):
        is_equal = False
        if isinstance(other, Coordinate2d):
            is_equal = \
                (self.get_x() == other.get_x()) and \
                (self.get_y() == other.get_y())
        return is_equal

    def __neq__(self, other):
        return not self == other

    def __neg__(self):
        X = -self.__x
        Y = -self.__y
        return Coordinate2d(X, Y)

    def __sub__(self, other):
        return self.__add__(-other)


class GenerateBaseSimulation:
    """Class for running the base simulation"""

    def __init__(self, true_model, observer, acceleration,
                 output_noise=None, input_noise=None,
                 sample_time=None):
        """Instantiate the object and run the simulation."""
        self.__true_model = true_model
        self.__observer = observer
        self.__acceleration = acceleration
        n_samples = len(self.__acceleration)
        if output_noise is None:
            self.__output_noise = [Coordinate2d(0, 0)
                                   for i in range(n_samples)]
        else:
            self.__output_noise = output_noise
        if input_noise is None:
            self.__input_noise = [Coordinate2d(0, 0)
                                  for i in range(n_samples)]
        else:
            self.__input_noise = input_noise
        if sample_time is None:
            self.__sample_time = observer.get_sample_time()
        else:
            self.__sample_time = sample_time

        self.__run_simulation()

    def __run_simulation(self):
        n_samples = len(self.__acceleration)
        state = []
        estimated_state = []
        measured_acceleration = []
        measured_position = []
        for i_step in range(n_samples):
            state.append(self.__true_model.get_state())
            estimated_state.append(self.__observer.get_state())
            measured_acceleration.append(
                self.__acceleration[i_step] + self.__input_noise[i_step])
            measured_position.append(
                self.__true_model.get_position() + self.__output_noise[i_step])

            self.__true_model.update_state(self.__acceleration[i_step])
            self.__observer.get_estimation(measured_acceleration[i_step],
                                           measured_position[i_step])

        self.__state = state
        self.__estimated_state = estimated_state
        self.__measured_acceleration = measured_acceleration
        self.__measured_position = measured_position
        self.__n_samples = n_samples

    def __extract_element_from_state(self, element_type, state):
        if element_type == "speed":
            idx1, idx2 = 1, 3
        elif element_type == "position":
            idx1, idx2 = 0, 2

        n_steps = len(state)  # number of time stamps in state
        temp_list = \
            [Coordinate2d(state[time_id][idx1], state[time_id][idx2])
             for time_id in range(n_steps)]
        return temp_list

    def get_estimated_speed(self):
        return self.__extract_element_from_state("speed",
                                                 self.__estimated_state)

    def get_estimated_position(self):
        return self.__extract_element_from_state("position",
                                                 self.__estimated_state)

    def get_speed(self):
        return self.__extract_element_from_state("speed",
                                                 self.__state)

    def get_position(self):
        return self.__extract_element_from_state("position",
                                                 self.__state)

    def get_measured_position(self):
        return self.__measured_position

    def get_measured_acceleration(self):
        return self.__measured_acceleration

    def get_state_as_np_array(self):
        return np.array(self.__state)

    def get_estimated_state_as_np_array(self):
        return np.array(self.__estimated_state)

    def get_speed_numerical_difference(self):
        measured_position = self.get_measured_position()
        sample_time = self.__sample_time
        x_numeric_speed = [0] + \
                          [(measured_position[i+1].get_x() -
                            measured_position[i].get_x())/sample_time
                           for i in range(len(measured_position) - 1)]
        y_numeric_speed = [0] + \
                          [(measured_position[i+1].get_y() -
                            measured_position[i].get_y())/sample_time
                           for i in range(len(measured_position) - 1)]
        out_data = [
            Coordinate2d(x_numeric_speed[i], y_numeric_speed[i])
            for i in range(len(x_numeric_speed))]

        return out_data

    def convert_list_to_np_array(self, input_list):
        temp_list = [
             [input_list[i].get_x(), input_list[i].get_y()]
             for i in range(len(input_list))]
        return np.array(temp_list)

    def get_speed_numerical_difference_as_np_array(self):
        data = self.get_speed_numerical_difference()
        return self.convert_list_to_np_array(data)

    def get_max_vector(self):
        true_state = self.get_state_as_np_array()
        estimated_state = self.get_estimated_state_as_np_array()
        conatenated_state = np.concatenate((true_state, estimated_state),
                                           axis=0)
        return np.amax(conatenated_state, axis=0)

    def get_min_vector(self):
        true_state = self.get_state_as_np_array()
        estimated_state = self.get_estimated_state_as_np_array()
        conatenated_state = np.concatenate((true_state, estimated_state),
                                           axis=0)
        return np.amin(conatenated_state, axis=0)

    def get_min_max_position(self):
        """
        Computes the largest coordinate point (x,y) for the position
        among all of the position-related vectors.
        """

        max_item = self.get_max_vector()
        max_position = Coordinate2d(max_item[0], max_item[2])

        min_item = self.get_min_vector()
        min_position = Coordinate2d(min_item[0], min_item[2])
        return (min_position, max_position)

    def get_min_max_speed(self):
        """
        Computes the largest speed among all of the position-related vectors.
        """
        max_item = self.get_max_vector()
        min_item = self.get_min_vector()
        num_speed = self.get_speed_numerical_difference_as_np_array()
        num_speed_max = np.amax(num_speed, axis=0)
        num_speed_min = np.amin(num_speed, axis=0)

        #print("max_item:{}".format(max_item))
        #print("min_item:{}".format(min_item))
        #print("num_speed:{}".format(num_speed))
        #print("num_speed_max:{}".format(num_speed_max))
        #print("num_speed_min:{}".format(num_speed_min))

        if num_speed_max[0] > max_item[1]:
            max_speed_x = num_speed_max[0]
        else:
            max_speed_x = max_item[1]

        if num_speed_max[1] > max_item[3]:
            max_speed_y = num_speed_max[1]
        else:
            max_speed_y = max_item[3]

        max_speed = Coordinate2d(max_speed_x, max_speed_y)

        if num_speed_min[0] < min_item[1]:
            min_speed_x = num_speed_min[0]
        else:
            min_speed_x = min_item[1]

        if num_speed_min[1] < min_item[3]:
            min_speed_y = num_speed_min[1]
        else:
            min_speed_y = min_item[3]

        min_speed = Coordinate2d(min_speed_x, min_speed_y)

        return (min_speed, max_speed)

    def get_n_time_steps(self):
        """Return the number of time stamps in this simulation."""
        return self.__n_samples
