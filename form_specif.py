from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QTextEdit, QPushButton, QMessageBox, QWidget
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QSize
from construction_class.ground import *

class Specifications(QWidget):
    hor_headers = ['Название конструкции', 'tв, °С', 'tн, °С', 'n', 'A, м²', 'Ro,\nм²·ºС/Вт', 'n·A/Ro', '%']

    def __init__(self, parent=None):
        super().__init__()
        self.vbox = QVBoxLayout()
        # Элементы для вывода результатов
        self.label5 = QLabel('Вывод результата')
        self.vbox.addWidget(self.label5)
        self.result_text = QTextEdit()
        self.vbox.addWidget(self.result_text)
        parent.addLayout(self.vbox)

    def draw_table(self, building=None):
        """Перерисовка таблицы со слоями конструкции и других элементов"""
        # вывод результата расчета в текстовом поле
        self.result_text.clear()
        self.result_text.setHtml(building.get_text_spec_html())
