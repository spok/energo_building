from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QTextEdit, QPushButton, QMessageBox, QWidget
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QSize
from construction_class.windows import *
from func import to_float, load_windows_koef, MyCombo


class Doors(QWidget):
    hor_headers = ['R,\nм²·°С/Вт', '', 'S, м²', '', 'Размеры,\nмм·мм', '', 'Количество,\nшт.', '', '']

    def __init__(self, parent=None):
        super().__init__()
        self.build = None
        self.current_doors = None
        self.vbox = QVBoxLayout()
        self.label1 = QLabel('Двери и ворота')
        self.vbox.addWidget(self.label1)
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(self.hor_headers)
        self.table.horizontalHeader().setVisible(True)
        self.table.setColumnWidth(0, 100)
        self.table.setColumnWidth(1, 10)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 10)
        self.table.setColumnWidth(4, 80)
        self.table.setColumnWidth(5, 10)
        self.table.setColumnWidth(6, 80)
        self.table.setColumnWidth(7, 20)
        self.table.setColumnWidth(8, 20)
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
        self.current_doors = self.build.constructions[index]
        self.draw_table()

    def draw_table(self):
        """Перерисовка таблицы со слоями конструкции и других элементов"""
        self.table.blockSignals(True)
        self.table.clear()
        self.table.setHorizontalHeaderLabels(self.hor_headers)
        self.current_doors.draw_table(table=self.table)
        for i in range(self.table.rowCount()):
            # добавление кнопки для добавления пустого слоя
            el_but = self.table.cellWidget(i, 7)
            el_but.clicked.connect(self.add_door)
            # добавление кнопки для удаления активного слоя
            el_but = self.table.cellWidget(i, 8)
            el_but.clicked.connect(self.delete_door)
        self.table.blockSignals(False)
        # вывод результата расчета в текстовом поле
        self.result_text.clear()
        self.result_text.setHtml(self.current_doors.get_text_result())

    def get_change(self):
        """Сохранение внесенных изменений"""
        # Сохранение изменений в таблице
        cur_row = self.table.currentRow()
        if cur_row > -1:
            current_door = self.current_doors.elements[cur_row]
            current_door.r_pr = to_float(self.table.item(cur_row, 0).text())
            current_door.area = to_float(self.table.item(cur_row, 2).text())
            current_door.set_size(self.table.item(cur_row, 4).text())
            s = self.table.item(cur_row, 6).text()
            if len(s) > 0:
                current_door.count = int(s)
            else:
                current_door.count = 0
        # Пересчет конструкций
        self.build.calc()
        # вывод результата расчета в текстовом поле
        self.result_text.clear()
        self.result_text.setText(self.current_doors.get_text_result())

    def add_door(self):
        """Добавление нового слоя"""
        self.current_doors.add_door(index=self.table.currentRow())
        self.draw_table()

    def delete_door(self):
        """Удаление активного слоя"""
        if self.table.rowCount() > 1:
            cur = self.table.currentRow()
            self.current_doors.del_door(index=cur)
            self.draw_table()
        else:
            print(f'Должна остаться хотя бы одна строка')
