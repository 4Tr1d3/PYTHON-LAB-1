from decimal import Decimal

import pytest

from src.toolkit.converter import convert
from src.toolkit.errors import ConverterError


def test_cm_to_m():
    assert convert(Decimal("100"), "cm", "m") == Decimal("1")


def test_km_to_m():
    assert convert(Decimal("2"), "km", "m") == Decimal("2000")


def test_kg_to_g():
    assert convert(Decimal("3"), "kg", "g") == Decimal("3000")


def test_c_to_f():
    assert convert(Decimal("100"), "c", "f") == Decimal("212")


def test_regist():
    assert convert(Decimal("1"), "KM", "m") == Decimal("1000")


def test_wrong_unit_1():
    with pytest.raises(ConverterError):
        convert(Decimal("10"), "km", "kg")


def test_wrong_unit_2():
    with pytest.raises(ConverterError):
        convert(Decimal("10"), "abc", "m")


def test_absolute_zero():
    with pytest.raises(ConverterError):
        convert(Decimal("-300"), "c", "f")