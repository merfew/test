import pytest
from lab6 import Calculator

calc = Calculator()

@pytest.mark.parametrize("a, b, expected", [
    (1, 2, 3),
    (-1, 5, 4),
    (0, 0, 0),
    (10, -3, 7),
    (2.5, 3.5, 6.0),
    (100, 50, 150),
    (-5, -3, -8)
])
def test_add(a, b, expected):
    assert calc.add(a, b) == expected

@pytest.mark.parametrize("a, b, expected", [
    (10, 2, 5),
    (9, 3, 3),
    (-6, 2, -3),
    (5, 2, 2.5),
    (0, 5, 0),
    (100, 4, 25),
    (7.5, 2.5, 3.0)
])
def test_divide(a, b, expected):
    assert calc.divide(a, b) == expected

def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError, match="Division by zero"):
        calc.divide(5, 0)


@pytest.mark.parametrize("n, expected", [
    (2, True),
    (3, True),
    (4, False),
    (17, True),
    (20, False),
    (1, False),
    (0, False),
    (-5, False),
    (97, True),
    (100, False),
    (29, True),
    (31, True),
    (113, True)
])
def test_is_prime_number(n, expected):
    assert calc.is_prime_number(n) == expected