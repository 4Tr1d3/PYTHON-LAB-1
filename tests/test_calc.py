import pytest
from src.toolkit.calculator import tokenize, validate, calculate


def test_addition():
    tokens = tokenize("2+3")
    validate(tokens)

    assert calculate(tokens) == 5


def test_subtraction():
    tokens = tokenize("10-4")
    validate(tokens)

    assert calculate(tokens) == 6


def test_multiplication_priority():
    tokens = tokenize("2+3*4")
    validate(tokens)

    assert calculate(tokens) == 14


def test_division():
    tokens = tokenize("15/3")
    validate(tokens)

    assert calculate(tokens) == 5


def test_parentheses():
    tokens = tokenize("(2+3)*4")
    validate(tokens)

    assert calculate(tokens) == 20


def test_unary_minus():
    tokens = tokenize("-5+8")
    validate(tokens)

    assert calculate(tokens) == 3


def test_spaces_and_complex_expression():
    tokens = tokenize(" 2 * ( 3 + 4 ) - 10 / 2 ")
    validate(tokens)

    assert calculate(tokens) == 9


def test_division_by_zero():
    tokens = tokenize("10/0")
    validate(tokens)

    with pytest.raises(ValueError):
        calculate(tokens)


def test_two_binary_operators():
    tokens = tokenize("2*/3")

    with pytest.raises(ValueError):
        validate(tokens)


def test_invalid_symbol():
    with pytest.raises(ValueError):
        tokenize("2&3")
        