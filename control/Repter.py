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
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Repter, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self._user = ""
        self._airlines: list[Legitarsasag] = []
        self._bookings: list[JegyFoglalas] = []
        self._selected_flight: Jarat | None = None
        self._travel_date = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)

    @staticmethod
    def is_bookable(flight):
        now = datetime.now()
        departure = datetime.strptime(flight.departure, "%Y.%m.%d. %H:%M")
        return departure - now > timedelta(minutes=0)

    @staticmethod
    def format_time(date: datetime, add_hours=0):
        _date = date + timedelta(hours=add_hours)
        return datetime.strftime(_date, "%Y.%m.%d. %H:%M")

    @property
    def airlines(self):
        return self._airlines

    @airlines.setter
    def airlines(self, new_airline: Legitarsasag):
        self._airlines.append(new_airline)

    @property
    def selected_flight(self):
        return self.flight_details(self._selected_flight.flight_id)

    def flight_details(self, flight_id):
        flight, airline = self.find_flight(flight_id)
        return f"{GREEN}{flight.flight_id}. {airline.name} - {flight.destination} {RESET}[{GREEN}{flight.departure}{RESET}]"

    def _init_data(self):
        today = self._travel_date
        yesterday = today + timedelta(days=-1)
        tomorrow = today + timedelta(days=+1)

        days = [today, today, yesterday, yesterday, tomorrow, tomorrow]
        random.shuffle(days)

        hours = [9, 10, 13, 15, 17, 19]
        random.shuffle(hours)

        minutes = [50, 20, 30, 40, 45, 30]
        random.shuffle(minutes)

        def create_time(i: int, add_hours=0):
            date = days[i] + timedelta(hours=hours[i], minutes=minutes[i])
            return self.format_time(date, add_hours)

        self.airlines = Legitarsasag("Luft Panda", [
            NemzetkoziJarat(random.randint(1, 9999), "A", "Kuala Lumpur", create_time(0), create_time(0, 7), 1200.00, 120),
            BelfoldiJarat(random.randint(1, 9999), "A", "Debrecen", create_time(1), create_time(1, 1), 250.00, 60),
            BelfoldiJarat(random.randint(1, 9999), "A", "Szolnok", create_time(2), create_time(2, 1), 250.00, 60)
        ])
        self.airlines = Legitarsasag("Brian Air", [
            NemzetkoziJarat(random.randint(1, 9999), "B", "Róma", f"{create_time(3)}", f"{create_time(3, 3)}", 1000.00, 120),
            NemzetkoziJarat(random.randint(1, 9999), "B", "Betlehem", f"{create_time(4)}", f"{create_time(4, 4)}", 1100.00, 120),
            BelfoldiJarat(random.randint(1, 9999), "B", "Szentkirályszabadja", f"{create_time(5)}", f"{create_time(5, 1)}", 250.00, 60)
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

        print(f"{padding}{RESET}{BOLD}Üdvözöljük, {AMBER}{new_user}{RESET}!\n")

    def set_travel_date(self, message=""):
        p = 24
        padding = " " * p

        while True:
            msg = f"\n{RESET}{padding}{message}{GREEN}" if message else ""
            date = prompt(f"{AMBER}Utazás időpontja (ÉÉÉÉ.HH.NN.){RESET}\n{padding}Vagy a mai nap (Enter){msg}", p)
            result = self.update_travel_date(date, padding)

            if type(result) is bool:
                return
            else:
                clear_screen()
                return self.set_travel_date(result)

    def update_travel_date(self, date: str, padding=""):
        if date == "":
            return False

        try:
            travel_date = datetime.strptime(date, "%Y.%m.%d.")

        except Exception:
            error_msg = f"{RED}Érvénytelen dátum.{RESET}"
            error_hint = f"\n{padding}Használja a megadott formátumot. Pl.: {datetime.strftime(datetime.today(), "%Y.%m.%d.")}"

            return f"{error_msg} {error_hint}"

        if travel_date == self._travel_date:
            return False

        time_diff = travel_date - datetime.today()

        if time_diff < timedelta(days=-1):
            return f"{RED}Múltbeli dátum nem foglalható.{RESET}"

        elif time_diff > timedelta(days=365):
            return f"{RED}Egy évnél későbbi dátum nem foglalható.{RESET}"

        self._travel_date = travel_date
        return True

    def list_airlines(self):
        for airline in self._airlines:
            print(airline.name)

    def list_flights(self):
        for i, airline in enumerate(self._airlines):
            if i > len(self._airlines) - 5:
                for flight in airline.flights:
                    flight_info = f"{airline.name}:\t{flight.destination: <20}Terminál {flight.terminal} {flight.departure: <18} {flight.flight_duration} óra {flight.ticket_price}€"
                    if self.is_bookable(flight):
                        print(
                            f"{AMBER}{flight.flight_id}.{RESET} {flight_info}")
                    else:
                        print(
                            f"{GREY}{flight.flight_id}. {flight_info}{RESET}")

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

            print(f"{message}\nVissza (0) Járatválasztás (1-9999) Időpontmódosítás (ÉÉÉÉ.HH.NN.)")
            _prompt = prompt()

            if _prompt == "0":
                self.main_menu()
                return

            try:
                flight, _ = self.find_flight(int(_prompt))
                if flight:
                    if self.is_bookable(flight):
                        self._selected_flight = flight
                        return flight
                    else:
                        return self.choose_flight(f"{RED}Ez a járat nem választható a megadott időponbtban.{RESET}")
                else:
                    return self.choose_flight(f"{RED}Nem található járat a megadott azonosítóval.{RESET}")

            except Exception:

                result = self.update_travel_date(_prompt)

                if type(result) is bool:
                    if result:
                        self._init_data()
                        self._init_booking()
                    return self.choose_flight()
                else:
                    clear_screen()
                    return self.choose_flight(result)
                # return self.choose_flight(f"{RED}Hiba!{RESET} Kérjük csak egész számot adjon meg.")

    def choose_seat(self, message: str = ""):
        clear_screen()
        selected_seat: Seat
        selected_flight = self._selected_flight
        print_message = ""

        prev_booking = list(
            filter(lambda b: b.flight_id == selected_flight.flight_id and b.user == self._user, self._bookings))
        flight_booking = (prev_booking and prev_booking[0] or JegyFoglalas(selected_flight.flight_id, self._user))
        has_booked_seat = len(flight_booking.seat_numbers) > 0
        book_label = f"Foglalás (1-{selected_flight.seat_count})"

        seats_available = f"{AMBER}Ülőhelyek:{RESET} {GREEN}{selected_flight.seats_free}{RESET}/{selected_flight.seat_count} szabad"
        flight_time = f"{AMBER}Menetidő:{RESET} {selected_flight.flight_duration} óra"
        ticket_price = f"{AMBER}Jegyár:{RESET} {selected_flight.ticket_price}€"

        print(f"{AMBER}{selected_flight.type}:{RESET} {self.selected_flight}")
        print(f"{seats_available} {flight_time} {ticket_price}")
        print(f"{GRASS}■{RESET} saját foglalás   {PURPLE}■{RESET} egyéb foglalások\n")

        while True:
            selected_flight.list_seats(flight_booking.seat_numbers)

            print(f"\n{message}" if message else f"\n{AMBER}Kérjük válasszon az elérhető helyek közül{RESET}")
            _prompt = prompt(
                f"Vissza (0) {book_label} Folytatás (Enter)" if has_booked_seat else f"Vissza (0) {book_label}").strip()

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
                        flight_booking.book_ticket(selected_flight.flight_id, seat_number, selected_flight.ticket_price,
                                                   self._user)

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
            input("Vissza (Enter)")

        while True:
            current_flight_id = self._bookings[current_booking_index].flight_id
            current_flight, _ = self.find_flight(current_flight_id)
            seats_available = f"{AMBER}Ülőhelyek:{RESET} {GREEN}{current_flight.seats_free}{RESET}/{current_flight.seat_count} szabad"
            flight_time = f"{AMBER}Menetidő:{RESET} {current_flight.flight_duration} óra"
            ticket_price = f"{AMBER}Jegyár:{RESET} {current_flight.ticket_price}€"

            print(f"{AMBER}{current_flight.type}:{RESET} {self.flight_details(current_flight_id)}")
            print(f"{seats_available} {flight_time} {ticket_price}")
            print(f"{GRASS}■{RESET} saját foglalás   {PURPLE}■{RESET} egyéb foglalások\n")

            current_flight.list_seats(self._bookings[current_booking_index].seat_numbers)

            _prompt = input(
                f"\n{"Vissza (0)  Következő (Enter)" if my_bookings_count > 1 else "Vissza (Enter)"} {message}")

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
            padding = 30
            p = " " * padding

            print("\n" * 3)
            print(f"{p}{border}┌─{BOLD} Reptér{PURPLE}♪ {RESET}{border}───────────────┐{RESET}")
            print(f"{p}{border}│                         │{RESET}")
            print(f"{p}{l} {AMBER} 1.{RESET} Jegyfoglalás        {l}")
            print(f"{p}{border}│                         │{RESET}")
            print(f"{p}{l} {AMBER} 2.{RESET} Foglalásaim{my_bookings: <8} {l}")
            print(f"{p}{border}│                         │{RESET}")
            print(f"{p}{l} {AMBER} 3.{RESET} Jegylemondás        {l}")
            print(f"{p}{border}│                         │{RESET}")
            if my_bookings:
                print(f"{p}{l} {AMBER} 4.{RESET} Járatfoglaltság     {l}")
                print(f"{p}{border}│                         │{RESET}")
            print(f"{p}{l} {x} Kilépés             {l}")
            print(f"{p}{border}│                         │{RESET}")
            print(f"{p}{border}└────────────────── {ITALIC}v1.0 ─┘{RESET}")
            _prompt = prompt("", padding)

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
                quit()

    def start(self):
        resize_console(88, 28)
        clear_screen()

        brd_l = f"{BG_BLUE}{WHITE}│{BG_BLUE}"
        brd_r = f"{BG_BLUE}{WHITE}║{RESET}"
        padding = " " * 24

        print("\n" * 3)
        print(f"{padding}{BG_BLUE}{WHITE}╒═════════════════════════════════╗{RESET}")
        print(
            f"{padding}{brd_l} {AMBER}{BOLD}Reptér CLI v1.0{RESET}{BG_BLUE}{BLACK} (c) 2024 {BOLD}ARGVKW {RESET}{brd_r}")
        print(f"{padding}{BG_BLUE}{WHITE}└─────────────────────────────────╜{RESET}")
        print("\n" * 5)

        self.set_user("Vendég")
        self.set_travel_date()
        self._init_data()
        self._init_booking()
        self.main_menu()
