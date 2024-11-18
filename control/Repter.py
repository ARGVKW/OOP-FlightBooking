from model.BelfoldiJarat import BelfoldiJarat
from model.Legitarsasag import Legitarsasag
from model.NemzetkoziJarat import NemzetkoziJarat

class Repter:
    def __init__(self):
        self._user = "Vendég"
        self._airlines: list[Legitarsasag] = []
        self._selected_flight = None
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
        _user = input("Adjon meg egy felhasználónevet: \n")
        new_user = _user or user
        self._user = new_user
        print(f"Üdvözöljük, {new_user}!\n")

    def list_airlines(self):
        for airline in self._airlines:
            print(airline.name)

    def list_flights(self):
        for airline in self._airlines:
            for flight in airline.flights:
                print(f"{flight.flight_id}.\t{flight.destination}\t\t\t{flight.ticket_price}€")

    def find_flight_by_id(self, flight_id: int):
        for airline in self._airlines:
            for flight in airline.flights:
                if flight.flight_id == flight_id:
                    return flight
        return False

    def choose_flight(self):
        while True:
            print("Kérjük, válasszon járatot!")
            self.list_flights()
            flight_id = input("")

            flight = self.find_flight_by_id(int(flight_id))
            if flight:
                self._selected_flight = flight
                break
            else:
                print("Nem található járat a megadott azonosítóval.")

        selected_flight = self._selected_flight
        print("A kiválasztott járat: ")
        print(f"{selected_flight.flight_id}.\t{selected_flight.destination}\t{selected_flight.ticket_price}€")
        while True:
            proceed = input("Folytatás (1) Módosítás (2)\n")
            if proceed == "1":
                return selected_flight
            elif proceed == "2":
                return self.choose_flight()


    def start(self):
        print("╒═════════════════════════════════╗")
        print("│ Reptér CLI v1.0 (c) 2024 ARGVKW ║")
        print("└─────────────────────────────────╜")

        self.set_user("Teszt")

        flight = self.choose_flight()
        print(dir(flight))

