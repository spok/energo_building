from PyQt5.QtWidgets import QTableWidgetItem, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt
from construction_class.base import *


class WindowElement(BaseElement):
    def __init__(self):
        super().__init__()
        self.r_pr = 0.0
        self.area = 0.0
        self.size = '0*0'
        self.size_b = 0.0
        self.size_h = 0.0
        self.count_orientation = dict()
        self.g_koef = 0.0
        self.tau_koef = 0.0
        self.i_rad = 0.0

    def set_size(self, size: str):
        """Определение размера окна из строковой переменной"""
        self.size = size
        s = []
        for razd in ['*', 'x', 'х', 'X', 'Х']:
            if razd in size:
                s = size.split(razd)
        if len(s) > 1 and len(size) > 0:
            self.size_b = float(s[0])
            self.size_h = float(s[1])

    def get_area(self) -> float:
        """Плащадь окна общая"""
        sum_area = 0.0
        if self.area > 0 and len(self.size) > 0:
            area = self.area
        else:
            area = self.size_b / 1000 * self.size_h / 1000
        for key, value in self.count_orientation.items():
            sum_area += area * value
        return sum_area

    def get_area_azimut(self) -> dict:
        """Плащадь окна отдельно по азимутам"""
        res = dict()
        if self.area > 0 and len(self.size) > 0:
            area = self.area
        else:
            area = self.size_b / 1000 * self.size_h / 1000
        for key, value in self.count_orientation.items():
            if value > 0:
                res[key] = area * value
        return res


