from datetime import datetime

from models import Entity

TIME_FORMAT = "%d.%m.%Y %H:%M:%S"


class Session(Entity):
    def __init__(self, login, time_in):
        self._login = ""
        self._time_in = time_in
        self._time_out = None
        self.login = login

    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, value):
        value = str(value).strip()
        if value == "":
            raise ValueError("Логин не может быть пустым")
        self._login = value

    @property
    def time_in(self):
        return self._time_in

    @time_in.setter
    def time_in(self, value):
        self._time_in = value

    @property
    def time_out(self):
        return self._time_out

    @time_out.setter
    def time_out(self, value):
        self._time_out = value

    def time_in_text(self):
        return self._time_in.strftime(TIME_FORMAT)

    def time_out_text(self):
        if self._time_out is None:
            return ""
        return self._time_out.strftime(TIME_FORMAT)

    def close(self):
        self._time_out = datetime.now()

    def sort_key(self):
        return (self._time_in,)

    def __eq__(self, other):
        if not isinstance(other, Session):
            return False
        return (
            self._login == other.login
            and self._time_in == other.time_in
            and self._time_out == other.time_out
        )

    def __repr__(self):
        return f"Session({self._login!r}, {self.time_in_text()!r}, {self.time_out_text()!r})"

    def __str__(self):
        return f"{self._login}: {self.time_in_text()} - {self.time_out_text()}"

    @staticmethod
    def start(login):
        return Session(login, datetime.now())


class ReportWriter:
    @staticmethod
    def build(session):
        names = ["login", "time_in", "time_out"]
        values = [session.login, session.time_in_text(), session.time_out_text()]
        head = "|"
        line = "|"
        row = "|"
        for i in range(3):
            width = max(len(names[i]), len(values[i]))
            head += " " + names[i].ljust(width) + " |"
            line += "-" * (width + 2) + "|"
            row += " " + values[i].ljust(width) + " |"
        border = "+" + "-" * (len(head) - 2) + "+"
        return border + "\n" + head + "\n" + line + "\n" + row + "\n" + border + "\n"

    @staticmethod
    def save(session):
        with open("report.txt", "w", encoding="utf-8") as file:
            file.write(ReportWriter.build(session))
