from utils.utils import prompt
from utils.utils import clear_screen
from view.colors import GREEN, RESET, GREY, BLUE, BOLD, PURPLE, AMBER, ITALIC


class MainMenu:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MainMenu, cls).__new__(cls)
        return cls._instance

    def __init__(self, bookings, on_input):
        self._bookings = bookings
        self._render(on_input)

    def _render(self, on_input):
        clear_screen()

        border = BLUE
        l = f"{border}│{RESET}"

        badge = f" ({GREEN}{len(self._bookings)}{RESET})"
        my_bookings = f"{badge: <17}" if len(self._bookings) > 0 else ""

        x = f"{GREY}[{RESET}x{GREY}]{RESET}"
        padding = 30
        p = " " * padding

        print("\n" * 3)
        print(f"{p}{border}┌─{BOLD} Reptér{PURPLE}♪ {RESET}{border}───────────────┐{RESET}")
        print(f"{p}{border}│                         │{RESET}")
        print(f"{p}{l} {AMBER} 1.{RESET} Jegyfoglalás        {l}")
        print(f"{p}{border}│                         │{RESET}")
        print(f"{p}{l} {AMBER} 2.{RESET} Foglalásaim{my_bookings: <8} {l}")
        print(f"{p}{border}│                         │{RESET}")
        print(f"{p}{l} {AMBER} 3.{RESET} Jegylemondás        {l}")
        print(f"{p}{border}│                         │{RESET}")
        if my_bookings:
            print(f"{p}{l} {AMBER} 4.{RESET} Járatfoglaltság     {l}")
            print(f"{p}{border}│                         │{RESET}")
        print(f"{p}{l} {x} Kilépés             {l}")
        print(f"{p}{border}│                         │{RESET}")
        print(f"{p}{border}└────────────────── {ITALIC}v1.0 ─┘{RESET}")

        _prompt = prompt("", padding + 1)

        while on_input(_prompt):
            self._render(on_input)
