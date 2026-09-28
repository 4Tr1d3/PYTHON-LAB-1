import subprocess
import sys
import os

def run_cli(*args):# ПОЗВОЛЯЕТ НЕ ПИСТАЬ ОДНУ И ТУЖЕ ФУНКЦИЮ НЕСКОЛЬКО РАЗ ПОДРЯД 
    return subprocess.run( # ПОЗВОЛЯЕТ ПИСАТЬ В ТЕРМИНАЛ, КАК БЫ ОТ НАШЕГО ЛИЦА
        [sys.executable, "-m", "toolkit", *args],
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONPATH": "src"}
    )


def test_calc_cli():
    result = run_cli("calc", "2+3")

    assert result.returncode == 0
    assert result.stdout.strip() == "5.0" #УБИРАЕТ ДЛЯ ПРОВЕРКИ НЕВИДИМЫЙ \N


def test_calc_cli_complex():
    result = run_cli("calc", "2+3*4")

    assert result.returncode == 0
    assert result.stdout.strip() == "14.0"


def test_convert_cli():
    result = run_cli(
        "convert", "100", "--from", "cm", "--to", "m"
    )

    assert result.returncode == 0
    assert result.stdout.strip() == "1.0"


def test_calc_cli_error():
    result = run_cli("calc", "10/0")

    assert result.returncode == 2
    assert result.stderr != "" # ПОЗВОЛЯЕТ СОХРАНЯТЬ ОШИБКУ СЮДА, ЕСЛИ ОНА ПРОЗОШЛА


def test_convert_cli_error():
    result = run_cli(
        "convert", "10", "--from", "km", "--to", "kg"
    )

    assert result.returncode == 2
    assert result.stderr != ""