from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (QDialog, QDialogButtonBox, QFormLayout, QHBoxLayout,
                             QLabel, QLineEdit, QMainWindow, QMessageBox, QPushButton,
                             QVBoxLayout, QWidget)
from models import Car
from report import ReportWriter
from widgets import (AddButton, CarTable, DeleteButton, NumberSpin,
                     SearchEdit, StatusCombo, StatusLabel, TypeCombo)


class LoginWindow(QWidget):
    logged_in = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Вход")
        self.setFixedSize(320, 180)
        title = QLabel("Учёт автомобилей в автопарке")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.login_edit = QLineEdit()
        self.login_edit.setPlaceholderText("Имя пользователя")
        self.login_edit.returnPressed.connect(self.try_login)
        self.error_label = QLabel("")
        self.enter_button = QPushButton("Войти")
        self.enter_button.clicked.connect(self.try_login)
        form = QFormLayout()
        form.addRow("Логин:", self.login_edit)
        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addLayout(form)
        layout.addWidget(self.error_label)
        layout.addWidget(self.enter_button)
        self.setLayout(layout)

    def try_login(self):
        login = self.login_edit.text().strip()
        if not login:
            self.error_label.setText("Введите логин")
            return
        self.logged_in.emit(login)


class CarDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Новый автомобиль")
        self._car = None
        self.type_combo = TypeCombo()
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Например, Lada Vesta")
        self.status_combo = StatusCombo(with_all=False)
        self.year_spin = NumberSpin(1950, 2100)
        self.year_spin.setValue(2022)
        self.price_spin = NumberSpin(0, 1000000)
        self.price_spin.setValue(2500)
        self.error_label = QLabel("")
        form = QFormLayout()
        form.addRow("Тип:", self.type_combo)
        form.addRow("Марка и модель:", self.name_edit)
        form.addRow("Статус:", self.status_combo)
        form.addRow("Год выпуска:", self.year_spin)
        form.addRow("Аренда, руб./сутки:", self.price_spin)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.button(QDialogButtonBox.StandardButton.Ok).setText("Добавить")
        buttons.button(QDialogButtonBox.StandardButton.Cancel).setText("Отмена")
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(self.error_label)
        layout.addWidget(buttons)
        self.setLayout(layout)

    def get_car(self):
        return self._car

    def accept(self):
        try:
            self._car = Car.create(self.type_combo.currentText(), self.name_edit.text(),
                                   self.status_combo.currentText(), self.price_spin.value(),
                                   self.year_spin.value())
        except ValueError as error:
            self.error_label.setText(str(error))
            return
        super().accept()


class MainWindow(QMainWindow):
    def __init__(self, fleet, session):
        super().__init__()
        self._fleet = fleet
        self._session = session
        self.setWindowTitle(f"Учёт автомобилей в автопарке — {session.login}")
        self.resize(850, 480)
        self.search_edit = SearchEdit()
        self.status_combo = StatusCombo()
        self.table = CarTable()
        self.stats_label = QLabel("")
        self.add_button = AddButton()
        self.delete_button = DeleteButton()
        self.status_label = StatusLabel()
        self.search_edit.textChanged.connect(self.refresh)
        self.status_combo.currentIndexChanged.connect(self.refresh)
        self.add_button.clicked.connect(self.add_car)
        self.delete_button.clicked.connect(self.delete_car)
        self.table.delete_pressed.connect(self.delete_car)
        top = QHBoxLayout()
        top.addWidget(QLabel("Поиск:"))
        top.addWidget(self.search_edit, 1)
        top.addWidget(QLabel("Статус:"))
        top.addWidget(self.status_combo)
        bottom = QHBoxLayout()
        bottom.addWidget(self.add_button)
        bottom.addWidget(self.delete_button)
        bottom.addStretch()
        bottom.addWidget(self.status_label)
        layout = QVBoxLayout()
        layout.addLayout(top)
        layout.addWidget(self.table, 1)
        layout.addWidget(self.stats_label)
        layout.addLayout(bottom)
        central = QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)
        self.refresh()

    def refresh(self):
        cars = self._fleet.find(self.search_edit.text(), self.status_combo.currentText())
        self.table.show_cars(cars)
        counts = self._fleet.count_by_status()
        self.stats_label.setText(
            f"Всего: {len(self._fleet)} | Свободно: {counts['Свободен']} | "
            f"В аренде: {counts['В аренде']} | На обслуживании: {counts['На обслуживании']}"
        )

    def add_car(self):
        dialog = CarDialog(self)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        car = dialog.get_car()
        if self._fleet.add(car):
            self.status_label.setText(f"Добавлен: {car.name}")
        else:
            self.status_label.setText("Такая модель с этим годом уже есть")
        self.refresh()

    def delete_car(self):
        car = self.table.selected_car()
        if car is None:
            self.status_label.setText("Сначала выберите автомобиль")
            return
        answer = QMessageBox.question(self, "Удаление", f"Удалить {car.name} ({car.year})?",
                                      QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if answer != QMessageBox.StandardButton.Yes:
            return
        self._fleet.remove(car)
        self.status_label.setText(f"Удалён: {car.name}")
        self.refresh()

    def closeEvent(self, event):
        self._session.close()
        try:
            ReportWriter.save(self._session)
        except OSError as error:
            QMessageBox.warning(self, "Ошибка отчёта", str(error))
        event.accept()
