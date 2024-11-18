from model.Jarat import Jarat
from model.Seat import Seat


class NemzetkoziJarat(Jarat):

    def __init__(self, flight_id, destination, ticket_price, seat_count):
        super().__init__(flight_id, destination, ticket_price, seat_count)

    def book_seat(self, number: int):
        index = number - 1
        if self._seats_free > 0:
            self._seats[index].book()
            self._seats_free -= 1
        else:
            print("Hiba! Ez a nemzetközi járat megtelt.")

    def cancel_seat(self, number: int):
        index = number - 1
        if self._seats_free < self._seats_count:
            self._seats[index].cancel()
            self._seats_free += 1
        else:
            print("Hiba, a művelet nem hajtható végre.")
