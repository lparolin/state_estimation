"""Script of running base tests on utils"""

from simplified_models import TrueModel
from utils import Coordinate2d

def create_input_data():
    position = Coordinate2d(3.0, 4.0)
    speed = Coordinate2d(2.0, 5.0)
    sample_time = 0.1
    return {'position': position,
            'speed': speed,
            'sample_time': sample_time}

def test_base():
    input_data = create_input_data()
    base_model = TrueModel(input_data['position'],
                           input_data['speed'],
                           input_data['sample_time'])
    assert(True)

def test_get_position_velocity():
    input_data = create_input_data()
    base_model = TrueModel(input_data['position'],
                           input_data['speed'],
                           input_data['sample_time'])
    assert(base_model.get_position() == input_data['position'])
    assert(base_model.get_speed() == input_data['speed'])

def test_get_state():
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
