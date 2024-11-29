
class Seat:
    def __init__(self, number: int, is_booked: bool):
        self._number = number
        self._is_booked = is_booked

    @property
    def number(self):
        return self._number

    @property
    def is_booked(self):
        return self._is_booked

    def book(self):
        self._is_booked = True

    def cancel(self):
        self._is_booked = False
