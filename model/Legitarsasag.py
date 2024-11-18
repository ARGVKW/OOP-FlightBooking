from model.BelfoldiJarat import BelfoldiJarat
from model.NemzetkoziJarat import NemzetkoziJarat


class Legitarsasag:
    def __init__(self, name: str, flights: list[BelfoldiJarat | NemzetkoziJarat]):
        self._name = name
        self._flights = flights

    @property
    def name(self):
        return self._name

    @property
    def flights(self):
        return self._flights

    @flights.setter
    def flights(self, new_flight: BelfoldiJarat | NemzetkoziJarat):
        self._flights.append(new_flight)
