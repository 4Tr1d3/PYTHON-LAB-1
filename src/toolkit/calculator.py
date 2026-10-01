from decimal import Decimal

from .errors import CalculatorError


def tokenize(expression: str) -> list[tuple[str, str]]:
    """РАЗБИВАЕМ ВЫРАЖЕНИЕ НА ТОКЕНЫ"""
    i = 0
    tokens = []
    operation = "-+*/()"
    numbers = ""
    while i < len(expression):  # ЦИКЛ ДЛЯ ЗАПИСИ ТОКЕНОВ
        if expression[i].isspace():  # ПРОВЕРКА НА ПРОБЕЛЫ
            i += 1
            continue

        """ЦИКЛ ДЛЯ ЗАПИСИ ЧИСЕЛ БЕЗ И С ТОЧКОЙ"""
        while i < len(expression) and (expression[i].isdigit() or expression[i] == "."):
            numbers += expression[i]
            i += 1

        """ЕСЛИ ПОСЛЕ ЦИКЛА ФЛАГ НЕ ПУСТОЙ, ТО ДОБАВЛЯЕМ ЕГО В ТОКЕН И ЗАНУЛЯЕМ ЕГО"""
        if numbers != "":
            tokens.append(("NUMS", numbers))
            numbers = ""

        """ПРОВЕРКА НА ПОЯВИВШИЙСЯ ИЗ-ЗА СДВИГОВ i ПРОБЕЛ"""
        if i < len(expression) and expression[i].isspace():
            i += 1
            continue


        """ПРОВЕРКА НА ОПЕРАЦИЮ"""
        if i < len(expression):  # ПРОВЕРЯЕМ, НАХОДИТСЯ ЛИ i ЕЩЕ В ВНУТРИ СТРОКИ
            if expression[i] in operation:
                tokens.append(("OPERATION", expression[i]))
            else:
                raise CalculatorError(f"Ошибка: Недопустимый символ '{expression[i]}'")
            # ВЫВОДИМ ОШИБКУ, ЕСЛИ ТАКОГО СИМВОЛА НЕ МОЖЕТ БЫТЬ
            i += 1   
    return tokens

def validate(tokens: list[tuple[str, str]]) -> None:
    """ПРОВЕРЯЕМ ВОЗМОЖНОСТЬ СУЩЕСТВОВАНИЯ ТАКОГО ВЫРАЖЕНИЯ"""
    i = 0
    found_number = False
    operations_unary = "-+"
    operations = "*/"
    error = ""
    brackets = 0

    if len(tokens) == 0:
        error = "Пустое выражение"
    
    while i < len(tokens):
        if tokens[i][0] == "NUMS":
#РЕПЛЕЙСИМ ТОЧКУ ОДИН РАЗ НА ПУСТОТУ, И В СЛУЧАЕ ЛИШНЕЙ ТОЧКИ КОД НЕ ПРОШЕЛ ПРОВЕРКУ
            if tokens[i][1].replace(".", "", 1).isdigit():
                if not found_number:
                    found_number = True
                    i += 1
                    continue
                else:
                    error = "Пропущенный оператор"
                    break
            
        #ПРОВЕРКА НА УНАРНЫЙ ОПЕРАТОР   
        if tokens[i][0] == "OPERATION" and tokens[i][1] in operations_unary:
            if found_number:
                found_number = False
                i += 1
                continue
            else:
                i += 1
                continue

        if tokens[i][0] == "OPERATION" and tokens[i][1] in operations:
            if found_number:
                found_number = False
                i += 1
                continue
            else:
                error = "Два бинарных оператора подряд"
                break

        if tokens[i][0] == "OPERATION" and tokens[i][1] == '(':
            #ПРОВЕРКА НА НАЛИЧИЕ ОПЕРАТОРА ПЕРЕД СКОБКОЙ
            if found_number:
                error = "Пропущенный оператор"
                break

            brackets += 1
            i += 1

        elif tokens[i][0] == "OPERATION" and tokens[i][1] == ')':
            brackets -= 1
            i += 1
            # ПРОВЕРКА НА КОЛИЧЕСТВО СКОБОК
            if brackets < 0:
                error = "Лишняя закрывающая скобка"
                break


    if error == "" and not found_number:
        error = "Пропущенный операнд"

    if brackets != 0:
        raise CalculatorError("Ошибка: Незакрытая скобка")
    if error:
        raise CalculatorError(f"Ошибка: {error}")

