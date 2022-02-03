from PyQt5.QtWidgets import QTableWidgetItem, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt
from construction_class.base import *


class GroundElement(BaseElement):
    def __init__(self):
        super().__init__()
        self.name = ''
        self.r_pr = 0.0
        self.area = []

    def get_area(self) -> float:
        """Плащадь элемента общая"""
        return sum(self.area)

    def calc_r(self):
        """Расчет сопротивления теплопередаче"""
        sum_area = self.get_area()
        sum_r = 0.0
        r = [2.1, 4.3, 8.6, 14.2]
        for i, elem in enumerate(self.area):
            try:
                sum_r += elem / r[i]
            except:
                print('Ошибка деления на ноль, для участка не указано сопротивление теплопередаче')
        try:
            self.r_pr = round(sum_area/sum_r, 2)
        except:
            print('Ошибка деления на ноль')

class Grounds(BaseConstruction):
    def __init__(self):
        super().__init__()
        self.add_ground()

    def add_ground(self, index=0):
        elem = GroundElement()
        elem.area = [0.0] * 4
        if index < (len(self.elements) - 1):
            self.elements.insert(index+1, elem)
        else:
            self.elements.append(elem)

    def del_door(self, index):
        """Удаления выбранной конструкции"""
        if len(self.elements) > 1:
            try:
                self.elements.pop(index)
            except:
                print(f'Невозможно удалить строку {index}')

    def get_sum_area(self) -> dict:
        """Расчет суммарной площади дверей"""
        sum_area = 0.0
        for elem in self.elements:
            sum_area += elem.get_area()
        return round(sum_area, 2)

    def calc(self):
        """Расчет для дверей"""
        # Расчет приведенного сопротивления теплопередаче
        sum_area = 0.0
        sum_r = 0.0
        for elem in self.elements:
            area = elem.get_area()
            elem.calc_r()
            try:
                sum_r += area / elem.r_pr
            except:
                print('Деление на ноль, для окна не указано сопротивление теплопередаче')
            sum_area += area
        try:
            self.r_pr = round(sum_area/sum_r, 2)
        except:
            print('Ошибка деления на ноль')

    def draw_table(self, table):
        """Отрисовка элементов в таблице"""
        if len(self.elements) > 0:
            table.setRowCount(len(self.elements))
            for i, elem in enumerate(self.elements):
                if type(elem) is GroundElement:
                    # добавление элемента с названием участка
                    table.setItem(i, 0, QTableWidgetItem(str(elem.name)))
                    table.item(i, 0).setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
                    # добавление элементов с площадью
                    for j in range(4):
                        el = QTableWidgetItem(str(elem.area[j]))
                        table.setItem(i, j + 1, el)
                        table.item(i, j + 1).setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
                    # добавление кнопки для добавления пустого слоя
                    el_but = QPushButton()
                    el_but.setToolTip('Добавить строку')
                    el_icon = QIcon('icon/add.png')
                    el_but.setIcon(el_icon)
                    table.setCellWidget(i, 5, el_but)
                    # добавление кнопки для удаления активного слоя
                    el_but = QPushButton()
                    el_but.setToolTip('Удалить строку')
                    el_icon = QIcon('icon/minus.png')
                    el_but.setIcon(el_icon)
                    table.setCellWidget(i, 6, el_but)

    def get_text_result(self):
        """Генерация результата расчета"""
        s = f'Суммарная площадь всех конструкций в контакте с грунтом S = {self.get_sum_area()} м².\n'
        s += f'Приведенное сопротивление теплопередаче конструкции: Rпр = {self.r_pr} м²·ºС/Вт.\n'
        s += "Конструкции в грунте не нормируются по сопротивлению теплопередаче."
        return s
