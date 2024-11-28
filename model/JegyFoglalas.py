from model.Ticket import Ticket
from functools import reduce

from model.User import User


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
    def ticket_count(self) -> int:
        return len(self._tickets)

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

    def get_seat_numbers_by_flight(self, flight_id: int):
        if flight_id:
            return list(
                map((lambda ticket: ticket.seat_number),
                    filter((lambda ticket: ticket.flight_id == flight_id), self._tickets)))

    def get_ticket(self, flight_id: int, seat_number: int) -> Ticket:
        try:
            return filter((lambda ticket: ticket.flight_id == flight_id and ticket.seat_number == seat_number), self._tickets)[0]
        except Exception as e:
            print(e)

    def book_ticket(self, flight_id: int, seat_number: int, price: float, user: str):
        self._tickets.append(Ticket(flight_id, seat_number, price, user))

    def redeem_ticket(self, flight_id: int, seat_number: int):
        redeemed = 0
        ticket = filter(
            lambda t: t.user == self.user and t.flight_id == flight_id and t.seat_number == seat_number,
            self._tickets
        )[0]
        if ticket:
            redeemed = ticket.redeem()
            self._tickets.remove(ticket)
        else:
            print("A keresett jegy nem található.")
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

    def find_user_tickets(self, user: str) -> list[Ticket]:
        tickets = filter(lambda ticket: ticket.user == user, self._tickets)
        return list(tickets)
