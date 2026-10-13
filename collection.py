from models import Car, Entity, STATUSES


class Fleet(Entity):
    def __init__(self):
        self._cars = []

    @property
    def cars(self):
        return list(self._cars)

    def add(self, car):
        if not isinstance(car, Car):
            raise TypeError("Можно добавлять только автомобили")
        if car in self._cars:
            return False
        self._cars.append(car)
        return True

    def remove(self, car):
        if car not in self._cars:
            return False
        self._cars.remove(car)
        return True

    def find(self, text="", status="Все"):
        text = text.strip().lower()
        result = []
        for car in self._cars:
            if text not in car.name.lower():
                continue
            if status != "Все" and car.status != status:
                continue
            result.append(car)
        return sorted(result)

    def count_by_status(self):
        return {status: sum(car.status == status for car in self._cars) for status in STATUSES}

    def total_price(self):
        return sum(car.price for car in self._cars)

    def sort_key(self):
        return (len(self._cars),)

    def __eq__(self, other):
        return isinstance(other, Fleet) and self._cars == other.cars

    def __len__(self):
        return len(self._cars)

    def __str__(self):
        return f"Автопарк: {len(self)} автомобилей"

    @staticmethod
    def seed():
        fleet = Fleet()
        examples = [
            ("Легковой", "Kia Rio", "Свободен", 2500, 2020),
            ("Легковой", "Hyundai Solaris", "В аренде", 2700, 2021),
            ("Легковой", "Volkswagen Polo", "Свободен", 2600, 2019),
            ("Легковой", "Toyota Camry", "На обслуживании", 4900, 2022),
            ("Внедорожник", "Renault Duster", "Свободен", 3800, 2020),
            ("Внедорожник", "Toyota RAV4", "В аренде", 5500, 2021),
            ("Внедорожник", "Nissan X-Trail", "Свободен", 5200, 2018),
            ("Микроавтобус", "Ford Transit", "Свободен", 6500, 2019),
            ("Микроавтобус", "Mercedes Sprinter", "В аренде", 8500, 2020),
        ]
        for kind, name, status, price, year in examples:
            fleet.add(Car.create(kind, name, status, price, year))
        return fleet
