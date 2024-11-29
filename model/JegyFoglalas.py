from model.Ticket import Ticket
from functools import reduce

from model.User import User
from view.colors import RED, RESET


class JegyFoglalas:

    def __init__(self, flight_id: int, user: User):
        self._flight_id = flight_id
        self._user = user
        self._tickets: list[Ticket] = []

    @property
    def flight_id(self):
        return self._flight_id

    @property
    def user(self) -> User:
        return self._user

    @user.setter
    def user(self, user: User):
        self._user = user

    @property
    def tickets(self) -> list[Ticket]:
        return self._tickets

    @property
    def is_paid(self):
        return all(ticket.is_paid for ticket in self._tickets)

    @property
    def total(self):
        return reduce((lambda sub_total, ticket: sub_total + ticket.price), self._tickets, 0)

    @property
    def total_outstanding(self):
        return reduce((lambda sub_total, ticket: sub_total + (0 if ticket.is_paid else ticket.price)), self._tickets, 0)

    @property
    def seat_numbers(self):
        return list(map((lambda ticket: ticket.seat_number), self._tickets))

    def get_ticket(self, flight_id: int, seat_number: int) -> Ticket | None:
        return next(filter((lambda ticket: ticket.flight_id == flight_id and ticket.seat_number == seat_number), self._tickets), None)

    def book_ticket(self, flight_id: int, seat_number: int, price: float, user: User):
        self._tickets.append(Ticket(flight_id, seat_number, price, user))

    def redeem_ticket(self, flight_id: int, seat_number: int):
        redeemed = 0
        ticket = next(filter(
            lambda t: t.user == self.user and t.flight_id == flight_id and t.seat_number == seat_number,
            self._tickets
        ), None)
        if ticket:
            redeemed += ticket.redeem()
            self._tickets.remove(ticket)
        else:
            return f"{RED}A keresett jegy ({RESET}{seat_number}{RED}) nem található.{RESET}"
        return redeemed

    def pay_all(self) -> int:
        payed = 0
        for ticket in self._tickets:
            if ticket.user == self.user and not ticket.is_paid:
                payed += ticket.pay()
        return payed

    def redeem_all(self):
        redeemed = 0
        for ticket in self._tickets:
            if ticket.user == self.user and ticket.is_paid:
                redeemed += ticket.redeem()
        self._tickets.clear()
        return redeemed
