from math import log
from copy import copy
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QComboBox, QPushButton, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.Qt import QStandardItem
from func import get_string_index, r_unit, alfa_unit, l_unit, load_solar_radiation, load_orientation_coef
from construction_class.construction import *
from construction_class.windows import *
from construction_class.doors import *

class Building:
    typ_constr = ['Наружная стена', 'Покрытие', 'Чердачное перекрытие', 'Перекрытие над холодным подвалом',
                  'Перекрытие над проездом', 'Окна', 'Витражи', 'Фонари', 'Двери', 'Ворота',
                  'Конструкция в контакте с грунтом']
    typ_buildings = ["Жилое", "Лечебно-профилактическое", "Детское учреждение", "Школа", "Интернат", "Гостиница",
                     "Общежитие", "Общественное", "Административное", "Сервисного обслуживания", "Бытовое",
                     "Производственное и другое с влажным или мокрым режимом эксплуатации",
                     "Производственное с сухим и нормальным режимом эксплуатации"]
    latitude_list = [37, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78]
    orientation = ['С', 'З', 'Ю', 'В', 'СЗ', 'СВ', 'ЮЗ', 'ЮВ']

    def __init__(self):
        self.typ = 'Жилое'
        self.v_heat = 0.0
        self.floors = 0
        self.area_all = 0.0
        self.area_calc = 0.0
        self.area_live = 0.0
        self.height_building = 0.0
        self.t_int = 20.0
        self.t_ros = 0.0
        self.w_int = 55.0
        self.ekspl = 'А'
        self.norm = dict()

        self.citi = 'Волгоград'
        self.t_nhp = 0.0
        self.t_ot = 0.0
        self.z_ot = 0
        self.gsop = 0.0
        self.solar_citi = 'Волгоград'
        self.latitude = 48
        self.solar_energy = dict()
        self.constructions = []
        self.solar_citi_dict = load_solar_radiation('solar_radiation.xlsx')
        self.orientation_coef = load_orientation_coef('solar_radiation.xlsx')

        self.add_construction(typ='Наружная стена', name='')

    def add_construction(self, typ: str, name: str, index=0):
        """Добавление новой конструции в список"""
        if typ in ['Наружная стена', 'Покрытие', 'Чердачное перекрытие',
                   'Перекрытие над холодным подвалом', 'Перекрытие над проездом']:
            con = Construction()
            con.name = name
        elif typ in ['Окна', 'Витражи', 'Фонари']:
            con = Windows()
        elif typ in ['Двери', 'Ворота']:
            con = Doors()
        con.typ = typ
        if index < (len(self.constructions) - 1):
            self.constructions.insert(index+1, con)
        else:
            self.constructions.append(con)

    def copy_construction(self, index=0):
        """Копирование выделенной конструкции"""
        elem = copy(self.constructions[index])
        if index < (len(self.constructions) - 1):
            self.constructions.insert(index + 1, elem)
        else:
            self.constructions.append(elem)

    def del_construction(self, index=0):
        """Удаление выделенной конструкции"""
        if len(self.constructions) > 1:
            self.constructions.pop(index)

    def change_typ(self, new_typ: str, index=0):
        """Смена типа конструкции
        :param
        new_typ - новое название конструкции
        index - номер авктивной конструкции"""
        if new_typ in ['Наружная стена', 'Покрытие', 'Чердачное перекрытие',
                   'Перекрытие над холодным подвалом', 'Перекрытие над проездом']:
            con = Construction()
            con.name = ''
        elif new_typ in ['Окна', 'Витражи', 'Фонари']:
            con = Windows()
        elif new_typ in ['Двери', 'Ворота']:
            con = Doors()
        con.typ = new_typ
        self.constructions[index] = con

    def calc_solar_radiation(self):
        """Расчет солнечной радиации для каждого азимута"""
        n = self.z_ot // 60
        ost = int((self.z_ot % 60) / 2)
        self.solar_energy = dict()
        # Определение коэффициентов по широте и ориентации
        coef = dict()
        for key in self.orientation:
            coef[key] = self.orientation_coef[key][self.latitude]
        # Расчет параметров радиации на горизонтальную поверхность в отопительный период
        sol = dict()
        for key in self.solar_citi_dict[self.solar_citi]:
            sol[key] = [0] * 12
            for i in range(12):
                if i < n or i > (11 - n):
                    sol[key][i] += self.solar_citi_dict[self.solar_citi][key][i]
                elif i == n or i == (11 - n):
                    sol[key][i] += self.solar_citi_dict[self.solar_citi][key][i] * ost/30
        # Пересчет в вертикальную поверхность по азимутам
        for key in self.orientation:
            q = 0
            for i in range(12):
                q += sol['S'][i] * coef[key][i] + sol['D'][i] / 2 + sol['I'][i] * sol['A'][i] / 200
            self.solar_energy[key] = q

    def calc(self):
        # расчет температуры точки росы
        self.t_ros = round(237.7 * (17.27 * self.t_int / (237.7 + self.t_int) + log(self.w_int / 100)) /
                     (17.27 - (17.27 * self.t_int / (237.7 + self.t_int) + log(self.w_int / 100))), 1)
        # расчет значения ГСОП
        self.gsop = round((self.t_int - self.t_ot) * self.z_ot, 2)
        # Расчет солнечной радиации
        self.calc_solar_radiation()
        # расчет нормативных сопротивлений теплопередаче
        self.calc_norm()
        for con in self.constructions:
            con_typ = con.typ
            if con_typ in self.norm:
                con.r_tr = self.norm[con_typ]['Rtr']
                con.r_tr_min = self.norm[con_typ]['Rmin']
            if con_typ in ['Окна', 'Витражи', 'Фонари']:
                con.calc(self.solar_energy)
            else:
                con.calc()

    def calc_norm(self):
        """Расчет нормативных сопротивлений теплопопередаче для всех типов конструкций"""
        for elem in self.typ_constr:
            if elem != 'Конструкция в контакте с грунтом':
                self.norm[elem] = self.calc_norm_constr(elem)

    def calc_norm_constr(self, name) -> dict:
        """Расчет параметров нормативного сопротивления теплопередаче"""
        gsop_norm = [2000, 4000, 6000, 8000, 10000, 12000]
        rez = dict()
        rez['name'] = name
        norm = []
        index = -1
        if name == 'Наружная стена':
            norm = [[2.1, 2.8, 3.5, 4.2, 4.9, 5.6],
                    [2.1, 2.8, 3.5, 4.2, 4.9, 5.6],
                    [1.8, 2.4, 3.0, 3.6, 4.2, 4.8],
                    [1.4, 1.8, 2.2, 2.6, 3.0, 3.4]]
            mp = 0.63
        elif name == 'Покрытие' or name == 'Перекрытие над проездом':
            norm = [[3.2, 4.2, 5.2, 6.2, 7.2, 8.2],
                    [3.2, 4.2, 5.2, 6.2, 7.2, 8.2],
                    [2.4, 3.2, 4.0, 4.8, 5.6, 6.4],
                    [2.0, 2.5, 3.0, 3.5, 4.0, 4.5]]
            mp = 0.8
        elif name == 'Чердачное перекрытие' or name == 'Перекрытие над холодным подвалом':
            norm = [[3.2, 4.2, 5.2, 6.2, 7.2, 8.2],
                    [3.2, 4.2, 5.2, 6.2, 7.2, 8.2],
                    [2.4, 3.2, 4.0, 4.8, 5.6, 6.4],
                    [2.0, 2.5, 3.0, 3.5, 4.0, 4.5]]
            mp = 0.8
        elif name == 'Окна' or name == 'Витражи':
            norm = [[0.49, 0.63, 0.73, 0.75, 0.77, 0.8],
                    [0.3, 0.45, 0.6, 0.7, 0.75, 0.8],
                    [0.49, 0.63, 0.73, 0.75, 0.77, 0.8],
                    [0.25, 0.3, 0.35, 0.4, 0.45, 0.5]]
            mp = 1.0
        elif name == 'Фонари':
            norm = [[0.3, 0.35, 0.4, 0.45, 0.5, 0.55],
                    [0.3, 0.35, 0.4, 0.45, 0.5, 0.55],
                    [0.3, 0.35, 0.4, 0.45, 0.5, 0.55],
                    [0.2, 0.25, 0.3, 0.35, 0.4, 0.45]]
            mp = 1.0
        if self.typ in ["Жилое", "Гостиница", "Общежитие"]:
            index = 0
        elif self.typ in ["Лечебно-профилактическое", "Детское учреждение", "Школа", "Интернат"]:
            index = 1
        elif self.typ in ["Общественное", "Административное", "Сервисного обслуживания", "Бытовое"]:
            index = 2
        elif self.typ == "Производственное с сухим и нормальным режимом эксплуатации":
            index = 3
        elif self.typ == "Производственное и другое с влажным или мокрым режимом эксплуатации":
            index = 4
        # расчет требуемого сопротивления для конструкции указанного типа здания
        if -1 < index < 4 and len(norm) > 0:
            gsop1 = int(self.gsop // 2000 * 2000)
            if gsop1 == 0:
                gsop1 = 2000
            elif gsop1 >= 12000:
                gsop1 = 10000
            gsop2 = gsop1 + 2000
            r1 = norm[index][gsop_norm.index(gsop1)]
            r2 = norm[index][gsop_norm.index(gsop2)]
            rtr = r1 + (r2 - r1)/(gsop2 - gsop1)*(self.gsop - gsop1)
            rez['GSOP1'] = gsop1
            rez['GSOP2'] = gsop2
            rez['R1'] = r1
            rez['R2'] = r1
            rez['Rtr'] = round(rtr, 2)
            rez['mp'] = mp
            rez['Rmin'] = round(rez['Rtr'] * rez['mp'], 2)
            rez['delta_t'] = self.get_delta_t(name)
        elif index == 4:
            # расчет только для промзданий с влажным и мокрым режимом
            if name in ['Наружная стена', 'Покрытие', 'Чердачное перекрытие', 'Перекрытие над холодным подвалом',
                  'Перекрытие над проездом']:
                rez['delta_t'] = self.get_delta_t(name)
                rez['alfa_int'] = self.get_alfa_int(name)
                rez['t_ext'] = self.t_nhp
                rez['t_int'] = self.t_int
                rez['Rtr'] = round((rez['t_int'] - rez['t_ext']) / (rez['delta_t'] * rez['alfa_int']), 2)
                rez['mp'] = 1.0
                rez['Rmin'] = round(rez['Rtr'] * rez['mp'], 2)
            else:
                rez['Rtr'] = 0.0
                rez['mp'] = 1.0
                rez['Rmin'] = 0.0
        # расчет требуемого сопротивления теплопередаче для дверей и ворот
        if name == 'Двери' or name == 'Ворота':
            rez['delta_t'] = self.get_delta_t('Наружная стена')
            rez['alfa_int'] = 8.7
            rez['t_ext'] = self.t_nhp
            rez['t_int'] = self.t_int
            rez['R_sten'] = (rez['t_int'] - rez['t_ext']) / (rez['delta_t'] * rez['alfa_int'])
            rez['Rtr'] = round(0.6 * rez['R_sten'], 2)
            rez['mp'] = 1.0
            rez['Rmin'] = round(rez['Rtr'] * rez['mp'], 2)
        return rez

    def get_delta_t(self, name):
        """Определение нормируемого температурного перепада"""
        norm = []
        if name == 'Наружная стена':
            norm = [4.0, 4.5, 0, 0, 12]
            delta_t = self.t_int - self.t_ros
            norm[2] = delta_t
            norm[3] = delta_t
            if delta_t > 7:
                norm[2] = 7
        elif name == 'Покрытие' or name == 'Чердачное перекрытие':
            norm = [3.0, 4.0, 0, 0, 12]
            delta_t = 0.8*(self.t_int - self.t_ros)
            norm[2] = delta_t
            norm[3] = delta_t
            if delta_t > 6:
                norm[2] = 6
        elif name == 'Перекрытие над проездом' or name == 'Перекрытие над холодным подвалом':
            norm = [2.0, 2.5, 2.5, 2.5, 2.5]
        elif name == 'Фонари':
            delta_t = self.t_int - self.t_ros
            norm = [delta_t for x in range(5)]
            norm[3] = 0
        index = 0
        if self.typ in ["Жилое", "Гостиница", "Общежитие", "Лечебно-профилактическое", "Детское учреждение",
                        "Школа", "Интернат"]:
            index = 0
        elif self.typ in ["Общественное", "Административное", "Сервисного обслуживания", "Бытовое"]:
            index = 1
        elif self.typ == "Производственное с сухим и нормальным режимом эксплуатации":
            index = 2
        elif self.typ == "Производственное и другое с влажным или мокрым режимом эксплуатации":
            index = 3
        if len(norm):
            delta = norm[index]
        else:
            delta = 0
        return delta

    def get_alfa_int(self, name: str) -> float:
        """Определение коэффициента теплоотдачи для внутренней поверхности"""
        alfa = 8.7
        if name == 'Окна' or name == 'Витражи':
            alfa = 8.0
        elif name == 'Фонари':
            alfa = 9.9
        return alfa

    def get_gsop_text(self) -> str:
        s = "Градусо-сутки отопительного периода (ГСОП) определяется по формуле 5.2 СП 50.13330.2012 \n"
        s += "ГСОП = (tв - tн)*zот\n"
        s += f"где tв = {self.t_int} °С - температура внутреннего воздуха помещений здания (определяется по ГОСТ 30494-96);\n"
        s += f"tот = {self.t_ot} °С – средняя температура наружного воздуха отопительного периода "
        s += f"для г.{self.citi}, для периода со средней суточной температурой наружного воздуха не более "
        if self.typ == "Детское учреждение":
            s += f"{10} °С, определяется по табл. 1 СП 131.13330.2012; \n"
        else:
            s += f"{8} °С, определяется по табл. 1 СП 131.13330.2012; \n"
        s += f"zот = {self.z_ot} °С – продолжительность отопительного периода "
        s += f"для г.{self.citi}, для периода со средней суточной температурой наружного воздуха не более "
        if self.typ == "Детское учреждение":
            s += f"{10} °С, определяется по табл. 1 СП 131.13330.2012; \n"
        else:
            s += f"{8} °С, определяется по табл. 1 СП 131.13330.2012; \n"
        s += f"ГСОП = ({self.t_int} - {self.t_ot})*{self.z_ot} = {self.gsop} ºС·сут\n"
        return s

    def get_dict(self) -> dict:
        """Генерация словаря с данными
        :return - словарь"""
        data = dict()
        for key in self.__dict__:
            if key not in ['constructions', 'norm', 'solar_energy', 'solar_citi_dict', 'orientation_coef']:
                data[key] = self.__dict__[key]
            elif key == 'constructions':
                cons = []
                for elem in self.__dict__[key]:
                    cons.append(elem.get_dict())
                data[key] = cons
        return data

    def data_from_dict(self, data: dict):
        """Загрузка данных из словаря"""
        for key in data:
            if key == 'constructions':
                self.constructions.clear()
                for i, con in enumerate(data[key]):
                    self.add_construction(con['typ'], con['name'])
                    self.constructions[i].data_from_dict(con)
            else:
                if key in self.__dict__.keys():
                    self.__dict__[key] = data[key]

    def draw_table(self, table: object, tree: object):
        """Перерисовка таблицы с перечнем конструкций
        :param
        table - таблица конструкций QTableWidget
        tree - список конструкции QTreeView"""
        if len(self.constructions) > 0:
            table.setRowCount(len(self.constructions))
            # очистка конструкции в дереве проекта
            tree.removeRows(0, tree.rowCount())
            for i, elem in enumerate(self.constructions):
                # добавление элемента с списком конструкций
                elem_typ = QComboBox()
                elem_typ.addItems(Building.typ_constr)
                elem_typ.setCurrentText(elem.typ)
                table.setCellWidget(i, 0,  elem_typ)
                # добавление элемента с названием конструкции
                table.setItem(i, 1, QTableWidgetItem(elem.name))
                # добавление элемента с сопротивлением конструкции
                el = QTableWidgetItem(str(elem.r_pr))
                el.setTextAlignment(Qt.AlignRight)
                el.setTextAlignment(Qt.AlignVCenter)
                table.setItem(i, 2, el)
                # добавление кнопки для добавления конструкции
                el_but = QPushButton()
                el_but.setToolTip('Добавить пустую конструкцию')
                el_icon = QIcon('icon/add.png')
                el_but.setIcon(el_icon)
                table.setCellWidget(i, 3, el_but)
                # добавление кнопки для копирования конструкции
                el_but = QPushButton()
                el_but.setToolTip('Сделать копию конструкции')
                el_icon = QIcon('icon/copy.png')
                el_but.setIcon(el_icon)
                table.setCellWidget(i, 4, el_but)
                # добавление кнопки для удаления конструкции
                el_but = QPushButton()
                el_but.setToolTip('Удалить конструкцию')
                el_icon = QIcon('icon/minus.png')
                el_but.setIcon(el_icon)
                table.setCellWidget(i, 5, el_but)
                # добавление элемента в дерево конструкций
                elem_nod = QStandardItem(elem.get_construction_name())
                elem_nod.setData(elem)
                tree.appendRow(elem_nod)