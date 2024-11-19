from abc import ABC, abstractmethod

from model.Seat import Seat


class Jarat(ABC):
    def __init__(self, flight_id: int, destination: str, ticket_price: float, seat_count: int):
        self._flight_id = flight_id
        self._destination = destination
        self._ticket_price = ticket_price
        self._seats_count = seat_count
        self._seats_free = seat_count
        self._seats = self._init_seats()

    @abstractmethod
    def list_seats(self, user_seats: [str]):
        ...

    @abstractmethod
    def book_seat(self, number: int):
        ...

    @abstractmethod
    def cancel_seat(self, number: int):
        ...

    @property
    def flight_id(self):
        return self._flight_id

    @property
    def destination(self):
        return self._destination

    @property
    def ticket_price(self):
        return self._ticket_price

    @property
    def seat_count(self):
        return self._seats_count

    @property
    def seats_free(self):
        return self._seats_free

    @property
    def seats(self):
        return self._seats

    @seats.setter
    def seats(self, new_seat: Seat):
        self._seats.append(new_seat)

    def get_seat(self, number: int):
        index = number - 1
        try:
            return self._seats[index]
        except Exception:
            print("Hiba! " + str(number) + " számú ülés nem létezik.")

    def _init_seats(self):
        seats: list[Seat] = []
        for i in range(self._seats_count):
            seats.append(Seat(i + 1, False))
        return seats
