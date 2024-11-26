from utils.utils import clear_screen
from view.colors import BG_BLUE, WHITE, RESET, AMBER, BOLD, BLACK, BLUE, PURPLE, MAGENTA


class Header:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Header, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        clear_screen()

        brd_l = f"{BG_BLUE}{WHITE}│{BG_BLUE}"
        brd_r = f"{BG_BLUE}{WHITE}║{RESET}"
        padding = " " * 24

        print("\n" * 3)
        print(f"{padding}{BG_BLUE}{WHITE}╒═══════════════════════════════════╗{RESET}")
        print(
            f"{padding}{brd_l}{RESET}{PURPLE} {BOLD}Reptér{MAGENTA}♪{PURPLE} CLI v1.0 {RESET}{BG_BLUE}{BLACK} (c) 2024 {BOLD}ARGVKW {RESET}{brd_r}")
        print(f"{padding}{BG_BLUE}{WHITE}└───────────────────────────────────╜{RESET}")
        print("\n" * 5)
