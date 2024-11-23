import random
from datetime import datetime, timedelta
from functools import reduce
from time import sleep

from model.BelfoldiJarat import BelfoldiJarat
from model.Jarat import Jarat
from model.JegyFoglalas import JegyFoglalas
from model.Legitarsasag import Legitarsasag
from model.NemzetkoziJarat import NemzetkoziJarat
from model.Seat import Seat
from utils.utils import clear_screen, resize_console, prompt
from view.colors import GREY, AMBER, RESET, GREEN, RED, WHITE, BLACK, BG_BLUE, BOLD, BLUE, ITALIC, PURPLE, GRASS


class Repter:
    def __init__(self):
        self._user = ""
        self._airlines: list[Legitarsasag] = []
        self._bookings: list[JegyFoglalas] = []
        self._selected_flight: Jarat | None = None

    @property
    def airlines(self):
        return self._airlines

    @airlines.setter
    def airlines(self, new_airline: Legitarsasag):
        self._airlines.append(new_airline)

    @property
    def selected_flight(self):
        flight, airline = self.find_flight(self._selected_flight.flight_id)
        return f"{GREEN}{flight.flight_id}. {airline.name} {flight.destination} {flight.ticket_price}{RESET}€"

    def flight_details(self, flight_id):
        flight, airline = self.find_flight(flight_id)
        return f"{GREEN}{flight.flight_id}. {airline.name} {flight.destination} {flight.ticket_price}{RESET}€"

    def _init_data(self):
        today_date = datetime.today()
        today = today_date.strftime('%Y-%m-%d')

        yesterday_date = today_date + timedelta(days=-1)
        yesterday = yesterday_date.strftime('%Y-%m-%d')

        tomorrow_date = today_date + timedelta(days=-1)
        tomorrow = tomorrow_date.strftime('%Y-%m-%d')

        days = [today, today, yesterday, yesterday, tomorrow, tomorrow]
        random.shuffle(days)

        times = ["17:50", "19:20", "9:30", "10:40", "13:45", "15:30"]
        random.shuffle(times)

        self.airlines = Legitarsasag("Luft Panda", [
            NemzetkoziJarat(1, "A", "Kuala Lumpur", f"{days[0]} {times[0]}", f"{today} {random.choice(times)}", 1200.00, 120),
            BelfoldiJarat(2, "A", "Debrecen", f"{days[1]} {times[1]}", f"{today} {random.choice(times)}", 250.00, 60),
            BelfoldiJarat(3, "A", "Szolnok", f"{days[2]} {times[2]}", f"{today} {random.choice(times)}", 250.00, 60)
        ])
        self.airlines = Legitarsasag("Brian Air", [
            NemzetkoziJarat(4,"B", "Róma", f"{days[3]} {times[3]}", f"{today} {random.choice(times)}", 1000.00, 120),
            NemzetkoziJarat(5, "B", "Betlehem", f"{days[4]} {times[4]}", f"{today} {random.choice(times)}", 1100.00, 120),
            BelfoldiJarat(6, "B", "Szentkirályszabadja", f"{days[5]} {times[5]}", f"{today} {random.choice(times)}", 250.00, 60)
        ])

    def _init_booking(self):
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
                    f"{AMBER}{flight.flight_id}.{RESET} {airline.name}:\t{flight.destination: <20}Terminál {flight.terminal} {flight.departure: <18} {flight.ticket_price}€")

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

    def manage_bookings(self, is_redemption: bool = False, message: str = ""):
        padding = " " * 56
        padding_msg = " " * 52

        while True:
            my_bookings: list[JegyFoglalas] = list(filter((lambda b: b.user == self._user), self._bookings))
            my_booking_count = len(my_bookings)

            if my_booking_count > 0:
                print(f"{AMBER}Az Ön által leadott foglalások:{RESET}")

                for i, booking in enumerate(my_bookings):
                    ticket_count = len(booking.tickets)
                    if ticket_count:
                        flight, airline = self.find_flight(booking.flight_id)
                        flight_info = f"{AMBER}{i + 1}.{RESET} {f"{airline.name}:": <12} {flight.destination: <20} {flight.departure: <18}"
                        ticket_info = f"{f"Jegy: {GREEN}{ticket_count}{RESET} db.": <12} {booking.total}€"
                        ticket_payment = f"{GREEN}Fizetve{RESET}" if booking.is_paid else f"{AMBER}Fizetendő{RESET}"
                        print(f"{flight_info} {ticket_info: <30} {ticket_payment}")

                total = reduce((lambda sub_total, b: sub_total + b.total), my_bookings, 0)
                outstanding = reduce((lambda sub_total, b: sub_total + b.total_outstanding), my_bookings, 0)

                print(f"\n{padding}{"Összesen:": <12} {WHITE}{total}{RESET}€")
                if outstanding:
                    print(f"{padding}{"Fizetendő:": <12} {AMBER}{outstanding}{RESET}€")
                print(f"{message}\n" if message else "")

                payment_label = f"Fizetés (F) " if outstanding and not is_redemption else ""
                redemption_index = f"1-{my_booking_count}" if my_booking_count > 1 else "L"
                redeem_all_label = " Összes lemondása (L)" if is_redemption and my_booking_count > 1 else ""
                redemption_label = f"Lemondás ({redemption_index})" if is_redemption else ""
                _prompt = input(f"{payment_label}{redemption_label}{redeem_all_label} Folytatás (Enter) ")

                try:
                    index = int(_prompt)
                except Exception:
                    index = -1

                if outstanding and _prompt.lower() == "f":
                    clear_screen()
                    payed_amount = 0

                    for my_booking in my_bookings:
                        payed_amount += my_booking.pay_all()

                    payed_msg = f"{padding_msg}Sikeres fizetés! {GREEN}{payed_amount}{RESET}€" if payed_amount else ""
                    return self.manage_bookings(is_redemption, payed_msg)

                elif is_redemption and total and 0 < index <= my_booking_count:
                    clear_screen()
                    redemption_amount = 0

                    my_booking = my_bookings[index - 1]
                    flight, _ = self.find_flight(my_booking.flight_id)
                    for ticket in my_booking.tickets:
                        flight.cancel_seat(ticket.seat_number)
                    redemption_amount += my_booking.redeem_all()
                    self._bookings.remove(my_booking)

                    redemption_msg = f" Visszatérítés: {RESET}{redemption_amount}€" if redemption_amount else f"{RESET} (Nem történt fizetés)"
                    cancellation_msg = f"{AMBER}Sikeres lemondás!{redemption_msg}"

                    return self.manage_bookings(is_redemption, cancellation_msg)

                elif is_redemption and total and _prompt.lower() == "l":
                    clear_screen()
                    redemption_amount = 0

                    for my_booking in my_bookings:
                        flight, _ = self.find_flight(my_booking.flight_id)
                        for ticket in my_booking.tickets:
                            flight.cancel_seat(ticket.seat_number)
                        redemption_amount += my_booking.redeem_all()
                        self._bookings.remove(my_booking)

                    redemption_msg = f" Visszatérítés: {RESET}{redemption_amount}€" if redemption_amount else f"{RESET} (Nem történt fizetés)"
                    cancellation_msg = f"{AMBER}Sikeres lemondás!{redemption_msg}"

                    return self.manage_bookings(is_redemption, cancellation_msg)
                else:
                    return
            else:
                print(message)
                print(f"{RESET}Nem található foglalás.")
                input("Vissza (Enter)")
                return

    def choose_flight(self, message: str = "") -> Jarat | None:
        clear_screen()
        while True:
            print(f"{AMBER}Kérjük, válasszon járatot!{RESET}\n")
            self.list_flights()

            print(f"{message}\nVissza (0) Járatválasztás (1-6)\n")
            flight_id = prompt("> ")

            if flight_id == "0":
                self.main_menu()
                return

            try:
                flight, _ = self.find_flight(int(flight_id))
                if flight:
                    self._selected_flight = flight
                    return flight
                else:
                    return self.choose_flight(f"{RED}Nem található járat a megadott azonosítóval.{RESET}")

            except Exception:
                return self.choose_flight(f"{RED}Hiba!{RESET} Kérjük csak egész számot adjon meg.")

    def choose_seat(self, message: str = ""):
        selected_seat: Seat
        selected_flight = self._selected_flight

        prev_booking = list(filter(lambda b: b.flight_id == selected_flight.flight_id and b.user == self._user, self._bookings))
        flight_booking = (prev_booking and prev_booking[0] or JegyFoglalas(selected_flight.flight_id, self._user))
        has_booked_seat = len(flight_booking.seat_numbers) > 0
        book_label = f"Foglalás (1-{selected_flight.seat_count})"
        print_message = ""

        clear_screen()
        print(f"{AMBER}{selected_flight.type}:{RESET} {self.selected_flight}")
        print(f"{AMBER}Ülőhelyek:{RESET} {GREEN}{self._selected_flight.seats_free}{RESET}/{selected_flight.seat_count} szabad")
        print(f"{GRASS}■{RESET} saját foglalás   {PURPLE}■{RESET} egyéb foglalások\n")

        while True:
            selected_flight.list_seats(flight_booking.seat_numbers)

            print(f"\n{message}" if message else f"\n{AMBER}Kérjük válasszon az elérhető helyek közül{RESET}")
            _prompt = prompt(f"Vissza (0) {book_label} Folytatás (Enter)\n> " if has_booked_seat else f"Vissza (0) {book_label}\n> ").strip()

            if _prompt == "0":
                self.choose_flight()
                break

            if _prompt == "" and has_booked_seat:
                return

            try:
                seat_number = int(_prompt)
                selected_seat = self.find_seat(selected_flight.flight_id, seat_number)

                if selected_seat:
                    if selected_seat.is_booked:
                        print_message = f"{AMBER}A megadott ülőhely ({RESET}{seat_number}{AMBER}) már foglalt.{RESET}"
                        break
                    else:
                        self._selected_flight.book_seat(seat_number)
                        flight_booking.book_ticket(selected_flight.flight_id, seat_number, selected_flight.ticket_price, self._user)

                        if not self._bookings.count(flight_booking):
                            self._bookings.append(flight_booking)

                        print_message = (f"{AMBER}A lefoglalt ülőhely: {RESET}{GREEN}{selected_seat.number}.{RESET}"
                                         + f"\t{self._selected_flight.ticket_price}€{RESET}")
                        break
                else:
                    print_message = f"{AMBER}A megadott ülőhely ({RESET}{seat_number}{AMBER}) nem található.{RESET}"
                    break
            except Exception:
                print_message = f"{RED}Hiba!{RESET} Kérjük csak egész számot adjon meg, és a számjegyek között ne legyen szóköz."
                break

        return self.choose_seat(print_message)

    def view_flight_bookings(self, current_booking_index=0, message=""):
        clear_screen()

        my_bookings_count = len(self._bookings)

        if my_bookings_count == 0:
            print(f"{RESET} Nem található foglalás")
            prompt("Vissza (Enter)")

        while True:
            current_flight_id = self._bookings[current_booking_index].flight_id
            current_flight, _ = self.find_flight(current_flight_id)
            print(f"{AMBER}{current_flight.type}:{RESET} {self.flight_details(current_flight_id)}")
            print(
                f"{AMBER}Ülőhelyek:{RESET} {GREEN}{current_flight.seats_free}{RESET}/{current_flight.seat_count} szabad")
            print(f"{GRASS}■{RESET} saját foglalás   {PURPLE}■{RESET} egyéb foglalások\n")
            current_flight.list_seats(self._bookings[current_booking_index].seat_numbers)

            _prompt = prompt(f"\n{"Vissza (0)  Következő (Enter)" if my_bookings_count > 1 else "Vissza (Enter)"} {message}")

            if _prompt == "0" or (_prompt == "" and my_bookings_count == 1):
                return
            elif _prompt == "" and my_bookings_count > 1:
                next_booking_index = current_booking_index + 1 if current_booking_index + 1 < len(self._bookings) else 0
                return self.view_flight_bookings(next_booking_index)
            else:
                return self.view_flight_bookings(current_booking_index, f"{RED}Érvénytelen karakter{RESET}")

    def main_menu(self):
        border = BLUE
        l = f"{border}│{RESET}"

        while True:
            clear_screen()

            badge = f" ({GREEN}{len(self._bookings)}{RESET})"
            my_bookings = f"{badge: <17}" if len(self._bookings) > 0 else ""

            x = f"{GREY}[{RESET}x{GREY}]{RESET}"
            padding = " " * 30

            print("\n" * 3)
            print(f"{padding}{border}┌─{BOLD} Reptér{PURPLE}♪ {RESET}{border}───────────────┐{RESET}")
            print(f"{padding}{border}│                         │{RESET}")
            print(f"{padding}{l} {AMBER} 1.{RESET} Jegyfoglalás        {l}")
            print(f"{padding}{border}│                         │{RESET}")
            print(f"{padding}{l} {AMBER} 2.{RESET} Foglalásaim{my_bookings: <8} {l}")
            print(f"{padding}{border}│                         │{RESET}")
            print(f"{padding}{l} {AMBER} 3.{RESET} Jegylemondás        {l}")
            print(f"{padding}{border}│                         │{RESET}")
            if my_bookings:
                print(f"{padding}{l} {AMBER} 4.{RESET} Járatfoglaltság     {l}")
                print(f"{padding}{border}│                         │{RESET}")
            print(f"{padding}{l} {x} Kilépés             {l}")
            print(f"{padding}{border}│                         │{RESET}")
            print(f"{padding}{border}└────────────────── {ITALIC}v1.0 ─┘{RESET}")
            _prompt = prompt(f"{padding}   ")

            if _prompt == "1":
                clear_screen()
                flight = self.choose_flight()

                if not flight:
                    continue

                self.choose_seat()
                clear_screen()

                if len(self._bookings):
                    self.manage_bookings()

            elif _prompt == "2":
                clear_screen()
                self.manage_bookings()
            elif _prompt == "3":
                clear_screen()
                self.manage_bookings(True)
            elif my_bookings and _prompt == "4":
                self.view_flight_bookings()
            elif _prompt == "X" or _prompt == "x":
                clear_screen()
                print("Viszontlátásra!")
                sleep(1)
                break

    def start(self):
        resize_console(88, 28)
        clear_screen()

        brd_l = f"{BG_BLUE}{WHITE}│{BG_BLUE}"
        brd_r = f"{BG_BLUE}{WHITE}║{RESET}"
        padding = " " * 24

        print("\n" * 3)
        print(f"{padding}{BG_BLUE}{WHITE}╒═════════════════════════════════╗{RESET}")
        print(f"{padding}{brd_l} {AMBER}{BOLD}Reptér CLI v1.0{RESET}{BG_BLUE}{BLACK} (c) 2024 {BOLD}ARGVKW {RESET}{brd_r}")
        print(f"{padding}{BG_BLUE}{WHITE}└─────────────────────────────────╜{RESET}")
        print("\n" * 5)

        self.set_user("Vendég")
        self._init_data()
        self._init_booking()
        sleep(1.5)
        self.main_menu()
