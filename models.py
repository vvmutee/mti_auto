from abc import ABC, abstractmethod
from functools import total_ordering

STATUSES = ("Свободен", "В аренде", "На обслуживании")
KINDS = ("Легковой", "Внедорожник", "Микроавтобус")


@total_ordering
class Entity(ABC):
    @abstractmethod
    def sort_key(self):
        pass

    def __lt__(self, other):
        if not isinstance(other, Entity):
            return NotImplemented
        return self.sort_key() < other.sort_key()


class Car(Entity):
    def __init__(self, name, status, price, year):
        self.name = name
        self.status = status
        self.price = price
        self.year = year

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        value = str(value).strip()
        if not value:
            raise ValueError("Введите марку и модель")
        self._name = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value not in STATUSES:
            raise ValueError("Неизвестный статус")
        self._status = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        value = int(value)
        if value < 0:
            raise ValueError("Стоимость не может быть отрицательной")
        self._price = value

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value):
        value = int(value)
        if not 1950 <= value <= 2100:
            raise ValueError("Некорректный год выпуска")
        self._year = value

    @abstractmethod
    def kind(self):
        pass

    def sort_key(self):
        return (self.name.lower(), self.year)

    def __eq__(self, other):
        return isinstance(other, Car) and self.name.lower() == other.name.lower() and self.year == other.year

    def __repr__(self):
        return f"{type(self).__name__}({self.name!r}, {self.status!r}, {self.price}, {self.year})"

    def __str__(self):
        return f"{self.name} ({self.year}), {self.kind()}, {self.status}, {self.price} руб./сутки"

    @staticmethod
    def create(kind, name, status, price, year):
        types = {"Легковой": PassengerCar, "Внедорожник": SUV, "Микроавтобус": Minibus}
        if kind not in types:
            raise ValueError("Неизвестный тип автомобиля")
        return types[kind](name, status, price, year)


class PassengerCar(Car):
    def kind(self):
        return "Легковой"


class SUV(Car):
    def kind(self):
        return "Внедорожник"


class Minibus(Car):
    def kind(self):
        return "Микроавтобус"