def get_priority(operate: str) -> int:
    """ВЫВОДИТ ПРИОРИТЕТ ФУНКЦИИ ОТ ВВЕДЕННОЙ ОПЕРАЦИИ"""
    if operate == '+':
        return 1
    elif operate == '-':
        return 1
    elif operate == '*':
        return 2
    elif operate == '/':
        return 2
    return -1

def calculate(tokens: list[tuple[str, str]]) -> Decimal:
    """РАСТАВЛЯЕМ ПРИОРИТЕТЫ И ДЕЛИМ ВЫРАЖЕНИЕ НА ЧАСТИ, СЧИТАЕМЫЕ ДРУГОЙ Ф-ЦИЕЙ"""
    left = -1 # ЛЕВАЯ ГРАНИЦА ДЛЯ РАЗДЕЛЕНИЯ ПО ПРИОРИТЕТАМ
    right = len(tokens) - 1 # ПРАВАЯ ГРАНИЦА ДЛЯ РАЗДЕЛЕНИЯ ПО ПРИОРИТЕТАМ


    operation_priority = 100
    operation_position = -2
    brackets = 0
    """ПРОВЕРЯЕМ ДЛЯ ПОВТОРНЫХ КАЛКУЛТОРОВ, ЧТО ОСТАЛОСЬ ТОЛЬКО ЧИСЛО В СРЕЗЕ"""
    if len(tokens) == 1:
        return Decimal(tokens[0][1])

    if len(tokens) == 2 and tokens[0][1] in "+-":
        result = calculate(tokens[1:])
        if tokens[0][1] == '-':
            return -result
        return result

    for i in range(right, left, -1):
    # ИДЕМ ПО ЦИКЛУ СПРАВА НАЛЕВО (УДОБНЕЙ ДЛЯ ВОСПРИЯТИЯ УНАРНЫЙ ОПЕРАТОР -> БИНАРНЫЙ)
        unary = False

        #ПРОВЕРКА НА СКОБКУ
        if tokens[i][1] == ')':
            brackets += 1
            continue
        
        if tokens[i][1] == '(':
            brackets -= 1
            continue


        """ПРОВЕРКА НА УНАРНЫЕ ОПЕРАЦИИ"""
        if tokens[i][1] == '+' or tokens[i][1] == '-':
            if i == 0 or tokens[ i - 1][1] in "+-/*":
                unary = True
            else:
                unary = False
        if unary:
            continue

        if brackets == 0:
            operate = get_priority(tokens[i][1])
        
            if (operate != -1 and operate < operation_priority):
                """БЕРЕМ ПРИОРИТЕТ ОТ ЛЮБОГО СИМВОЛА.ЕСЛИ int -> -1.ЕСЛИ +-*/ -> 1,2"""
                operation_position = i
                operation_priority = operate

    if operation_position == -2:
        return calculate(tokens[1:-1])

    """ДЕЛАЕМ СРЕЗ ЧАСТЕЙ ТОКЕНЫ, КОТОРЫЕ ОТДЕЛЬНО ПОТОМ БУДЕМ СЧИТАТЬ"""
    left_tokens = tokens[:operation_position]
    right_tokens = tokens[operation_position + 1 :right + 1]
    
    """ПОВТОРЯЕМ КАЛЬКУЛЕЙТ ДЛЯ СРЕЗОВ"""
    left_result = calculate(left_tokens)
    right_result = calculate(right_tokens)
    return apply_operation(left_result, tokens[operation_position][1], right_result)

def apply_operation(left: Decimal, operation: str, right: Decimal) -> Decimal:
    """СЧИТАЕМ ДВА ЧИСЛА И ВОЗВРАЩАЕМ РЕЗУЛЬТАТ"""
    if operation == '+':
        return left + right
    elif operation == '-':
        return left - right
    elif operation == '*':
        return left * right
    elif operation == '/':
        if right != 0:
            return left / right
        else:
            raise CalculatorError("Ошибка: Нельзя делить на ноль")