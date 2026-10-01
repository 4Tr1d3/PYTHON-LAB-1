from decimal import Decimal

from .constants import ABSOLUTE_ZERO, LENGTH_CONSTS, MASS_CONSTS
from .errors import ConverterError


def get_unit_group(unit: str) -> str:
    """УЗНАЕМ, К КАКОЙ ГРУППЕ ИЗМЕРЕНИЙ ОТНОСИТСЯ НАШЕ ЗНАЧЕНИЕ"""
    length = ['mm', 'cm', 'm', 'km']
    mass = ['g', 'kg']
    temperature = ['c', 'f', 'k']
    if unit in length:
        return 'length'
    elif unit in mass:
        return 'mass'
    elif unit in temperature:
        return 'temperature'
    else:
        raise ConverterError('Ошибка: Нету такой единицы измерения')


def convert(value: Decimal, from_unit: str, to_unit: str) -> Decimal:
    """САМ КОНВЕРТЕР"""
    from_unit = from_unit.lower()  # ПРИВОДИМ К НИЖНЕМУ РЕГИСТРУ
    to_unit = to_unit.lower()  # ПРИВОДИМ К НИЖНЕМУ РЕГИСТРУ

    # УЗНАЕМ ГРУППУ ЕДИНИЦ ИЗМЕРЕНИЯ, ДЛЯ ПРОВЕРКИ НА ОШИБКУ
    group_from = get_unit_group(from_unit)
    # УЗНАЕМ ГРУППУ ЕДИНИЦ ИЗМЕРЕНИЯ, ДЛЯ ПРОВЕРКИ НА ОШИБКУ
    group_to = get_unit_group(to_unit)

    # ОШИБКА НЕСОВМЕСТИМЫХ ГРУПП
    if group_from != group_to:
        raise ConverterError('Ошибка: Несовместимые единицы измерения')

    # КОНВЕРТИУРЕМ ГРУППЫ
    if group_from == 'length':
        value_from = LENGTH_CONSTS[from_unit] * value # ПЕРЕВОДИМ В МЕТРЫ
        value_to = value_from / LENGTH_CONSTS[to_unit]
        return value_to
    elif group_from == 'mass':
        value_from = MASS_CONSTS[from_unit] * value # ПЕРЕВОДИМ В ГРАММЫ
        value_to = value_from / MASS_CONSTS[to_unit]
        return value_to
    elif group_from == 'temperature':
        if value < ABSOLUTE_ZERO[from_unit]:
            raise ConverterError(
                'Ошибка: Температура не может быть ниже абсолютного нуля'
            )

        """ПЕРЕВОДИМ ВСЕ ЗНАЧЕНИЯ К C"""
        if from_unit == 'c':
            value_c = value
        elif from_unit == 'f':
            value_c = (value - 32) * 5 / 9
        elif from_unit == 'k':
            value_c = value - Decimal("273.15")

        """ПЕРЕВОДИМ ИЗ C В ОТВЕТ"""
        if to_unit == 'c':
            return value_c
        elif to_unit == 'f':
            return value_c * 9 / 5 + 32
        elif to_unit == 'k':
            return value_c + Decimal("273.15")
