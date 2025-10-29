import pytest
from src.сalculate import Calculate

@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (1, 3, 4),
    (3, 3, 6),
])
def test_add(a, b, expected):
    assert Calculate().add(a, b) == expected

@pytest.mark.parametrize("a, b, expected", [
    (2, 1, 2.0),
    (1, 2, 0.5),
    (6, 3, 2.0),
])
def test_division_normal(a, b, expected):
    assert Calculate().division(a, b) == expected

@pytest.mark.parametrize("a, b, expected_exception", [
    (10, 0, ZeroDivisionError),
    (5, "abc", TypeError),
    (7, None, TypeError),
])
def test_division_errors(a, b, expected_exception):
    with pytest.raises(expected_exception):
        Calculate().division(a, b)
