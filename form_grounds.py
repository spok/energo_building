from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QTextEdit, QPushButton, QMessageBox, QWidget
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QSize
from construction_class.ground import *
from func import to_float, load_windows_koef, MyCombo


class Grounds(QWidget):
    hor_headers = ['Название участка', 'Площадь 1 зоны, м²', 'Площадь 2 зоны, м²', 'Площадь 3 зоны, м²',
                   'Площадь 4 зоны, м²', '', '']

    def __init__(self, parent=None):
        super().__init__()
        self.build = None
        self.current_doors = None
        self.vbox = QVBoxLayout()
        self.label1 = QLabel('Конструкции в контакте с грунтом')
        self.vbox.addWidget(self.label1)
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(self.hor_headers)
        self.table.horizontalHeader().setVisible(True)
        self.table.setColumnWidth(0, 100)
        self.table.setColumnWidth(1, 80)
        self.table.setColumnWidth(2, 80)
        self.table.setColumnWidth(3, 80)
        self.table.setColumnWidth(4, 80)
        self.table.setColumnWidth(5, 20)
        self.table.setColumnWidth(6, 20)
        self.table.resizeColumnsToContents()
        self.vbox.addWidget(self.table)
        # Элементы для вывода результатов
        self.label5 = QLabel('Вывод результата')
        self.vbox.addWidget(self.label5)
        self.result_text = QTextEdit()
        self.vbox.addWidget(self.result_text)
        parent.addLayout(self.vbox)
        # Установка сигналов
        self.table.itemChanged.connect(self.get_change)

    def build_table(self, build=None, index=0):
        self.build = build
        self.current_ground = self.build.constructions[index]
        self.draw_table()

    def draw_table(self):
        """Перерисовка таблицы со слоями конструкции и других элементов"""
        self.table.blockSignals(True)
        self.table.clear()
        self.table.setHorizontalHeaderLabels(self.hor_headers)
        self.current_ground.draw_table(table=self.table)
        for i in range(self.table.rowCount()):
            # добавление кнопки для добавления пустого слоя
            el_but = self.table.cellWidget(i, 5)
            el_but.clicked.connect(self.add_ground)
            # добавление кнопки для удаления активного слоя
            el_but = self.table.cellWidget(i, 6)
            el_but.clicked.connect(self.delete_ground)
        self.table.blockSignals(False)
        # вывод результата расчета в текстовом поле
        self.result_text.clear()
        self.result_text.setText(self.current_ground.get_text_result())

    def get_change(self):
        """Сохранение внесенных изменений"""
        # Сохранение изменений в таблице
        cur_row = self.table.currentRow()
        if cur_row > -1:
            current_ground = self.current_ground.elements[cur_row]
            current_ground.name = self.table.item(cur_row, 0).text()
            current_ground.area.clear()
            for i in range(4):
                current_ground.area.append(to_float(self.table.item(cur_row, i + 1).text()))
        # Пересчет конструкций
        self.build.calc()
        # вывод результата расчета в текстовом поле
        self.result_text.clear()
        self.result_text.setText(self.current_ground.get_text_result())

    def add_ground(self):
        """Добавление нового слоя"""
        self.current_ground.add_ground(index=self.table.currentRow())
        self.draw_table()

    def delete_ground(self):
        """Удаление активного слоя"""
        if self.table.rowCount() > 1:
            cur = self.table.currentRow()
            self.current_ground.del_ground(index=cur)
            self.draw_table()
        else:
            print(f'Должна остаться хотя бы одна строка')