class Windows(BaseConstruction):
    orientation = ['С', 'З', 'Ю', 'В', 'СЗ', 'СВ', 'ЮЗ', 'ЮВ']
    def __init__(self):
        super().__init__()
        self.g_koef = 0.0
        self.tau_koef = 0.0
        self.construction_windows = ''
        self.solar_energy = dict()
        self.add_window(r=0.0, area=0.0, size='0*0')

    def add_window(self, r: float = 0.0, area: float = 0.0, size: str = '0*0', index=0):
        elem = WindowElement()
        elem.r_pr = r
        elem.area = area
        elem.set_size(size)
        if index < (len(self.elements) - 1):
            self.elements.insert(index+1, elem)
        else:
            self.elements.append(elem)

    def del_window(self, index):
        """Удаления выбранной конструкции"""
        if len(self.elements) > 1:
            try:
                self.elements.pop(index)
            except:
                print(f'Невозможно удалить строку {index}')

    def get_sum_area(self) -> dict:
        """Расчет суммарной площади окон отдельно по азимутам"""
        sum_area = dict()
        for elem in self.elements:
            area = elem.get_area_azimut()
            for key in area:
                if key in sum_area:
                    sum_area[key] += area[key]
                else:
                    sum_area[key] = area[key]
        return sum_area

    def calc(self, solar_dict: dict):
        """Расчет для окон
        :param solar_dict - словарь с значениями солнечной энергии по азимутам"""
        # Расчет приведенного сопротивления теплопередаче
        sum_area = 0
        sum_r = 0
        for elem in self.elements:
            area = elem.get_area()
            try:
                sum_r += area / elem.r_pr
            except:
                print('Деление на ноль, для окна не указано сопротивление теплопередаче')
            sum_area += area
        try:
            self.r_pr = round(sum_area/sum_r, 2)
        except:
            print('Ошибка деления на ноль')
        # Расчет солнечной радиации
        if sum_area > 0:
            self.solar_energy = dict()
            area_azimut = self.get_sum_area()
            for key in area_azimut:
                if key in self.solar_energy:
                    self.solar_energy[key] += solar_dict[key] * area_azimut[key] * self.g_koef * self.tau_koef
                else:
                    self.solar_energy[key] = solar_dict[key] * area_azimut[key] * self.g_koef * self.tau_koef

    def draw_table(self, table):
        """Отрисовка элементов в таблице"""
        if len(self.elements) > 0:
            table.setRowCount(len(self.elements))
            for i, elem in enumerate(self.elements):
                if type(elem) is WindowElement:
                    # добавление элемента с сопротивлением теплопередаче
                    table.setItem(i, 0, QTableWidgetItem(str(elem.r_pr)))
                    table.item(i, 0).setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
                    table.setItem(i, 1, QTableWidgetItem('('))
                    table.item(i, 1).setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
                    table.item(i, 1).setBackground(QtGui.QColor(230, 230, 230))
                    cell_item = table.item(i, 1)
                    if cell_item:
                        cell_item.setFlags(cell_item.flags() ^ QtCore.Qt.ItemIsEditable)
                    # добавление элемента с площадью окон
                    el = QTableWidgetItem(str(elem.area))
                    table.setItem(i, 2, el)
                    table.item(i, 2).setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
                    table.setItem(i, 3, QTableWidgetItem('+'))
                    table.item(i, 3).setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
                    table.item(i, 3).setBackground(QtGui.QColor(230, 230, 230))
                    cell_item = table.item(i, 3)
                    if cell_item:
                        cell_item.setFlags(cell_item.flags() ^ QtCore.Qt.ItemIsEditable)
                    # добавление элемента с размерами окна
                    el = QTableWidgetItem(elem.size)
                    table.setItem(i, 4, el)
                    table.item(i, 4).setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
                    table.setItem(i, 5, QTableWidgetItem(')*'))
                    table.item(i, 5).setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
                    table.item(i, 5).setBackground(QtGui.QColor(230, 230, 230))
                    cell_item = table.item(i, 5)
                    if cell_item:
                        cell_item.setFlags(cell_item.flags() ^ QtCore.Qt.ItemIsEditable)
                    # добавление количество элементов для каждой ориентации
                    for key in elem.count_orientation:
                        index = self.orientation.index(key)
                        if elem.count_orientation[key] == 0:
                            s = ''
                        else:
                            s = str(elem.count_orientation[key])
                        el = QTableWidgetItem(s)
                        table.setItem(i, 6 + index, el)
                        table.item(i, 6 + index).setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
                    # добавление кнопки для добавления пустого слоя
                    el_but = QPushButton()
                    el_but.setToolTip('Добавить строку')
                    el_icon = QIcon('icon/add.png')
                    el_but.setIcon(el_icon)
                    table.setCellWidget(i, 14, el_but)
                    # добавление кнопки для удаления активного слоя
                    el_but = QPushButton()
                    el_but.setToolTip('Удалить строку')
                    el_icon = QIcon('icon/minus.png')
                    el_but.setIcon(el_icon)
                    table.setCellWidget(i, 15, el_but)

    def get_text_result(self):
        """Генерация результата расчета"""
        s = 'Площадь светопрозрачного заполнения проемов раздельно по азимутам:\n'
        area = self.get_sum_area()
        for key in area:
            if area[key] > 0:
                s += f'- азимут {key} - S = {area[key]} м²;\n'
        s += f'Приведенное сопротивление теплопередаче конструкции: Rпр = {self.r_pr}\n'
        s += "В соответствии с п. 5.1 СП 50.13330.2012 сопротивление теплопередаче конструкции должно быть не ниже "
        s += 'требуемого сопротивления теплопередаче. '
        if self.r_pr > self.r_tr:
            s_usl = ''
            s_znak = '>'
        else:
            s_usl = 'не '
            s_znak = '<'
        s += f'Так как для конструкции выполняется условие, '
        s += f'а именно {self.r_pr} м²·ºС/Вт {s_znak} {self.r_tr} м²·ºС/Вт, следовательно, требование п. 5.1 {s_usl}выполняется.'
        s += 'Количество солнечной радиации получаемой светопрозрачными конструкциями ориентирвоанными по азимутам:\n'
        for key in self.solar_energy:
            if key in area:
                s += f'- азимут {key} - S = {round(self.solar_energy[key], 2)} МДж;\n'
        return s
