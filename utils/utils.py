import os
from os import system

RED = '\033[91m'
GREEN = '\033[92m'
AMBER = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[1;3;35m'
RESET = '\033[0m'

IN_IDE_TERMINAL = False

try:
    os.get_terminal_size()
    IN_IDE_TERMINAL = True
except Exception:
    IN_IDE_TERMINAL = False


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



