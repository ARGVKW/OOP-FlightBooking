from abc import ABC, abstractmethod


class Jarat(ABC):
    def __init__(self, flight_id: int, destination: str, ticket_price: float, seat_count: int):
        self._flight_id = flight_id
        self._destination = destination
        self._ticket_price = ticket_price
        self._seat_count = seat_count

    @abstractmethod
    def book_seat(self, number: int):
        pass

    @abstractmethod
    def cancel_seat(self, number: int):
        pass

