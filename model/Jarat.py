from abc import ABC, abstractmethod
from datetime import datetime, timedelta

from model.Seat import Seat
from view.colors import RED, RESET


class Jarat(ABC):
    def __init__(self, flight_id: int, terminal: str, destination: str, departure: str, arrival: str,
                 ticket_price: float, seat_count: int):
        self._type: str | None = None
        self._flight_id = flight_id
        self._terminal = terminal
        self._destination = destination
        self._departure = departure
        self._arrival = arrival
        self._ticket_price = ticket_price
        self._seats_count = seat_count
        self._seats_free = seat_count
        self._seats = self._init_seats()

    @abstractmethod
    def list_seats(self, user_seats: [str]):
        pass

    @abstractmethod
    def book_seat(self, number: int):
        pass

    @abstractmethod
    def cancel_seat(self, number: int):
        pass

    @property
    def type(self):
        return self._type

    @property
    def flight_id(self):
        return self._flight_id

    @property
    def terminal(self):
        return self._terminal

    @property
    def destination(self):
        return self._destination

    @property
    def departure(self):
        return self._departure

    @property
    def arrival(self):
        return self._arrival

    @property
    def is_bookable(self):
        now = datetime.now()
        departure = datetime.strptime(self._departure, "%Y.%m.%d. %H:%M")
        return departure - now > timedelta(minutes=0)

    @property
    def flight_duration(self):
        departure_time = datetime.strptime(self._departure, "%Y.%m.%d. %H:%M")
        arrival_time = datetime.strptime(self._arrival, "%Y.%m.%d. %H:%M")
        return int((arrival_time - departure_time).total_seconds() / 60 / 60)

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
        except ValueError:
            return f"{RED}Hiba!{RESET} {number} {RED}számú ülés nem létezik.{RESET}"

    def _init_seats(self):
        seats: list[Seat] = []
        for i in range(self._seats_count):
            seats.append(Seat(i + 1, False))
        return seats
