
class Seat:
    def __init__(self, number: int, is_booked: bool):
        self._number = number
        self._is_booked = is_booked

    def book(self):
        self._is_booked = True

    def cancel(self):
        self._is_booked = False

    def get(self):
        return self
