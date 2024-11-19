from time import sleep

from model.BelfoldiJarat import BelfoldiJarat
from model.Jarat import Jarat
from model.JegyFoglalas import JegyFoglalas
from model.Legitarsasag import Legitarsasag
from model.NemzetkoziJarat import NemzetkoziJarat
from model.Seat import Seat
from utils.utils import clear_screen, AMBER, RESET, resize_console


class Repter:
    def __init__(self):
        self._airlines: list[Legitarsasag] = []
        self._selected_flight: Jarat | None = None
        self._user = ""
        self._user_tickets: JegyFoglalas

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
                NemzetkoziJarat(4, "Róma", 1000.00, 120),
                NemzetkoziJarat(5, "Betlehem", 1100.00, 120),
                BelfoldiJarat(6, "Szentkirályszabadja", 250.00, 60)
            ])

    def _init_booking(self):
        self._user_tickets = JegyFoglalas(self._user)

        for airline in self._airlines:
            for flight in airline.flights:
                for seat in flight.seats:
                    if seat.number % (len(flight.seats)/6) == 0:
                        flight.book_seat(seat.number)

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
            for flight in airline.flights:
                print(f"{flight.flight_id}. {airline.name}:\t{flight.destination: <20}{flight.ticket_price}€")

    def list_bookings(self):
        if len(self._user_tickets.tickets) > 0:
            print('Az Ön által lefoglalt jegyek:')

            for ticket in self._user_tickets.tickets:
                print(str(ticket))

            print(f'\nÖsszesen: {self._user_tickets.total}€\n')
        else:
            print("Nem található foglalás.")

    def make_payment(self):
        if len(self._user_tickets.tickets) > 0:
            pass

    def find_flight(self, flight_id: int):
        for airline in self._airlines:
            for flight in airline.flights:
                if flight.flight_id == flight_id:
                    return flight
        return None

    def find_seat(self, flight_id: int, seat_number: int):
        flight = self.find_flight(flight_id)
        if flight.flight_id == flight_id:
            for seat in flight.seats:
                if seat.number == seat_number:
                    return seat
        return None

    def choose_flight(self) -> Jarat:
        while True:
            print("Kérjük, válasszon járatot!")
            self.list_flights()
            flight_id = input(">> ")

            if flight_id == "0":
                break

            try:
                flight = self.find_flight(int(flight_id))
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
            flight.list_seats(self._user_tickets.seat_numbers)
            prompt = input("").strip()

            if prompt == "0":
                break

            try:
                seat_number = int(prompt)
                selected_seat = self.find_seat(flight.flight_id, seat_number)

                if selected_seat:
                    if selected_seat.is_booked:
                        print(f"A megadott ülőhely ({seat_number}) már foglalt.")
                    else:
                        self._selected_flight.book_seat(seat_number)
                        self._user_tickets.book_ticket(flight.flight_id, seat_number, flight.ticket_price, self._user)
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

    def main_menu(self):
        I = f"{AMBER}│{RESET}"
        while True:
            clear_screen()
            print("\n")
            print(f"{AMBER}┌─ Főmenü ────────────┐{RESET}")
            print(f"{I} 1. Jegyfoglalás     {I}")
            print(f"{I} 2. Foglalásaim      {I}")
            print(f"{I} 3. Jegyvisszaváltás {I}")
            if self._selected_flight:
                print(f"{I} 4. Járatfoglaltság  {I}")
            print(f"{I} X. Kilépés          {I}")
            print(f"{AMBER}└─────────────────────┘{RESET}")
            prompt = input("")

            if prompt == "1":
                clear_screen()
                flight = self.choose_flight()
                if not flight:
                    continue
                seat = self.choose_seat(flight)
                clear_screen()

                # list booked seats
                self.list_bookings()

                # pay booked seats

                # list tickets
            elif prompt == "2":
                clear_screen()
                self.list_bookings()
                input()
            elif prompt == "3":
                clear_screen()
                pass
            elif prompt == "4":
                clear_screen()
                print(f"{AMBER}Aktu'lis járat foglaltsága:{RESET}")
                self._selected_flight.list_seats(self._user_tickets.seat_numbers)
                input()
                clear_screen()
            elif prompt == "X" or prompt == "x":
                clear_screen()
                print("Viszontlátásra!")
                sleep(1)
                break

    def start(self):
        resize_console(80, 28)

        print("╒═════════════════════════════════╗")
        print("│ Reptér CLI v1.0 (c) 2024 ARGVKW ║")
        print("└─────────────────────────────────╜")

        self.set_user("Vendég")
        self._init_data()
        self._init_booking()
        sleep(1.5)
        self.main_menu()

