from model.Jarat import Jarat


class BelfoldiJarat(Jarat):

    def __init__(self, flight_id, destination, ticket_price, seat_count):
        super().__init__(flight_id, destination, ticket_price, seat_count)

    def list_seats(self):
        row_width = 4
        column_width = 2
        table = ""
        for i, seat in enumerate(self.seats):
            seat_number = i + 1
            table += ("x" if seat.is_booked else str(seat_number)) + "\t"
            if seat_number % column_width == 0:
                table += "\t\t"
            if seat_number % row_width == 0:
                table += "\n"
        print(table)

    def book_seat(self, number: int):
        index = number - 1
        if self._seats_free > 0:
            self._seats[index].book()
            self._seats_free -= 1
        else:
            print("Hiba! Ez a belföldi járat megtelt.")

    def cancel_seat(self, number: int):
        index = number - 1
        if self._seats_free < self._seats_count:
            self._seats[index].cancel()
            self._seats_free += 1
        else:
            print("Hiba, a művelet nem hajtható végre.")
