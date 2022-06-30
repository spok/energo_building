from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QTextEdit, QPushButton, QMessageBox, QWidget
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QSize
from construction_class.windows import *
from func import to_float, load_windows_koef, MyCombo


class Windows(QWidget):
    hor_headers = ['R,\nм²·°С/Вт', '', 'S, м²', '', 'Размеры,\nмм·мм', '', 'С', 'З', 'Ю', 'В', 'СЗ', 'СВ', 'ЮЗ', 'ЮВ',
                   '', '']

    def __init__(self, parent=None):
        super().__init__()
        self.build = None
        self.current_windows = None
        self.vbox = QVBoxLayout()
        self.label1 = QLabel('Светопрозрачные конструкии')
        self.vbox.addWidget(self.label1)
        self.table_windows = QTableWidget()
        self.table_windows.setColumnCount(16)
        self.table_windows.setHorizontalHeaderLabels(self.hor_headers)
        self.table_windows.horizontalHeader().setVisible(True)
        self.table_windows.setColumnWidth(0, 70)
        self.table_windows.setColumnWidth(1, 10)
        self.table_windows.setColumnWidth(2, 100)
        self.table_windows.setColumnWidth(3, 10)
        self.table_windows.setColumnWidth(4, 70)
        self.table_windows.setColumnWidth(5, 10)
        self.table_windows.setColumnWidth(6, 20)
        self.table_windows.setColumnWidth(7, 20)
        self.table_windows.setColumnWidth(8, 20)
        self.table_windows.setColumnWidth(9, 20)
        self.table_windows.setColumnWidth(10, 20)
        self.table_windows.setColumnWidth(11, 20)
        self.table_windows.setColumnWidth(12, 20)
        self.table_windows.setColumnWidth(13, 20)
        self.table_windows.setColumnWidth(14, 20)
        self.table_windows.setColumnWidth(15, 20)
        self.vbox.addWidget(self.table_windows)
        # Настройка характеристик окон
        self.label2 = QLabel('Конструкция окон')
        self.vbox.addWidget(self.label2)
        self.windows_koef = load_windows_koef()
        self.combo_koef = MyCombo(self.windows_koef.keys())
        self.vbox.addWidget(self.combo_koef)
        # Элементы для вывода результатов
        self.label5 = QLabel('Вывод результата')
        self.vbox.addWidget(self.label5)
        self.result_text = QTextEdit()
        self.vbox.addWidget(self.result_text)
        parent.addLayout(self.vbox)
        # Установка сигналов
        self.table_windows.itemChanged.connect(self.get_change)
        self.combo_koef.activated.connect(self.get_change)

    def build_table(self, build=None, index=0):
        self.build = build
        self.current_windows = self.build.constructions[index]
        self.draw_table()

    def draw_table(self):
        """Перерисовка таблицы со слоями конструкции и других элементов"""
        self.table_windows.blockSignals(True)
        self.combo_koef.blockSignals(True)
        self.table_windows.clear()
        self.table_windows.setHorizontalHeaderLabels(self.hor_headers)
        self.current_windows.draw_table(table=self.table_windows)
        for i in range(self.table_windows.rowCount()):
            # добавление кнопки для добавления пустого слоя
            el_but = self.table_windows.cellWidget(i, 14)
            el_but.clicked.connect(self.add_window)
            # добавление кнопки для удаления активного слоя
            el_but = self.table_windows.cellWidget(i, 15)
            el_but.clicked.connect(self.delete_window)
        # вставка типа конструкции окна
        self.combo_koef.setCurrentText(self.current_windows.construction_windows)
        self.table_windows.blockSignals(False)
        self.combo_koef.blockSignals(False)
        # вывод результата расчета в текстовом поле
        self.result_text.clear()
        self.result_text.setHtml(self.current_windows.get_text_result())

    def get_change(self):
        """Сохранение внесенных изменений"""
        # Сохранение изменений в таблице
        cur_row = self.table_windows.currentRow()
        if cur_row > -1:
            current_window = self.current_windows.elements[cur_row]
            current_window.r_pr = to_float(self.table_windows.item(cur_row, 0).text())
            current_window.area = to_float(self.table_windows.item(cur_row, 2).text())
            current_window.set_size(self.table_windows.item(cur_row, 4).text())
            # сохранение количества элементов по азимутам
            for i, azimuth in enumerate(self.current_windows.orientation):
                if self.table_windows.item(cur_row, 6 + i):
                    s = self.table_windows.item(cur_row, 6 + i).text()
                    if s != '':
                        try:
                            current_window.count_orientation[azimuth] = int(s)
                        except:
                            QMessageBox.about(self, "Ошибка", f"Неверно указано количество в строке {cur_row}")
                            current_window.count_orientation[azimuth] = 0
                    else:
                        current_window.count_orientation[azimuth] = 0
        # Сохранение изменений в выпадающих списках
        self.current_windows.construction_windows =self.combo_koef.currentText()
        self.current_windows.tau_koef = self.windows_koef[self.combo_koef.currentText()][0]
        self.current_windows.g_koef = self.windows_koef[self.combo_koef.currentText()][1]
        # Пересчет конструкций
        self.build.calc()
        # вывод результата расчета в текстовом поле
        self.result_text.clear()
        self.result_text.setText(self.current_windows.get_text_result())

    def add_window(self):
        """Добавление нового слоя"""
        self.current_windows.add_window(index=self.table_windows.currentRow())
        self.draw_table()

    def delete_window(self):
        """Удаление активного слоя"""
        if self.table_windows.rowCount() > 1:
            cur = self.table_windows.currentRow()
            self.current_windows.del_window(index=cur)
            self.draw_table()
        else:
            print(f'Должна остаться хотя бы одна строка')