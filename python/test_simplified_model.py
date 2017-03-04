"""Script of running base tests on utils."""

from simplified_models import TrueModel
from utils import Coordinate2d


def create_input_data():
    """Utility function for creating input data."""
    position = Coordinate2d(3.0, 4.0)
    speed = Coordinate2d(2.0, 5.0)
    sample_time = 0.1
    return {'position': position,
            'speed': speed,
            'sample_time': sample_time}


def test_base():
    """Check we can create the model."""
    input_data = create_input_data()
    base_model = TrueModel(input_data['position'],
                           input_data['speed'],
                           input_data['sample_time'])
    assert(True)


def test_get_position_velocity():
    """Check we can get the right value of velocity."""
    input_data = create_input_data()
    base_model = TrueModel(input_data['position'],
                           input_data['speed'],
                           input_data['sample_time'])
    assert(base_model.get_position() == input_data['position'])
    assert(base_model.get_speed() == input_data['speed'])


def test_get_state():
    """Verify we return the correct state."""
    input_data = create_input_data()
    base_model = TrueModel(input_data['position'],
                           input_data['speed'],
                           input_data['sample_time'])
    state = base_model.get_state()
    assert(state[0] == input_data['position'].get_x())
    assert(state[1] == input_data['speed'].get_x())
    assert(state[2] == input_data['position'].get_y())
    assert(state[3] == input_data['speed'].get_y())


def test_set_state():
    """Verify we set the state correctly."""
    input_data = create_input_data()
    base_model = TrueModel(input_data['position'],
                           input_data['speed'],
                           input_data['sample_time'])
    state = [0, 1, 2, 3]
    base_model.set_state(state)
    new_state = base_model.get_state()
    for idx in range(len(state)):
        assert(state[idx] == new_state[idx])

    assert(base_model.get_position() == Coordinate2d(0, 2))
    assert(base_model.get_speed() == Coordinate2d(1, 3))


def test_update_step():
        """Verify update step."""
        initial_position = Coordinate2d(0, 0)
        initial_speed = Coordinate2d(3, 4)
        sample_time = 0.1
        base_model = TrueModel(initial_position,
                               initial_speed,
                               sample_time)
        acceleration = Coordinate2d(0, 0)
        base_model.update_state(acceleration)
        new_state = base_model.get_state()
        assert abs(new_state[0] - 0.3) < 1e-8
        assert(new_state[1] == 3)
        assert abs(new_state[2] - 0.4) < 1e-8
        assert(new_state[3] == 4)


def compute_new_state(initial_position, initial_speed, acceleration,
                      sample_time):
        expected_position_x = initial_position.get_x() + \
            sample_time * initial_speed.get_x() + \
            (sample_time**2) / 2 * acceleration.get_x()
        expected_position_y = initial_position.get_y() + \
            sample_time * initial_speed.get_y() + \
            (sample_time**2) / 2 * acceleration.get_y()

        expected_speed_x = initial_speed.get_x() + \
            sample_time * acceleration.get_x()
        expected_speed_y = initial_speed.get_y() + \
            sample_time * acceleration.get_y()
        return (expected_position_x, expected_speed_x,
                expected_position_y, expected_speed_y)


def test_update_step_acceleration():
        """Verify update step with non zero acceleration."""
        initial_position = Coordinate2d(0, 0)
        initial_speed = Coordinate2d(0, 0)
        sample_time = 0.1
        base_model = TrueModel(initial_position,
                               initial_speed,
                               sample_time)

        for iteration in range(5):
            acceleration = Coordinate2d(1*iteration, 2*iteration)
            current_position = base_model.get_position()
            current_speed = base_model.get_speed()
            base_model.update_state(acceleration)
            new_state = base_model.get_state()
            expected_state = compute_new_state(
                current_position, current_speed,
                acceleration, sample_time)

            assert all([abs(new_state[i] - expected_state[i]) < 1e-8]
                       for i in range(len(new_state)))
