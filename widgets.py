from datetime import datetime
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (QAbstractItemView, QComboBox, QHeaderView, QLabel,
                             QLineEdit, QPushButton, QSpinBox, QTableWidget, QTableWidgetItem)
from models import KINDS, STATUSES


class CarTable(QTableWidget):
    delete_pressed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(0, 5, parent)
        self._cars = []
        self.setHorizontalHeaderLabels(["Марка и модель", "Тип", "Статус", "Год", "Руб./сутки"])
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setAlternatingRowColors(True)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def show_cars(self, cars):
        self._cars = list(cars)
        self.setRowCount(len(self._cars))
        for row, car in enumerate(self._cars):
            for col, value in enumerate((car.name, car.kind(), car.status, str(car.year), str(car.price))):
                cell = QTableWidgetItem(value)
                cell.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.setItem(row, col, cell)

    def selected_car(self):
        row = self.currentRow()
        return self._cars[row] if 0 <= row < len(self._cars) else None

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Delete:
            self.delete_pressed.emit()
        else:
            super().keyPressEvent(event)


class SearchEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText("Поиск по марке и модели")
        self.setClearButtonEnabled(True)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.clear()
        else:
            super().keyPressEvent(event)


class StatusCombo(QComboBox):
    def __init__(self, with_all=True, parent=None):
        super().__init__(parent)
        if with_all:
            self.addItem("Все")
        self.addItems(STATUSES)


class TypeCombo(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.addItems(KINDS)


class NumberSpin(QSpinBox):
    def __init__(self, minimum, maximum, parent=None):
        super().__init__(parent)
        self.setRange(minimum, maximum)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)


class AddButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__("Добавить", parent)


class DeleteButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__("Удалить", parent)


class StatusLabel(QLabel):
    def setText(self, text):
        super().setText(f"[{datetime.now():%H:%M:%S}] {text}")
