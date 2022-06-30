from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QTextEdit, QPushButton, QMessageBox, QWidget
from PyQt5.QtGui import QIcon, QTextCursor
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QSize
from construction_class.ground import *

class Specifications(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.vbox = QVBoxLayout()
        # Элементы для вывода результатов
        self.label5 = QLabel('Вывод результата')
        self.vbox.addWidget(self.label5)
        self.result_text = QTextEdit()
        self.vbox.addWidget(self.result_text)
        self.cursor = self.result_text.textCursor()
        parent.addLayout(self.vbox)

    def draw_specif(self, building=None):
        """Перерисовка таблицы со слоями конструкции и других элементов"""
        # вывод результата расчета в текстовом поле
        self.result_text.clear()
        building.get_text_spec_html(self.result_text)
        # перемещение в начало текста
        self.cursor.movePosition(QTextCursor.Start)
        self.result_text.setTextCursor(self.cursor)

    def draw_result(self, building=None):
        # вывод результата расчета в текстовом поле
        self.result_text.clear()
        building.get_text_calulation_html(self.result_text)
        # перемещение в начало текста
        self.cursor.movePosition(QTextCursor.Start)
        self.result_text.setTextCursor(self.cursor)

    def draw_pasport(self, building=None):
        # вывод паспорта в текстовом поле
        self.result_text.clear()
        building.get_text_pasport_html(self.result_text)
        # перемещение в начало текста
        self.cursor.movePosition(QTextCursor.Start)
        self.result_text.setTextCursor(self.cursor)

    def draw_class(self, building=None):
        # вывод класса в текстовом поле
        self.result_text.clear()
        building.get_text_class_html(self.result_text)
        # перемещение в начало текста
        self.cursor.movePosition(QTextCursor.Start)
        self.result_text.setTextCursor(self.cursor)
