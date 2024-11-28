from view.colors import BLUE, BOLD, PURPLE, RESET, color
from utils.utils import clear_screen, prompt


class Page:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Page, cls).__new__(cls)
        return cls._instance

    def __init__(self, title, content, footer: str = None, on_input=None):
        self._title = title
        self._content = content
        self._footer = footer
        self._on_input = on_input
        self.padding = 0
        self.border_color = BLUE
        self.width = 90
        self.height = 32
        self._render()

    def header(self):
        padding = " " * self.padding
        max_width = self.width - 6
        width = max_width - len(self._title)
        border = "─" * width
        print(
            f"{padding}{self.border_color}┌─{BOLD}{PURPLE} {self._title} {RESET}{self.border_color}{border}─┐{RESET}")

    def content(self):
        offset = 5
        rows = str.splitlines(f"\n{self._content}")
        row_count = len(rows)
        footer_br_count = self._footer.count("\n") + 1 if self._footer else 0
        for i in range(self.height - row_count - footer_br_count - offset):
            rows.append(" ")
        for row in rows:
            self.body_row(row)

    def body(self, content=""):
        rows = str.splitlines(content)
        for row in rows:
            self.body_row(row)

    def body_row(self, row):
        padding = " " * self.padding
        specials = str.count(row, "\033[") * 5
        content_width = self.width - 4 + specials
        print(f"{padding}{self.border_color}│{RESET} {row: <{content_width}}{self.border_color} │{RESET}")

    def footer(self):
        padding = " " * self.padding
        max_width = self.width - self.padding - 4
        border = "─" * max_width
        print(f"{padding}{self.border_color}└─{border}─┘{RESET}")

    def hr(self):
        padding = " " * self.padding
        max_width = self.width - 4
        border = "─" * max_width
        print(f"{padding}{self.border_color}│{color(2)} {border} {RESET}{self.border_color}│{RESET}")

    def _render(self):
        clear_screen()
        self.header()
        self.content()
        if self._footer:
            p = " " * self.padding
            self.hr()
            self.body(f"{p}{self._footer}")
        self.footer()

        if self._on_input:
            _prompt = prompt()
            while self._on_input(_prompt):
                self._render()
