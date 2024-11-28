import os
from os import system

from view.colors import GREEN, RESET

WIDTH = 90
HEIGHT = 32

IN_OS_TERMINAL = False

try:
    os.get_terminal_size()
    IN_OS_TERMINAL = True
except Exception:
    IN_OS_TERMINAL = False


def prompt(message="", padding=0):
    p = " " * padding
    caret = ">" if IN_OS_TERMINAL else "✈️"
    msg = f"{p}{message}{RESET}\n" if message else ""
    return input(f"{msg}{p}{caret} {GREEN}")


def clear_screen():
    if IN_OS_TERMINAL:
        system('cls' if os.name == 'nt' else 'clear')
    else:
        print("\n" * 100)


def resize_console(cols: int, lines: int):
    try:
        os.terminal_size((cols, lines))
        system(f"mode con: cols={cols} lines={lines}")
    except Exception:
        return


def get_console_size() -> os.terminal_size:
    try:
        return os.get_terminal_size()
    except Exception:
        return os.terminal_size((WIDTH, HEIGHT))


def get_padding(target_width: int):
    columns, _ = get_console_size()
    return int(columns / 2 - target_width / 2)
