from decimal import ROUND_HALF_UP, Decimal


def round_result(value: Decimal) -> Decimal:
    """ОКРУГЛЕНИЕ ЧИСЕЛ С ПОМОЩЬЮ ЛОГИКИ DECIMAL"""
    return value.quantize(Decimal("0.00000001"), rounding = ROUND_HALF_UP)
# ПОЗВОЛЯЕТ ОКРУГЛИТЬ ЧИСЛО ОТ 5 В БОЛЬШУЮ СТОРОНУ

def improvement_output(value: Decimal) -> str:
    """УБИРАЕМ НУЛИ ПОСЛЕ ЗАПЯТОЙ"""
    value = round_result(value)

    if value == 0:
        return "0"

    return format(value, "f").rstrip("0").rstrip(".")
    #УДАЛЯЕТ СНАЧАЛА 0 СПРАВА, НО ЕСЛИ 5.000, ТО ОСТАНЕТСЯ 5. ПОЭТОМУ УБИРАЕМ И ТОЧКУ
    #ФОРМАТ Ф ПЕРЕВОДИТ ЧИСЛА Е-5 В ДЕСЯТИЧНЫЙ ВИД