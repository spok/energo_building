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
        self.table_windows.setColumnWidth(1, 15)
        self.table_windows.setColumnWidth(2, 70)
        self.table_windows.setColumnWidth(3, 15)
        self.table_windows.setColumnWidth(4, 70)
        self.table_windows.setColumnWidth(5, 15)
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
        self.windows_koef = load_windows_koef('windows.xlsx')
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
        if len(self.current_windows.elements) > 0:
            self.table_windows.setRowCount(len(self.current_windows.elements))
            for i, elem in enumerate(self.current_windows.elements):
                if type(elem) is WindowElement:
                    # добавление элемента с сопротивлением теплопередаче
                    self.table_windows.setItem(i, 0, QTableWidgetItem(str(elem.r_pr)))
                    self.table_windows.setItem(i, 1, QTableWidgetItem('('))
                    cell_item = self.table_windows.item(i, 1)
                    if cell_item:
                        cell_item.setFlags(cell_item.flags() ^ QtCore.Qt.ItemIsEditable)
                    # добавление элемента с площадью окон
                    el = QTableWidgetItem(str(elem.area))
                    el.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                    self.table_windows.setItem(i, 2, el)
                    self.table_windows.setItem(i, 3, QTableWidgetItem('+'))
                    cell_item = self.table_windows.item(i, 3)
                    if cell_item:
                        cell_item.setFlags(cell_item.flags() ^ QtCore.Qt.ItemIsEditable)
                    # добавление элемента с размерами окна
                    el = QTableWidgetItem(elem.size)
                    el.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                    self.table_windows.setItem(i, 4, el)
                    self.table_windows.setItem(i, 5, QTableWidgetItem(')*'))
                    cell_item = self.table_windows.item(i, 5)
                    if cell_item:
                        cell_item.setFlags(cell_item.flags() ^ QtCore.Qt.ItemIsEditable)
                    # добавление количество элементов для каждой ориентации
                    for key in elem.count_orientation:
                        index = self.current_windows.orientation.index(key)
                        el = QTableWidgetItem(str(elem.count_orientation[key]))
                        el.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                        self.table_windows.setItem(i, 6 + index, el)
                    # добавление кнопки для добавления пустого слоя
                    el_but = QPushButton()
                    el_but.setToolTip('Добавить строку')
                    el_icon = QIcon('icon/add.png')
                    el_but.setIcon(el_icon)
                    el_but.clicked.connect(self.add_window)
                    self.table_windows.setCellWidget(i, 14, el_but)
                    # добавление кнопки для удаления активного слоя
                    el_but = QPushButton()
                    el_but.setToolTip('Удалить строку')
                    el_icon = QIcon('icon/minus.png')
                    el_but.setIcon(el_icon)
                    el_but.clicked.connect(self.delete_window)
                    self.table_windows.setCellWidget(i, 15, el_but)

        # вставка типа конструкции окна
        self.combo_koef.setCurrentText(self.current_windows.construction_windows)
        self.table_windows.blockSignals(False)
        self.combo_koef.blockSignals(False)

    def get_change(self):
        """Сохранение внесенных изменений"""
        # Сохранение изменений в таблице
        cur_row = self.table_windows.currentRow()
        if cur_row > -1:
            current_window = self.current_windows.elements[cur_row]
            current_window.r = to_float(self.table_windows.item(cur_row, 0).text())
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

    def add_window(self):
        """Добавление нового слоя"""
        self.current_windows.add_window()
        self.draw_table()

    def delete_window(self):
        """Удаление активного слоя"""
        if self.table_windows.rowCount() > 1:
            cur = self.table_windows.currentRow()
            self.current_windows.del_window(index=cur)
            self.draw_table()
        else:
            print(f'Должна остаться хотя бы одна строка')