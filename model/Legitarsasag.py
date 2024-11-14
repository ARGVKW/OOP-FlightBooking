from model.Jarat import Jarat
from model.BelfoldiJarat import BelfoldiJarat
from model.NemzetkoziJarat import NemzetkoziJarat


class Legitarsasag:
    def __init__(self, name: str, flights: list[Jarat | BelfoldiJarat | NemzetkoziJarat]):
        self._name = name
        self._flights = flights
