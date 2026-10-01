import os
import subprocess
import sys


def run_cli(*args):# ПОЗВОЛЯЕТ НЕ ПИСТАЬ ОДНУ И ТУЖЕ ФУНКЦИЮ НЕСКОЛЬКО РАЗ ПОДРЯД 
    return subprocess.run( # ПОЗВОЛЯЕТ ПИСАТЬ В ТЕРМИНАЛ, КАК БЫ ОТ НАШЕГО ЛИЦА
        [sys.executable, "-m", "toolkit", *args],
        # ВВОДИМ В ЗАПУСК PYTHON КОТОРЫЙ У НАС ИСПОЛЬЗУЕТСЯ В ПРОГЕ  SYS, -M, TOOLKIT
        # И ПОЛУЧЕННЫЕ ЗНАЧЕНИЯ ИЗ *ARGS - РАСПАКОВЫВАЕТ КОРТЕЖ
        capture_output = True,# СОХРАНЯЕТ ВЫВОД STDOUT И STDERR(ВЫВОД ОБЫЧНЫЙ И ОШИБОК)
        text = True,# СОХРАЯНЕМ ВЫВОД КАК СТРОКУ 
        env = {**os.environ, "PYTHONPATH": "src"}
        # **OS.ENVIRON - ДАЕТ КОМАНДУ ИСКАТЬ ПУТЬ ДЛЯ ЗАПУСКА ПРОГИ ДЛЯ ТЕСТОВ В SRC
        # А УЖЕ ПОСЛЕ ПИСАТЬ ТАМ -M TOOLKIT
    )


def test_calc_cli():
    result = run_cli("calc", "2+3")

    assert result.returncode == 0
    #ПРОВЕРКА ЗАВЕРШЕННОЙ ПРОГИ, ASSERT - ЕСЛИ, TRUE -> CONTINUE
    assert result.stdout.strip() == "5" #УБИРАЕТ ДЛЯ ПРОВЕРКИ НЕВИДИМЫЙ \N


def test_calc_cli_difficult():
    result = run_cli("calc", "2+3*4")

    assert result.returncode == 0
    assert result.stdout.strip() == "14"


def test_convert_cli():
    result = run_cli("convert", "100", "--from", "cm", "--to", "m")

    assert result.returncode == 0
    assert result.stdout.strip() == "1"


def test_calc_cli_error():
    result = run_cli("calc", "10/0")

    assert result.returncode == 2
    assert result.stderr != ""
    # STDERR - ПОТОК ОШИБОК, ЕСЛИ ERROR -> ТО ПРОВЕРКА ПРОЙДЕНА 


def test_convert_cli_error():
    result = run_cli("convert", "10", "--from", "km", "--to", "kg")

    assert result.returncode == 2
    assert result.stderr != ""