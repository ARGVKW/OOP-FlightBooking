def color(color_code: str | int):
    return f"\033[{color_code}m"


RED = color(91)
GRASS = color(32)
GREEN = color(92)
AMBER = color(93)
BLUE = color(94)
PURPLE = color(35)
MAGENTA = color(95)
CYAN = color(96)
BLACK = color(97)
WHITE = color(99)
GREY = color(90)
RESET = color(0)

BG_GREEN = color(42)
BG_AMBER = color(43)
BG_BLUE = color(44)

BOLD = color(1)
ITALIC = color(3)
BOLD_ITALIC = color("1;3")
UNDERLINE = color(4)
INVERSE = color(7)
STRIKE = color(9)



