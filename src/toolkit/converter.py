from .constants import LENGTH_FACTORS, MASS_FACTORS, ABSOLUTE_ZERO


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
        raise ValueError('Ошибка: нету такой единицы измерения')


def convert(value: float, from_unit: str, to_unit: str) -> float:
    """САМ КОНВЕРТЕР"""
    from_unit = from_unit.lower()  # ПРИВОДИМ К НИЖНЕМУ РЕГИСТРУ
    to_unit = to_unit.lower()  # ПРИВОДИМ К НИЖНЕМУ РЕГИСТРУ

    # УЗНАЕМ ГРУППУ ЕДИНИЦ ИЗМЕРЕНИЯ, ДЛЯ ПРОВЕРКИ НА ОШИБКУ
    group_from = get_unit_group(from_unit)
    # УЗНАЕМ ГРУППУ ЕДИНИЦ ИЗМЕРЕНИЯ, ДЛЯ ПРОВЕРКИ НА ОШИБКУ
    group_to = get_unit_group(to_unit)

    # ОШИБКА НЕСОВМЕСТИМЫХ ГРУПП
    if group_from != group_to:
        raise ValueError('Ошибка: несовмистимые единицы измерения')

    # КОНВЕРТИУРЕМ ГРУППЫ
    if group_from == 'length':
        value_from = LENGTH_FACTORS[from_unit] * value
        value_to = value_from / LENGTH_FACTORS[to_unit]
        return value_to
    elif group_from == 'mass':
        value_from = MASS_FACTORS[from_unit] * value
        value_to = value_from / MASS_FACTORS[to_unit]
        return value_to
    elif group_from == 'temperature':
        if value < ABSOLUTE_ZERO[from_unit]:
            raise ValueError('Ошибка: температура не может быть ниже абсолютного нуля')

        """ПЕРЕВОДИМ ВСЕ ЗНАЧЕНИЯ К C"""
        if from_unit == 'c':
            value_c = value
        elif from_unit == 'f':
            value_c = (value - 32) * 5 / 9
        elif from_unit == 'k':
            value_c = value - 273.15

        """ПЕРЕВОДИМ ИЗ C В ОТВЕТ"""
        if to_unit == 'c':
            return value_c
        elif to_unit == 'f':
            return value_c * 9 / 5 + 32
        elif to_unit == 'k':
            return value_c + 273.15
