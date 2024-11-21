from time import sleep

from model.BelfoldiJarat import BelfoldiJarat
from model.Jarat import Jarat
from model.JegyFoglalas import JegyFoglalas
from model.Legitarsasag import Legitarsasag
from model.NemzetkoziJarat import NemzetkoziJarat
from model.Seat import Seat
from utils.utils import clear_screen, resize_console, prompt
from view.colors import GREY, AMBER, RESET, MAGENTA, GREEN, RED


class Repter:
    def __init__(self):
        self._airlines: list[Legitarsasag] = []
        self._selected_flight: Jarat | None = None
        self._user = ""
        self._user_tickets = JegyFoglalas()

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

    @property
    def selected_flight(self):
        flight, airline = self.find_flight(self._selected_flight.flight_id)
        return f"{GREEN}{flight.flight_id}. {airline.name} {flight.destination} {flight.ticket_price}{RESET}€"

    def _init_booking(self):
        self._user_tickets.user = self._user

        for airline in self._airlines:
            for flight in airline.flights:
                for seat in flight.seats:
                    if seat.number % (len(flight.seats) / 6) == 0:
                        flight.book_seat(seat.number)

    def set_user(self, user: str):
        padding = " " * 24
        _user = input(
            f"{padding}{AMBER}Adjon meg egy felhasználónevet!{RESET}\n{padding}Vagy folytatás vendégként (Enter)\n{padding}{GREEN}")
        new_user = _user or user
        self._user = new_user
        print(f"{padding}{RESET}Üdvözöljük, {AMBER}{new_user}{RESET}!\n")

    def list_airlines(self):
        for airline in self._airlines:
            print(airline.name)

    def list_flights(self):
        for airline in self._airlines:
            for flight in airline.flights:
                print(
                    f"{AMBER}{flight.flight_id}.{RESET} {airline.name}:\t{flight.destination: <20}{flight.ticket_price}€")

    def manage_bookings(self, is_redemption: bool = False):
        padding = " " * 56
        while True:
            if len(self._user_tickets.tickets) > 0:
                print(f"{AMBER}Az Ön által lefoglalt jegyek:{RESET}")

                for i, ticket in enumerate(self._user_tickets.tickets):
                    flight, airline = self.find_flight(ticket.flight_id)
                    print(f"{i + 1}. {airline.name} {flight.destination: <20} {str(ticket)}")

                total = self._user_tickets.total
                outstanding = self._user_tickets.total_outstanding
                payment_label = f"Fizetés (F) " if outstanding else ""
                redemption_label = f" Lemondás (L) " if is_redemption else ""

                print(f"\n{padding}{"Összesen:": <12} {AMBER}{total}{RESET}€")
                print(f"{padding}{"Fizetendő:": <12} {GREEN}{outstanding}{RESET}€\n" if outstanding else "\n")
                _prompt = input(f"{payment_label}{redemption_label} Folytatás (Enter) ")

                if outstanding and _prompt.lower() == "f":
                    clear_screen()
                    payed = self._user_tickets.pay_all()
                    if payed:
                        print(f"{GREEN}Sikeres fizetés! {RESET}{payed}€")
                    return self.manage_bookings(is_redemption)

                elif is_redemption and total and _prompt.lower() == "l":
                    clear_screen()

                    for ticket in self._user_tickets.tickets:
                        flight, _ = self.find_flight(ticket.flight_id)
                        flight.cancel_seat(ticket.seat_number)

                    redemption = self._user_tickets.redeem_all()
                    redemption_msg = f" Visszatérítés: {RESET}{redemption}€" if redemption else f"{RESET} (Nem történt fizetés)"
                    print(f"{AMBER}Sikeres lemondás!{redemption_msg}")

                    return self.manage_bookings(is_redemption)
                else:
                    return
            else:
                print("Nem található foglalás.")
                input("Vissza (Enter)")
                return

    def find_flight(self, flight_id: int) -> tuple[Jarat | None, Legitarsasag | None]:
        for airline in self._airlines:
            for flight in airline.flights:
                if flight.flight_id == flight_id:
                    return flight, airline
        return None, None

    def find_seat(self, flight_id: int, seat_number: int) -> Seat | None:
        flight, _ = self.find_flight(flight_id)
        if flight.flight_id == flight_id:
            for seat in flight.seats:
                if seat.number == seat_number:
                    return seat
        return None

    def choose_flight(self) -> Jarat | None:
        while True:
            clear_screen()
            print(f"{AMBER}Kérjük, válasszon járatot!{RESET}")
            self.list_flights()
            print(f"Vissza (0)\n")
            flight_id = prompt("> ")

            if flight_id == "0":
                return

            try:
                flight, _ = self.find_flight(int(flight_id))
                if flight:
                    self._selected_flight = flight
                    break
                else:
                    clear_screen()
                    print(f"{RED}Nem található járat a megadott azonosítóval.{RESET}")
            except Exception:
                clear_screen()
                print(f"{RED}Hiba!{RESET} Kérjük csak egész számot adjon meg.")

        selected_flight = self._selected_flight

        if not selected_flight:
            return self.choose_flight()

        print(f"{AMBER}A kiválasztott járat: {RESET}")
        print(
            f"{GREEN}{selected_flight.flight_id}.\t{selected_flight.destination}\t{selected_flight.ticket_price}{RESET}€")

        while True:
            proceed = input("Folytatás (Enter) Módosítás (1)\n")
            clear_screen()
            if proceed == "1":
                return self.choose_flight()
            else:
                return selected_flight

    def choose_seat(self, flight: Jarat, message: str = "", prev_prompt: str | None = None):
        selected_seat: Seat
        has_booked_seat = prev_prompt and f"{flight.flight_id}|{prev_prompt}" in self._user_tickets.seat_numbers

        clear_screen()
        print(f"{AMBER}Járat:{RESET} {self.selected_flight}")
        print(f"{AMBER}Ülőhelyek:{RESET} {GREEN}{self._selected_flight.seats_free}{RESET}/{self._selected_flight.seat_count} szabad")
        print(f"{GREEN}x{RESET}: saját foglalás  {MAGENTA}x{RESET}: egyéb foglalások\n")

        while True:
            flight.list_seats(self._user_tickets.seat_numbers)

            print(f"\n{message}" if message else f"\n{AMBER}Kérjük válasszon az elérhető helyek közül{RESET}")
            _prompt = prompt("Vissza (0) Folytatás (Enter)\n> " if has_booked_seat else "Vissza (0)\n> ").strip()

            if _prompt == "0":
                return self.choose_flight()

            if _prompt == "" and has_booked_seat:
                return

            try:
                seat_number = int(_prompt)
                selected_seat = self.find_seat(flight.flight_id, seat_number)

                if selected_seat:
                    if selected_seat.is_booked:
                        print_message = f"{AMBER}A megadott ülőhely ({seat_number}) már foglalt.{RESET}"
                        break
                    else:
                        self._selected_flight.book_seat(seat_number)
                        self._user_tickets.book_ticket(flight.flight_id, seat_number, flight.ticket_price, self._user)
                        print_message = (f"{AMBER}A lefoglalt ülőhely: {RESET}{GREEN}{selected_seat.number}."
                                         + f"\t{self._selected_flight.ticket_price}€{RESET}")
                        break
                else:
                    print_message = f"{AMBER}A megadott ülőhely ({RESET}{seat_number}{AMBER}) nem található.{RESET}"
                    break
            except Exception:
                print_message = f"{RED}Hiba!{RESET} Kérjük csak egész számot adjon meg, és a számjegyek között ne legyen szóköz."
                break

        return self.choose_seat(flight, print_message, _prompt)

    def main_menu(self):
        l = f"{AMBER}│{RESET}"

        while True:
            clear_screen()

            badge = f" ({GREEN}{self._user_tickets.ticket_count}{RESET})"
            my_bookings = f"{badge: <17}" if self._user_tickets.ticket_count > 0 else ""

            x = f"{GREY}[{RESET}x{GREY}]{RESET}"
            padding = " " * 30

            print("\n" * 3)
            print(f"{padding}{AMBER}┌─ Főmenü ────────────────┐{RESET}")
            print(f"{padding}{AMBER}│                         │{RESET}")
            print(f"{padding}{l}  1. Jegyfoglalás        {l}")
            print(f"{padding}{AMBER}│                         │{RESET}")
            print(f"{padding}{l}  2. Foglalásaim{my_bookings: <8} {l}")
            print(f"{padding}{AMBER}│                         │{RESET}")
            print(f"{padding}{l}  3. Jegylemondás        {l}")
            print(f"{padding}{AMBER}│                         │{RESET}")
            if self._selected_flight:
                print(f"{padding}{l}  4. Járatfoglaltság     {l}")
                print(f"{padding}{AMBER}│                         │{RESET}")
            print(f"{padding}{l} {x} Kilépés             {l}")
            print(f"{padding}{AMBER}│                         │{RESET}")
            print(f"{padding}{AMBER}└─────────────────────────┘{RESET}")
            prompt = input(f"{padding}   ")

            if prompt == "1":
                clear_screen()
                flight = self.choose_flight()
                if not flight:
                    continue
                self.choose_seat(flight)
                clear_screen()

                if self._user_tickets.ticket_count:
                    self.manage_bookings()

            elif prompt == "2":
                clear_screen()
                self.manage_bookings()
            elif prompt == "3":
                clear_screen()
                self.manage_bookings(True)
            elif prompt == "4":
                clear_screen()
                print(f"{AMBER}Járat:{RESET} {self.selected_flight}")
                print(f"{AMBER}Ülőhelyek:{RESET} {GREEN}{self._selected_flight.seats_free}{RESET}/{self._selected_flight.seat_count} szabad")
                print(f"{GREEN}x{RESET}: saját foglalás  {MAGENTA}x{RESET}: egyéb foglalások\n")
                self._selected_flight.list_seats(self._user_tickets.seat_numbers)
                input(f"\nFolytatás (Enter) ")
                clear_screen()
            elif prompt == "X" or prompt == "x":
                clear_screen()
                print("Viszontlátásra!")
                sleep(1)
                break

    def start(self):
        resize_console(88, 28)
        clear_screen()

        brd_l = f"{AMBER}│{RESET}"
        brd_r = f"{AMBER}║{RESET}"
        padding = " " * 24

        print("\n" * 3)
        print(f"{padding}{AMBER}╒═════════════════════════════════╗{RESET}")
        print(f"{padding}{brd_l} Reptér CLI v1.0 (c) 2024 ARGVKW {brd_r}")
        print(f"{padding}{AMBER}└─────────────────────────────────╜{RESET}")

        self.set_user("Vendég")
        self._init_data()
        self._init_booking()
        sleep(1.5)
        self.main_menu()
