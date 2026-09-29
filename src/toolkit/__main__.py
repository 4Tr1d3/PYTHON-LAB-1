import argparse  # ДОБАВЛЯЕМ БИБЛИОТЕКУ, КОТОРАЯ СЧИТЫВАЕТ CLI
import sys
from .calculator import tokenize, validate, calculate#ИМПОРТИРУЕМ КАЛЬКУЛЯТОР И ДОП.ФУНКЦИИ К НЕЙ
from .converter import convert#ИМПОРТИРУЕМ КОНВЕРТЕР


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Консольный набор утилит: калькулятор и конвертер единиц.",
        epilog="""Примеры:
    python -m toolkit calc "2 + 3 * 4"
    python -m toolkit calc "-5 + (10 / 2)"
    python -m toolkit convert 100 --from cm --to m
    python -m toolkit convert 100 --from c --to f

    Поддерживаемые единицы:
    Длина:       mm, cm, m, km
    Масса:       g, kg
    Температура: c, f, k

    Для подробной информации:
    python -m toolkit calc --help
    python -m toolkit convert --help""",
    formatter_class=argparse.RawDescriptionHelpFormatter)  # ПУСТОЙ ОБЪЕКТ ДЛЯ ЗАПИСИ CLI

    # СОЗДАЕМ ПОДКОМАНДЫ(МОЖЕМ ПРИНИМАТЬ БОЛЬШЕ ОДНОГО ЗНАЧЕНИЯ ИЗ CLI)
    subparsers = parser.add_subparsers(dest="command", required=True)

    calc_parser = subparsers.add_parser("calc", help = 'Вычисление математического выражения',
    description="Вычисляет математическое выражение.",
    epilog="""Поддерживаются:
    +  -  *  /
    круглые скобки
    унарные + и -
    целые и дробные числа

    Примеры:
    python -m toolkit calc "2 + 3 * 4"
    python -m toolkit calc "(10 - 2) / 4"
    python -m toolkit calc "-5 + 8" """,
    formatter_class=argparse.RawDescriptionHelpFormatter)  # СОЗДАЕМ КОМАНДУ CALC
    calc_parser.add_argument("expression")  # ПОЛУЧАЕМ АРГУМЕНТ ИЗ CLI


    convert_parser = subparsers.add_parser("convert",
    help="Конвертация единиц измерения",
    description="Конвертирует значение между единицами измерения.",
    epilog="""Длина:
    mm, cm, m, km

    Масса:
    g, kg

    Температура:
    c, f, k

    Единицы можно указывать в любом регистре.

    Примеры:
    python -m toolkit convert 100 --from cm --to m
    python -m toolkit convert 2 --from km --to m
    python -m toolkit convert 100 --from c --to f""",
    formatter_class=argparse.RawDescriptionHelpFormatter)  # СОЗДАЕМ КОМАНДУ CONVERT

    convert_parser.add_argument("value")  # ПОЛУЧАЕМ АРГУМЕНТ ИЗ CLI
    # ПОЛУЧАЕМ АРГУМЕНТ ИЗ CLI, dest(КАКОЕ ИМЯ ДАТЬ ПЕРЕМЕННОЙ ПОЛУЧЕННОЙ ПОСЛЕ ФЛАГА),required(ТРУ = ОБЯЗАТЕЛЬНО ДОЛЖНО БЫТЬ ЗНАЧЕНИЕ )
    convert_parser.add_argument("--from", dest="from_unit", required=True)
    convert_parser.add_argument("--to", dest="to_unit",required=True)  # ПОЛУЧАЕМ АРГУМЕНТ ИЗ CLI

    args = parser.parse_args()  # СОХРАНЯЕМ ЗНАЧЕНИЯ, ПОЛУЧЕННЫЕ ИЗ CLI
    try:
        if args.command == 'calc':#ЗАПУСКАЕМ КАЛЬКУЛЯТОР
            tokens = tokenize(args.expression)
            validate(tokens)
            result = calculate(tokens)
            print(result)
        elif args.command == 'convert':#ЗАПУСКАЕМ КОНВЕРТЕР
            try:
                value = float(args.value)
            except ValueError:
                raise ValueError("Ошибка: значение должно быть числом")
            result = convert(value, args.from_unit, args.to_unit)
            print(result)
    except ValueError as error:
        print(error, file = sys.stderr) # ПОЗВОЛЯЕТ ПРИНУДИТЕЛЬНО ВЫВЕСТИ ФУНКЦИЮ В ПОТОК ОШИБОК ( print - обычный поток, stderr позволяет вывести как ошибку)
        sys.exit(2)
if __name__ == "__main__":
    main()