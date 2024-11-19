class Ticket:
    def __init__(self, flight_id, seat_number, price, user):
        self._flight_id = flight_id
        self._seat_number = seat_number
        self._price = price
        self._user = user
        self._is_paid = False

    def __str__(self):
        return f'Flight ID: {self.flight_id}\tSeat Nr.: {self.seat_number}\tPrice: {self.price}€'

    @property
    def flight_id(self):
        return self._flight_id

    @property
    def seat_number(self):
        return self._seat_number

    @property
    def price(self):
        return self._price

    @property
    def user(self):
        return self._user

    @property
    def is_paid(self):
        return self._is_paid

    def pay(self):
        self._is_paid = True
        return self._price

    def redeem(self):
        self._is_paid = False
        return self._price
