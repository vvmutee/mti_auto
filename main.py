import sys
from PyQt6.QtWidgets import QApplication
from collection import Fleet
from report import Session
from windows import LoginWindow, MainWindow


class App:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.fleet = Fleet.seed()
        self.login_window = LoginWindow()
        self.main_window = None
        self.login_window.logged_in.connect(self.open_main)

    def open_main(self, login):
        session = Session.start(login)
        self.main_window = MainWindow(self.fleet, session)
        self.login_window.hide()
        self.main_window.show()

    def run(self):
        self.login_window.show()
        return self.app.exec()


if __name__ == "__main__":
    sys.exit(App().run())
