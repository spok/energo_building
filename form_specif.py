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
        self.label1 = QLabel('Теплофизическая харакетристика здания')
        self.vbox.addWidget(self.label1)
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(self.hor_headers)
        self.table.horizontalHeader().setVisible(True)
        self.table.setColumnWidth(0, 250)
        self.table.setColumnWidth(1, 50)
        self.table.setColumnWidth(2, 50)
        self.table.setColumnWidth(3, 50)
        self.table.setColumnWidth(4, 80)
        self.table.setColumnWidth(5, 80)
        self.table.setColumnWidth(6, 80)
        self.table.setColumnWidth(7, 50)
        # self.table.resizeColumnsToContents()
        self.vbox.addWidget(self.table)
        # Элементы для вывода результатов
        self.label5 = QLabel('Вывод результата')
        self.vbox.addWidget(self.label5)
        self.result_text = QTextEdit()
        self.vbox.addWidget(self.result_text)
        parent.addLayout(self.vbox)

    def draw_table(self, building=None):
        """Перерисовка таблицы со слоями конструкции и других элементов"""
        self.table.clear()
        self.table.setHorizontalHeaderLabels(self.hor_headers)
        building.draw_table_specif(self.table)
        # вывод результата расчета в текстовом поле
        self.result_text.clear()
        self.result_text.setText(building.get_text_spec())
