from decimal import Decimal

ABSOLUTE_ZERO = {
    'c': Decimal("-273.15"),
    'f': Decimal("-459.67"),
    'k': Decimal("0"),
}

LENGTH_CONSTS = {
    'mm': Decimal("0.001"),
    'cm': Decimal("0.01"),
    'm': Decimal("1"),
    'km': Decimal("1000"),
}

MASS_CONSTS = {
    'g': Decimal("1"),
    'kg': Decimal("1000"),
}