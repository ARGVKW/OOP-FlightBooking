from model.Jarat import Jarat
from model.Seat import Seat


class NemzetkoziJarat(Jarat):

    def __init__(self, flight_id, destination, ticket_price, seat_count):
        super().__init__(flight_id, destination, ticket_price, seat_count)
        self._seats_count = seat_count
        self._seats_free = seat_count
        self._seats = self._init_seats()

    @property
    def flight_id(self):
        return self._flight_id

    @property
    def ticket_price(self):
        return self._ticket_price

    @property
    def seats(self):
        return self._seats

    def seat(self, number: int):
        index = number - 1
        try:
            return self._seats[index]

        except:
            print("Hiba! " + str(number) + " számú ülés nem létezik.")

    def _init_seats(self):
        seats: list[Seat] = []
        for i in range(self._seats_count):
            seats.append(Seat(i, False))
        return seats

    def book_seat(self, number: int):
        index = number - 1
        self._seats[index].book()

    def cancel_seat(self, number: int):
        index = number - 1
        self._seats[index].cancel()

    def book_flight(self):
        if not self._seats_free == 0:
            self._seats_free -= 1
        else:
            print("Hiba, a járat megtelt.")
