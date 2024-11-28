from model.Jarat import Jarat
from model.Seat import Seat
from view.colors import RED, RESET, BOLD, INVERSE, PURPLE, GRASS


class NemzetkoziJarat(Jarat):

    def __init__(self, flight_id, terminal: str, destination: str, departure: str, arrival: str, ticket_price, seat_count):
        super().__init__(flight_id, terminal, destination, departure, arrival, ticket_price, seat_count)
        self._type = "Nemzetközi járat"

    def list_seats(self, user_seats: [int]):
        row_width = 6
        column_width = 3

        table = ""
        for i, seat in enumerate(self.seats):
            seat_number = i + 1
            colour = GRASS if seat_number in user_seats else PURPLE
            span = "   " if seat_number < 100 else "  "
            seat_badge = f"{colour}{BOLD}{INVERSE}{seat_number: <2}{RESET}"
            table += f"{seat_badge}{span}" if seat.is_booked else f"{seat_number: <5}"
            if seat_number % column_width == 0:
                table += "        "
            if not seat_number == self._seats_count and seat_number % row_width == 0:
                table += "\n"

        return table

    def book_seat(self, number: int):
        index = number - 1
        if self._seats_free > 0:
            self._seats[index].book()
            self._seats_free -= 1
        else:
            return f"{RED}Hiba! Ez a nemzetközi járat megtelt.{RESET}"

    def cancel_seat(self, number: int):
        index = number - 1
        if self._seats_free < self._seats_count:
            self._seats[index].cancel()
            self._seats_free += 1
        else:
            raise ValueError(f"{RED}Hiba, a művelet nem hajtható végre.{RESET}")
