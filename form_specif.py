from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QTextEdit, QPushButton, QMessageBox, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QIcon, QTextCursor
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QSize
from construction_class.ground import *

class Specifications(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.vbox = QVBoxLayout()
        # Элементы для вывода результатов
        self.result_text = QWebEngineView()
        self.vbox.addWidget(self.result_text)
        parent.addLayout(self.vbox)

    def draw_specif(self, building=None):
        """Вывод расчет удельной теплотехнической характеристики"""
        building.get_spec_html(self.result_text)

    def draw_result(self, building=None):
        """Вывод расчета паспорта в html-формате"""
        building.get_calсulation_html(self.result_text)

    def draw_pasport(self, building=None):
        """Вывод паспорта в html-формате"""
        building.get_pasport_html(self.result_text)

    def draw_class(self, building=None):
        """Вывод расчета класса энергетической эффективности в html-формате"""
        building.get_class_html(self.result_text)

