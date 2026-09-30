import pytest

from src.toolkit.converter import convert

def test_cm_to_m():
    assert convert(100, "cm", "m") == 1.0


def test_km_to_m():
    assert convert(2, "km", "m") == 2000.0


def test_kg_to_g():
    assert convert(3, "kg", "g") == 3000.0


def test_c_to_f():
    assert convert(100, "c", "f") == 212.0


def test_regist():
    assert convert(1, "KM", "m") == 1000.0


def test_wrong_unit_1():
    with pytest.raises(ValueError):
        convert(10, "km", "kg")


def test_wrong_unit_2():
    with pytest.raises(ValueError):
        convert(10, "abc", "m")


def test_absolute_zero():
    with pytest.raises(ValueError):
        convert(-300, "c", "f")