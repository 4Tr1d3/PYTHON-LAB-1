class ToolkitError(Exception):
    """Ошибка toolkit"""

class CalculatorError(ToolkitError):
    """Ошибка при вычислении"""


class ConverterError(ToolkitError):
    """Ошибка при конвертации"""