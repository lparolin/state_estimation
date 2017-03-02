"""Script of running base tests on utils"""

from utils import Coordinate2d

def test_base():
    my_coordinate = Coordinate2d(3.0, 4.0)
    assert (my_coordinate.get_x() == 3.0)
    assert (my_coordinate.get_y() == 4.0)
    assert (my_coordinate.get_idx(0) == 3.0)
    assert (my_coordinate.get_idx(1) == 4.0)

def test_negative_operator():
    my_coordinate = Coordinate2d(3.0, 4.0)
    negative_coordinate = -my_coordinate
    assert (negative_coordinate.get_x() == -3.0)
    assert (negative_coordinate.get_y() == -4.0)

def test_subtraction_operator():
    my_coordinate = Coordinate2d(3.0, 4.0)
    my_other_coordinate = Coordinate2d(5.0, 7.0)
    difference = my_coordinate - my_other_coordinate
    assert (difference.get_x() == -2.0)
    assert (difference.get_y() == -3.0)

def test_addition_operator():
    my_coordinate = Coordinate2d(3.0, 4.0)
    my_other_coordinate = Coordinate2d(5.0, 7.0)
    sum_coordinate = my_coordinate + my_other_coordinate
    assert (sum_coordinate.get_x() == 8.0)
    assert (sum_coordinate.get_y() == 11.0)

def test_equality():
    my_coordinate = Coordinate2d(3.0, 4.0)
    assert (my_coordinate == Coordinate2d(3.0, 4.0))
    assert (my_coordinate != Coordinate2d(3.0, 3.0))
    assert (my_coordinate != Coordinate2d(4.0, 4.0))
