from model.Ticket import Ticket
from functools import reduce


class JegyFoglalas:

    def __init__(self, user: str):
        self._user = user
        self._tickets: list[Ticket] = []

    @property
    def user(self):
        return self._user

    @property
    def tickets(self):
        return self._tickets

    @property
    def total(self):
        return reduce((lambda sub_total, ticket: sub_total + ticket.price), self._tickets, 0)

    @property
    def seat_numbers(self):
        return list(map((lambda ticket: f"{ticket.flight_id}|{ticket.seat_number}"), self._tickets))

    def get_ticket(self, flight_id: int, seat_number: int) -> Ticket:
        try:
            return filter((lambda ticket: ticket.flight_id == flight_id and ticket.seat_number == seat_number), self._tickets)[0]
        except Exception as e:
            print(e)

    def book_ticket(self, flight_id: int, seat_number: int, price: float, user: str):
        self._tickets.append(Ticket(flight_id, seat_number, price, user))

    def redeem_ticket(self, flight_id, seat_number, user):
        tickets = filter(
            lambda ticket:
                ticket.user == user and ticket.flight_id == flight_id and ticket.seat_number == seat_number,
            self._tickets
        )
        if tickets[0]:
            self._tickets.remove(tickets[0])
        else:
            print("A keresett jegy nem található.")

    def find_user_tickets(self, user: str) -> list[Ticket]:
        tickets = filter(lambda ticket: ticket.user == user, self._tickets)
        return list(tickets)
