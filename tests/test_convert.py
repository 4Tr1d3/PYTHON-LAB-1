import pytest

from src.toolkit.converter import convert

def test_cm_to_m():
    assert convert(100, "cm", "m") == 1.0


def test_km_to_m():
    assert convert(2, "km", "m") == 2000.0


def test_kg_to_g():
    assert convert(3, "kg", "g") == 3000.0


def test_celsius_to_fahrenheit():
    assert convert(100, "c", "f") == 212.0


def test_case_insensitive():
    assert convert(1, "KM", "m") == 1000.0


def test_incompatible_units():
    with pytest.raises(ValueError):
        convert(10, "km", "kg")


def test_unknown_unit():
    with pytest.raises(ValueError):
        convert(10, "abc", "m")


def test_below_absolute_zero():
    with pytest.raises(ValueError):
        convert(-300, "c", "f")