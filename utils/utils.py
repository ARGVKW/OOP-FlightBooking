import os
from os import system

from view.colors import GREEN

IN_IDE_TERMINAL = False

try:
    os.get_terminal_size()
    IN_IDE_TERMINAL = True
except Exception:
    IN_IDE_TERMINAL = False


def prompt(value: str = ""):
    return input(f"{value}{GREEN}")


def clear_screen():
    if IN_IDE_TERMINAL:
        system('cls' if os.name == 'nt' else 'clear')
    else:
        print("\n" * 100)


def resize_console(cols: int, lines: int):
    try:
        system(f"mode con: cols={cols} lines={lines}")
    except Exception:
        return



