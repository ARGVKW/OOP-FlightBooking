from model.BelfoldiJarat import BelfoldiJarat
from model.Jarat import Jarat
from model.Legitarsasag import Legitarsasag
from model.NemzetkoziJarat import NemzetkoziJarat
from model.Seat import Seat


class Repter:
    def __init__(self):
        self._user = ""
        self._airlines: list[Legitarsasag] = []
        self._selected_flight: Jarat
        self._init_data()

    @property
    def airlines(self):
        return self._airlines

    @airlines.setter
    def airlines(self, new_airline: Legitarsasag):
        self._airlines.append(new_airline)

    def _init_data(self):
        self.airlines = Legitarsasag("Luft Panda", [
                NemzetkoziJarat(1, "Kuala Lumpur", 1200.00, 120),
                BelfoldiJarat(2, "Debrecen", 250.00, 60),
                BelfoldiJarat(3, "Szolnok", 250.00, 60)
            ])
        self.airlines = Legitarsasag("Brian Air", [
                NemzetkoziJarat(4, "Rome", 1000.00, 120),
                NemzetkoziJarat(5, "Betlehem", 1100.00, 120),
                BelfoldiJarat(6, "Szentkirályszabadja", 250.00, 60)
            ])

    def set_user(self, user):
        _user = input("Adjon meg egy felhasználónevet!\nVagy folytatás vendégként (Enter)\n")
        new_user = _user or user
        self._user = new_user
        print(f"Üdvözöljük, {new_user}!\n")

    def list_airlines(self):
        for airline in self._airlines:
            print(airline.name)

    def list_flights(self):
        for airline in self._airlines:
            print(f"{airline.name}:")
            for flight in airline.flights:
                print(f"{flight.flight_id}.\t{flight.destination}\t\t\t{flight.ticket_price}€")

    def list_bookings(self):
        for airline in self._airlines:
            print(f"{airline.name}:")
            for flight in airline.flights:
                print(f"{flight.flight_id}.\t{flight.destination}\t\t\t{flight.ticket_price}€")

    def find_flight_by_id(self, flight_id: int):
        for airline in self._airlines:
            for flight in airline.flights:
                if flight.flight_id == flight_id:
                    return flight
        return None

    def find_seat(self, flight_id: int, seat_number: int):
        flight = self.find_flight_by_id(flight_id)
        if flight.flight_id == flight_id:
            for seat in flight.seats:
                if seat.number == seat_number:
                    return seat
        return None

    def choose_flight(self) -> Jarat:
        while True:
            print("Kérjük, válasszon járatot!")
            self.list_flights()
            flight_id = input("")

            try:
                flight = self.find_flight_by_id(int(flight_id))
                if flight:
                    self._selected_flight = flight
                    break
                else:
                    print("Nem található járat a megadott azonosítóval.")
            except Exception:
                print("Hiba! Kérjük csak egész számot adjon meg.")

        selected_flight = self._selected_flight
        print("A kiválasztott járat: ")
        print(f"{selected_flight.flight_id}.\t{selected_flight.destination}\t{selected_flight.ticket_price}€")
        while True:
            proceed = input("Folytatás (1) Módosítás (2)\n")
            if proceed == "1":
                return selected_flight
            elif proceed == "2":
                return self.choose_flight()

    def choose_seat(self, flight: Jarat) -> Seat:
        selected_seat: Seat

        while True:
            print("Kérjük válasszon az elérhető helyek közül:")
            flight.list_seats()
            prompt = input("").strip()

            try:
                seat_number = int(prompt)
                selected_seat = self.find_seat(flight.flight_id, seat_number)

                if selected_seat:
                    if selected_seat.is_booked:
                        print(f"A megadott ülőhely ({seat_number}) már foglalt.")
                    else:
                        self._selected_flight.book_seat(seat_number)
                        break
                else:
                    print(f"A megadott ülőhely ({seat_number}) nem található.")
            except Exception:
                print("Hiba! Kérjük csak egész számot adjon meg, és a számjegyek között ne legyen szóköz.")

        print("A lefoglalt ülőhely: ")
        print(f"{selected_seat.number}.\t{self._selected_flight.ticket_price}€")
        while True:
            proceed = input("Folytatás (1) Újabb foglalás (2)\n")
            if proceed == "1":
                return selected_seat
            elif proceed == "2":
                return self.choose_seat(flight)

    def start(self):
        print("╒═════════════════════════════════╗")
        print("│ Reptér CLI v1.0 (c) 2024 ARGVKW ║")
        print("└─────────────────────────────────╜")

        self.set_user("Vendég")

        # Main menu
        # 1. Book new flight
        # 2. View my tickets
        # 3. Redeem tickets
        # 4. Exit

        flight = self.choose_flight()
        seat = self.choose_seat(flight)

        # list booked seats
        print(f"{seat.number} számú ülőhely lefoglalva.")
        print(dir(seat))

        # pay booked seats

        # list tickets

