from random import randint


class User:
    def __init__(self, name):
        """ nincs password az egyszerűség kedvéért """
        self._name = name
        self._id = randint(1, 999)

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name
