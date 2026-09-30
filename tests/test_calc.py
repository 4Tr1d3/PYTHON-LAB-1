import pytest
from src.toolkit.calculator import tokenize, validate, calculate


def test_plus():
    tokens = tokenize("2+3")
    validate(tokens)

    assert calculate(tokens) == 5


def test_minus():
    tokens = tokenize("10-4")
    validate(tokens)

    assert calculate(tokens) == 6


def test_priority():
    tokens = tokenize("2+3*4")
    validate(tokens)

    assert calculate(tokens) == 14


def test_division():
    tokens = tokenize("15/3")
    validate(tokens)

    assert calculate(tokens) == 5


def test_brackets():
    tokens = tokenize("(2+3)*4")
    validate(tokens)

    assert calculate(tokens) == 20


def test_unary_minus():
    tokens = tokenize("-5+8")
    validate(tokens)

    assert calculate(tokens) == 3


def test_spaces():
    tokens = tokenize(" 2 * ( 3 + 4 ) - 10 / 2 ")
    validate(tokens)

    assert calculate(tokens) == 9


def test_division_by_zero():
    tokens = tokenize("10/0")
    validate(tokens)

    with pytest.raises(ValueError):
        calculate(tokens)


def test_two_operators():
    tokens = tokenize("2*/3")

    with pytest.raises(ValueError): # ОЖИДАЕМ ОШИБКУ 
        validate(tokens)


def test_wrong_symbol():
    with pytest.raises(ValueError):
        tokenize("2&3")
        