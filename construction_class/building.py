from math import log
from copy import copy
from PyQt5.Qt import QStandardItem
from jinja2 import Environment, FileSystemLoader
from func import load_solar_radiation, load_orientation_coef, load_udeln, MyCombo
from construction_class.construction import *
from construction_class.windows import *
from construction_class.doors import *
from construction_class.ground import *


class Building:
    typ_constr = ['Наружная стена', 'Покрытие', 'Чердачное перекрытие', 'Перекрытие над холодным подвалом',
                  'Перекрытие над проездом', 'Окна', 'Витражи', 'Фонари', 'Двери', 'Ворота',
                  'Конструкция в контакте с грунтом']
    typ_buildings = ["Жилое", "Лечебно-профилактическое", "Детское учреждение", "Школа", "Интернат", "Гостиница",
                     "Общежитие", "Общественное", "Административное", "Сервисного обслуживания", "Бытовое",
                     "Производственное и другое с влажным или мокрым режимом эксплуатации",
                     "Производственное с сухим и нормальным режимом эксплуатации"]
    typ_regular = ['система отопления с местными терморегуляторами и пофасадным авторегулированием на вводе',
                   'система отопления с местными терморегуляторами и центральным авторегулированием на вводе',
                   'система отопления без местных терморегуляторов и пофасадным авторегулированием',
                   'система отопления с местными терморегуляторами и без авторегулирования на вводе',
                   'система отопления без местных терморегуляторов и центральным авторегулированием на вводе',
                   'система отопления без местных терморегуляторов и без авторегулирования на вводе']
    latitude_list = [37, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78]
    orientation = ['С', 'З', 'Ю', 'В', 'СЗ', 'СВ', 'ЮЗ', 'ЮВ']
    purposes = ['Ограждающая', 'Внутреняя чердака', 'Наружная чердака', 'Внутреняя подвала', 'Наружная подвала']

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
        self.tenants = 0
        self.norm = dict()

        self.citi = 'Волгоград'
        self.t_nhp = 0.0
        self.t_ot = 0.0
        self.z_ot = 0
        self.gsop = 0.0
        self.solar_citi = 'Волгоград'
        self.latitude = 48
        self.solar_energy = dict()
        self.Q_solar = 0.0
        self.k_rad = 0.0
        self.k_bit = 0.0
        self.q_bit = 0.0
        self.constructions = []
        self.k_ob = 0.0
        self.k_ob_tr = 0.0
        self.sum_nAR = 0.0
        self.solar_citi_dict = load_solar_radiation()
        self.orientation_coef = load_orientation_coef()
        self.norm_udeln = load_udeln()
        self.udeln = 0.0
        self.year = 2022
        self.regular = 'система отопления с местными терморегуляторами и центральным авторегулированием на вводе'
        self.coef_regular = 0.9
        self.v_llu = 0.0
        self.p_vent = 0.0
        self.L_vent = 0.0
        self.G_inf = 0.0
        self.n_v = 0.0
        self.n_vent = 168
        self.n_inf = 168
        self.k_vent = 0.0
        self.beta_kpi = 0.0
        self.q_ot = 0.0
        self.class_energ = ["E", "Низкий"]
        self.otklon = 0.0
        self.r_pr_norm = 0.0
        self.r_pr = 0.0
        self.q_class = 0.0

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
        elif typ == 'Конструкция в контакте с грунтом':
            con = Grounds()
        con.typ = typ
        if index < (len(self.constructions) - 1):
            self.constructions.insert(index + 1, con)
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
        elif new_typ == ['Двери', 'Ворота']:
            con = Doors()
        elif new_typ == 'Конструкция в контакте с грунтом':
            con = Grounds()
        con.typ = new_typ
        self.constructions[index] = con

    def change_purpose(self, new_typ: str, index=0):
        """Смена типа конструкции
        :param
        new_typ - новое назначение конструкции
        index - номер авктивной конструкции"""
        if new_typ in self.purposes:
            self.constructions[index].purpose = new_typ

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
                    sol[key][i] += self.solar_citi_dict[self.solar_citi][key][i] * ost / 30
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
        # расчет нормативного удельного расхода
        self.get_udeln()
        # расчет коэффициента авторегулирования тепла
        coef = [0.95, 0.9, 0.85, 0.8, 0.7, 0.6]
        self.coef_regular = coef[self.typ_regular.index(self.regular)]
        # расчет сопротивлений теплопередаче конструкций
        for con in self.constructions:
            con_typ = con.typ
            if con_typ in self.norm:
                con.r_tr = self.norm[con_typ]['Rtr']
                con.r_tr_min = self.norm[con_typ]['Rmin']
            if con_typ in ['Окна', 'Витражи', 'Фонари']:
                con.calc(self.solar_energy)
            else:
                con.calc()
        # расчет технических этажей
        ar_basement = [0.0] * 2
        ar_attic = [0.0] * 2
        for con in self.constructions:
            con_purpose = con.purpose
            con.t_ext = self.t_ot
            if con_purpose == 'Внутреняя подвала':
                try:
                    ar_basement[0] += con.area / con.r_pr
                except ZeroDivisionError:
                    pass
            elif con_purpose == 'Наружная подвала':
                try:
                    ar_basement[1] += con.area / con.r_pr
                except ZeroDivisionError:
                    pass
            elif con_purpose == 'Внутреняя чердака':
                try:
                    ar_attic[0] += con.area / con.r_pr
                except ZeroDivisionError:
                    pass
            elif con_purpose == 'Наружная чердака':
                try:
                    ar_attic[1] += con.area / con.r_pr
                except ZeroDivisionError:
                    pass
        try:
            t_basement = round((ar_basement[0] * self.t_int + ar_basement[1] * self.t_ot) / sum(ar_basement), 2)
        except ZeroDivisionError:
            t_basement = self.t_ot
        try:
            t_attic = round((ar_attic[0] * self.t_int + ar_attic[1] * self.t_ot) / sum(ar_attic), 2)
        except ZeroDivisionError:
            t_attic = self.t_ot
        # Назначение температур наружной среды для конструкций и расчет коэффициента
        self.sum_nAR = 0.0
        for con in self.constructions:
            con_purpose = con.purpose
            if con_purpose in ['Внутреняя подвала', 'Внутреняя чердака']:
                if con_purpose == 'Внутреняя подвала':
                    con.t_ext = t_basement
                elif con_purpose == 'Внутреняя чердака':
                    con.t_ext = t_attic
                con.n_coef = round((self.t_int - con.t_ext) / (self.t_int - self.t_ot), 2)
                con.r_tr = round(con.r_tr * con.n_coef, 2)
            else:
                con.t_ext = self.t_ot
                con.n_coef = 1.0
            if con_purpose in ['Внутреняя подвала', 'Внутреняя чердака', 'Ограждающая']:
                try:
                    con.nAR = con.n_coef * con.area / con.r_pr
                except ZeroDivisionError:
                    con.nAR = 0.0
                self.sum_nAR += con.nAR
        self.sum_nAR = round(self.sum_nAR, 2)

        # выбор минимального сопротивления теплопередаче
        for con in self.constructions:
            if con.purpose in ['Внутреняя подвала', 'Внутреняя чердака', 'Ограждающая']:
                if con.r_tr_min < con.r_pr < con.r_tr:
                    con.r_tr = con.r_tr_min

        # расчет приведенного сопротивления конструкций здания
        self.r_pr = 0.0
        self.r_pr_norm = 0.0
        area_ogr = 0.0
        for con in self.constructions:
            if con.purpose in ['Внутреняя подвала', 'Внутреняя чердака', 'Ограждающая']:
                try:
                    self.r_pr += con.area / con.r_pr
                    area_ogr += con.area
                except ZeroDivisionError:
                    pass
                try:
                    self.r_pr_norm += con.area / con.r_tr
                    area_ogr += con.area
                except ZeroDivisionError:
                    pass
        try:
            self.r_pr = area_ogr / self.r_pr
            self.r_pr_norm = area_ogr / self.r_pr_norm
        except ZeroDivisionError:
            self.r_pr = 0.0
            self.r_pr_norm = 0.0

        # расчет удельной теплозащитной характеристики
        try:
            self.k_ob = round(self.sum_nAR / self.v_heat, 3)
        except ZeroDivisionError:
            self.k_ob = 0.0
        if self.v_heat > 960:
            self.k_ob_tr = (0.16 + 10 / self.v_heat ** 0.5) / (0.00013 * self.gsop + 0.61)
        else:
            try:
                self.k_ob_tr = (4.74 / (0.00013 * self.gsop + 0.61)) * 1 / self.v_heat ** (1. / 3.)
            except ZeroDivisionError:
                self.k_ob_tr = 0.0
        try:
            k_ob_tr_min = 8.5 / (self.gsop ** 0.5)
        except ZeroDivisionError:
            k_ob_tr_min = 0.0
        if self.k_ob_tr < k_ob_tr_min:
            self.k_ob_tr = k_ob_tr_min
        self.k_ob_tr = round(self.k_ob_tr, 3)

        # расчет удельной характеристики теплопоступления солнечной радиации
        self.Q_solar = 0.0
        for con in self.constructions:
            if con.typ in ['Окна', 'Витражи', 'Фонари']:
                for key in con.solar_energy:
                    self.Q_solar += con.solar_energy[key]
        try:
            self.Q_solar = round(self.Q_solar, 2)
            self.k_rad = round(11.6 * self.Q_solar / (self.gsop * self.v_heat), 3)
        except ZeroDivisionError:
            self.k_rad = 0.0

        # расчет бытовых тепловыделений для жилых зданий
        if self.typ in ["Жилое", "Общежитие"]:
            try:
                a_ras = self.area_calc / self.tenants
            except ZeroDivisionError:
                a_ras = 0.0
            if a_ras < 20:
                self.q_bit = 17
            elif a_ras > 45:
                self.q_bit = 10
            else:
                self.q_bit = round(17 + 7 / 25 * (a_ras - 20), 2)
            try:
                self.k_bit = round(self.q_bit * self.area_live / (self.v_heat * (self.t_int - self.t_ot)), 3)
            except ZeroDivisionError:
                self.k_bit = 0.0
        else:
            # расчет для нежилых зданий
            try:
                self.q_bit = round(self.tenants * 90 / self.area_calc + 10, 2)
                self.k_bit = round(self.q_bit * self.area_calc / (self.v_heat * (self.t_int - self.t_ot)), 3)
            except ZeroDivisionError:
                self.q_bit = 0.0
                self.k_bit = 0.0

        # расчет вентиляционной характеристики
        self.p_vent = round(353 / (273 + self.t_ot), 2)
        self.L_vent = 0.0
        if self.typ in ["Жилое", "Общежитие"]:
            try:
                a_min = self.area_calc / self.tenants
            except ZeroDivisionError:
                a_min = 0.0
            if a_min < 20:
                self.L_vent = round(3 * self.area_live, 2)
            else:
                self.L_vent = round(0.35 * self.v_heat, 2)
                if 30 * self.tenants > self.L_vent:
                    self.L_vent = round(30 * self.tenants, 2)
        else:
            self.L_vent = self.v_llu
        self.G_inf = 0.0
        if self.typ in ["Жилое", "Общежитие"]:
            if self.floors <= 3:
                self.G_inf = round(0.3 * 0.85 * self.v_llu, 2)
            elif 4 <= self.floors <= 9:
                self.G_inf = round(0.45 * 0.85 * self.v_llu, 2)
            else:
                self.G_inf = round(0.6 * 0.85 * self.v_llu, 2)
        else:
            if self.floors <= 3:
                self.G_inf = round(0.1 * 0.85 * self.v_heat, 2)
            elif 4 <= self.floors <= 9:
                self.G_inf = round(0.15 * 0.85 * self.v_heat, 2)
            else:
                self.G_inf = round(0.2 * 0.85 * self.v_heat, 2)
        try:
            self.n_v = round(((self.L_vent * self.n_vent) / 168 + (self.G_inf * self.n_inf) / (168 * self.p_vent)) / \
                             (0.85 * self.v_heat), 3)
        except ZeroDivisionError:
            self.n_v = 0.0
        try:
            self.k_vent = round(0.28 * 1 * (self.L_vent * self.p_vent * self.n_vent + self.G_inf * self.n_inf) / \
                                (168 * self.v_heat), 3)
        except ZeroDivisionError:
            self.k_vent = 0.0
        self.beta_kpi = round(self.coef_regular / (1 + 0.5 * self.n_v), 2)

        # расчет удельного расхода
        self.q_ot = round(self.k_ob + self.k_vent - self.beta_kpi * (self.k_bit + self.k_rad), 3)

        # определение класса энергосбережения
        try:
            self.otklon = round((self.q_ot - self.udeln) / self.udeln * 100, 2)
        except ZeroDivisionError:
            self.otklon = 0.0
        if self.otklon < -60:
            self.class_energ = ["A++", "Очень высокий"]
        elif -60 <= self.otklon <= -50:
            self.class_energ = ["A+", "Очень высокий"]
        elif -50 <= self.otklon <= -40:
            self.class_energ = ["A", "Очень высокий"]
        elif -40 <= self.otklon <= -30:
            self.class_energ = ["B+", "Высокий"]
        elif -30 <= self.otklon <= -15:
            self.class_energ = ["B", "Высокий"]
        elif -15 <= self.otklon <= -5:
            self.class_energ = ["С+", "Нормальный"]
        elif -5 <= self.otklon <= 5:
            self.class_energ = ["С", "Нормальный"]
        elif 5 <= self.otklon <= 15:
            self.class_energ = ["С-", "Нормальный"]
        elif 15 < self.otklon <= 50:
            self.class_energ = ["D", "Пониженный"]
        else:
            self.class_energ = ["E", "Низкий"]

        # расчет класса энергетической эффективности
        self.calc_tenants = round(self.area_calc / 20)
        self.volume_air = self.calc_tenants * 30
        try:
            self.air_cratn = round(
                (self.volume_air * self.n_vent / 168 + (self.G_inf * self.n_inf) / (168 * self.p_vent)) / \
                (0.85 * self.v_heat), 3)
        except:
            self.air_cratn = 0
        try:
            self.k_vent2 = round(0.28 * 1 * (self.volume_air * self.p_vent * self.n_vent + self.G_inf * self.n_inf) / \
                                 (168 * self.v_heat), 3)
        except ZeroDivisionError:
            self.k_vent2 = 0.0
        try:
            self.k_bit2 = round(17 * self.area_live / (self.v_heat * (self.t_int - self.t_ot)), 3)
        except ZeroDivisionError:
            self.k_bit2 = 0.0
        self.q_ot2 = round(self.k_ob + self.k_vent2 - self.beta_kpi * (self.k_bit2 + self.k_rad), 3)
        try:
            self.q_ras = round(0.024 * self.gsop * self.q_ot2 * self.v_heat / self.area_all, 2)
        except ZeroDivisionError:
            self.q_ras = 0.0

        # расчет нормы для класса энергетической эффективности
        self.calc_class()

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
            norm = [[2.8, 3.7, 4.6, 5.5, 6.4, 7.3],
                    [2.8, 3.7, 4.6, 5.5, 6.4, 7.3],
                    [2.0, 2.7, 3.4, 4.1, 4.8, 5.5],
                    [1.4, 1.8, 2.2, 2.6, 3.0, 3.4]]
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
            rtr = r1 + (r2 - r1) / (gsop2 - gsop1) * (self.gsop - gsop1)
            rez['GSOP1'] = gsop1
            rez['GSOP2'] = gsop2
            rez['R1'] = r1
            rez['R2'] = r2
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
            rez['R_sten'] = round((rez['t_int'] - rez['t_ext']) / (rez['delta_t'] * rez['alfa_int']), 2)
            rez['Rtr'] = round(0.6 * rez['R_sten'], 2)
            rez['mp'] = 1.0
            rez['Rmin'] = round(rez['Rtr'] * rez['mp'], 2)
        return rez

    def calc_class(self):
        """Расчет параметров нормативного сопротивления теплопередаче"""
        gsop_norm = [2000, 3000, 4000, 5000, 6000, 8000, 10000]
        norm = [[67, 56, 44, 42, 40, 39],
                [100, 83, 67, 63, 60, 58],
                [133, 111, 89, 84, 80, 78],
                [167, 139, 111, 106, 100, 97],
                [200, 167, 133, 127, 120, 117],
                [253, 211, 169, 160, 152, 148],
                [317, 264, 211, 201, 190, 85]]
        # поиск индексов списка по количеству этажей
        i = 0
        while (i + 1) * 2 < self.floors:
            i += 1
        if i > 5:
            floor_after = 5
        elif i == 0:
            floor_after = 0
        else:
            floor_after = i
        floor_before = floor_after - 1

        # поиск индексов списка по значению ГСОП
        i = 0
        while gsop_norm[i] < self.gsop:
            i += 1
        if i > 6:
            gsop_after = 6
        elif i == 0:
            gsop_after = 1
        else:
            gsop_after = i
        gsop_before = gsop_after - 1

        # расчет удельного расхода по оси ГСОП
        if 2 <= self.floors <= 12:
            ud1 = norm[gsop_before][floor_before] + (norm[gsop_after][floor_before] -
                                                     norm[gsop_before][floor_before]) / \
                  (gsop_norm[gsop_after] - gsop_norm[gsop_before]) * (self.gsop - gsop_norm[gsop_before])
            ud2 = norm[gsop_before][floor_after] + (norm[gsop_after][floor_after] - norm[gsop_before][floor_after]) / \
                  (gsop_norm[gsop_after] - gsop_norm[gsop_before]) * (self.gsop - gsop_norm[gsop_before])
            self.q_class = ud1 - (ud1 - ud2) / ((floor_after + 1) * 2 -
                                                (floor_before + 1) * 2) * (self.floors - (floor_before + 1) * 2)
        else:
            self.q_class = norm[gsop_before][floor_after] + (norm[gsop_after][floor_after] -
                                                             norm[gsop_before][floor_after]) / (
                               gsop_norm[gsop_after] - gsop_norm[gsop_before]) * \
                           (self.gsop - gsop_norm[gsop_before])
        self.q_class = round(self.q_class, 2)

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
            delta_t = 0.8 * (self.t_int - self.t_ros)
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

    def get_udeln(self):
        """Определение нормативной удельной харакетристики"""
        if self.floors:
            udeln_list = self.norm_udeln[self.typ]
            if self.floors > 12:
                self.udeln = udeln_list[11]
            else:
                self.udeln = udeln_list[self.floors - 1]
            if 2023 <= self.year <= 2027:
                self.udeln = self.udeln * 0.6
            elif self.year >= 2028:
                self.udeln = self.udeln * 0.5
            else:
                self.udeln = self.udeln * 0.8
            self.udeln = round(self.udeln, 3)

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

    def get_norm_html(self, text: object):
        other_name = {'Наружная стена': 'наружной стены', 'Покрытие': 'покрытия',
                      'Чердачное перекрытие': 'чердачного перекрытия',
                      'Перекрытие над холодным подвалом': 'перекрытия над подвалом',
                      'Перекрытие над проездом': 'перекрытия над проездом', 'Окна': 'окон', 'Витражи': 'витражей',
                      'Фонари': 'фонарей', 'Двери': 'дверей', 'Ворота': 'ворот'}
        attic = dict()
        basement = dict()
        attic["has"] = False
        basement["has"] = False
        attic["elem"] = None
        basement["elem"] = None
        for key in self.norm:
            if key == 'Чердачное перекрытие':
                for elem in self.constructions:
                    if elem.purpose == 'Внутреняя чердака':
                        attic["has"] = True
                        attic["elem"] = elem
                if attic["has"]:
                    attic["plus"] = ''
                    attic["minus"] = ''
                    for elem in self.constructions:
                        if elem.purpose == 'Внутреняя чердака':
                            if len(attic["plus"]) == 0:
                                attic["plus"] += f'{elem.area}/{elem.r_pr}'
                            else:
                                attic["plus"] += f' + {elem.area}/{elem.r_pr}'
                        if elem.purpose == 'Наружная чердака':
                            if len(attic["minus"]) == 0:
                                attic["minus"] += f'{elem.area}/{elem.r_pr}'
                            else:
                                attic["minus"] += f' + {elem.area}/{elem.r_pr}'
            if key == 'Перекрытие над холодным подвалом':
                for elem in self.constructions:
                    if elem.purpose == 'Внутреняя подвала':
                        basement["has"] = True
                        basement["elem"] = elem
                if basement["has"]:
                    basement["plus"] = ''
                    basement["minus"] = ''
                    for elem in self.constructions:
                        if elem.purpose == 'Внутреняя подвала':
                            if len(basement["plus"]) == 0:
                                basement["plus"] += f'{elem.area}/{elem.r_pr}'
                            else:
                                basement["plus"] += f' + {elem.area}/{elem.r_pr}'
                        if elem.purpose == 'Наружная подвала':
                            if len(basement["minus"]) == 0:
                                basement["minus"] += f'{elem.area}/{elem.r_pr}'
                            else:
                                basement["minus"] += f' + {elem.area}/{elem.r_pr}'
        k_ob_tr_min = 0.0
        try:
            k_ob_tr_min = round(8.5 / (self.gsop ** 0.5), 2)
        except ZeroDivisionError:
            k_ob_tr_min = 0.0
        file_loader = FileSystemLoader('templates')
        env = Environment(loader=file_loader)
        tm = env.get_template('norm.html')
        msg = tm.render(norm=self, other_name=other_name, attic=attic, basement=basement, k_tr=k_ob_tr_min)
        text.setHtml(msg)

    def get_text_spec(self) -> str:
        """Генерация текстового результата расчета"""
        s = ''
        s += "Удельная теплозащитная характеристика здания равна\n"
        s += f'kоб = 1/{self.v_heat}·{self.sum_nAR} = {self.k_ob} Вт/(м³∙°С).\n'
        if self.v_heat > 960:
            s += 'Для зданий с отапливаемым объемом больше 960 м³ нормируемое значение удельной теплозащитной '
            s += 'характеристики здания определяется по формуле 5.5 СП 50.13330.2012\n'
            s += f'kобтр = (0,16 + 10/√{self.v_heat})/(0,00013 · {self.gsop} + 0,61) = {self.k_ob_tr} Вт/(м³∙°С).\n'

        else:
            s += "Для зданий с отапливаемым объемом меньше или равно 960 м³ нормируемое значение удельной "
            s += "теплозащитной характеристики здания определяется по формуле 5.5 СП 50.13330.2012.\n"
            s += f'kобтр = (4,74/(0,00013 · {self.gsop} + 0,61)·1/³√{self.v_heat} = {self.k_ob_tr} Вт/(м³∙°С).\n'
        try:
            k_ob_tr_min = round(8.5 / (self.gsop ** 0.5), 2)
        except ZeroDivisionError:
            k_ob_tr_min = 0.0
        s += 'Нормируемое значение удельной теплозащитной характеристики здания также определяемое по формуле 5.6\n'
        s += f'kобтр = 8,5/√{self.gsop} = {k_ob_tr_min} Вт/(м³∙°С).\n'
        znak = '>' if self.k_ob_tr >= k_ob_tr_min else '<'
        form = '5.5' if self.k_ob_tr >= k_ob_tr_min else '5.6'
        s += f'Так как {self.k_ob_tr} {znak} {k_ob_tr_min}, следовательно окончательное значение нормируемой удельной теплозащитной'
        s += f'характеристики принимаем рассчитанной по формуле {form}, то есть равное {self.k_ob_tr} Вт/(м³∙°С).\n'
        znak = 'больше' if self.k_ob > self.k_ob_tr else 'меньше'
        s += f'Так как расчетная удельная теплозащитная характеристика равная {self.k_ob} Вт/(м³∙°С), {znak} '
        znak = 'не' if self.k_ob > self.k_ob_tr else ''
        s += f'нормируемой величины, равной {self.k_ob_tr} Вт/(м³∙°С), то требование показателя б) пункта 5.1 '
        s += f'СП 50.133300.2012 {znak} выполняется.'
        return s

    def get_dict(self) -> dict:
        """Генерация словаря с данными
        :return - словарь"""
        data = dict()
        for key in self.__dict__:
            if key not in ['constructions', 'norm', 'solar_energy', 'solar_citi_dict',
                           'orientation_coef', 'norm_udeln', 'typ_regular']:
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
                    self.add_construction(con['typ'], con['name'], index=i)
                    self.constructions[i].data_from_dict(con)
            else:
                if key in self.__dict__.keys():
                    self.__dict__[key] = data[key]

    def draw_table(self, table: object, tree: object):
        """Перерисовка таблицы с перечнем конструкций
        :param
        table - таблица конструкций QTableWidget
        tree - список конструкции QTreeView"""
        self.calc()
        if len(self.constructions) > 0:
            table.setRowCount(len(self.constructions))
            # очистка конструкции в дереве проекта
            tree.removeRows(0, tree.rowCount())
            for i, elem in enumerate(self.constructions):
                # добавление элемента с списком конструкций
                elem_typ = MyCombo(self.typ_constr)
                elem_typ.setCurrentText(elem.typ)
                table.setCellWidget(i, 0, elem_typ)
                # добавление элемента с названием конструкции
                table.setItem(i, 1, QTableWidgetItem(elem.name))
                # добавление элемента с площадью конструкции
                table.setItem(i, 2, QTableWidgetItem(str(elem.area)))
                table.item(i, 2).setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
                # добавление элемента с сопротивлением конструкции
                el = QTableWidgetItem(str(elem.r_pr))
                table.setItem(i, 3, el)
                table.item(i, 3).setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
                # добавление элемента с назначением конструкции
                elem_typ = MyCombo(self.purposes)
                elem_typ.setCurrentText(elem.purpose)
                table.setCellWidget(i, 4, elem_typ)
                # добавление кнопки для добавления конструкции
                el_but = QPushButton()
                el_but.setToolTip('Добавить пустую конструкцию')
                el_icon = QIcon('icon/add.png')
                el_but.setIcon(el_icon)
                table.setCellWidget(i, 5, el_but)
                # добавление кнопки для копирования конструкции
                el_but = QPushButton()
                el_but.setToolTip('Сделать копию конструкции')
                el_icon = QIcon('icon/copy.png')
                el_but.setIcon(el_icon)
                table.setCellWidget(i, 6, el_but)
                # добавление кнопки для удаления конструкции
                el_but = QPushButton()
                el_but.setToolTip('Удалить конструкцию')
                el_icon = QIcon('icon/minus.png')
                el_but.setIcon(el_icon)
                table.setCellWidget(i, 7, el_but)
                # добавление элемента в дерево конструкций
                elem_nod = QStandardItem(elem.get_construction_name())
                elem_nod.setData(elem)
                tree.appendRow(elem_nod)

    def get_spec_html(self, text: object):
        """Генерация расчета удельной теплотехнической характеристики"""
        # Подготовка дополнительных данных
        constr = []
        sum_a = 0.0
        for con in self.constructions:
            if con.purpose in ['Внутреняя подвала', 'Внутреняя чердака', 'Ограждающая']:
                elem = dict()
                pr = 0.0
                sum_a += con.area
                try:
                    pr = round(con.nAR / self.sum_nAR * 100, 2)
                except ZeroDivisionError:
                    pr = 0
                elem["name"] = con.get_construction_name()
                elem["t_int"] = self.t_int
                elem["t_ext"] = round(con.t_ext, 2)
                elem["n_coef"] = round(con.n_coef, 2)
                elem["area"] = round(con.area, 2)
                elem["r_pr"] = con.r_pr
                elem["nAR"] = round(con.nAR, 2)
                elem["pr"] = pr
                constr.append(elem)
        sum_a = round(sum_a, 2)
        # Вывод в html-формате
        file_loader = FileSystemLoader('templates')
        env = Environment(loader=file_loader)
        tm = env.get_template('udeln.html')
        msg = tm.render(udeln=self, constr=constr, sum_a=sum_a)
        text.setHtml(msg)

    def get_calсulation_html(self, text: object):
        """Генерация результата расчета энергетического паспорта"""
        # Подготовка данных
        data = dict()
        try:
            data["h_floor"] = round(self.v_heat / self.area_all, 1)
        except ZeroDivisionError:
            data["h_floor"] = 0
        data["a_min"] = 0
        if self.typ in ["Жилое", "Общежитие"]:
            try:
                data["a_min"] = self.area_calc / self.tenants
            except ZeroDivisionError:
                data["a_min"] = 0.0
            try:
                data["a_ras"] = round(self.area_calc / self.tenants, 1)
            except ZeroDivisionError:
                data["a_ras"] = 0.0
        # Вывод в html-формате
        file_loader = FileSystemLoader('templates')
        env = Environment(loader=file_loader)
        tm = env.get_template('calculation.html')
        msg = tm.render(calc=self, data=data)
        text.setHtml(msg)

    def get_pasport_html(self, text: object):
        """Генерация табличного представления энергетического паспорта"""
        # Подготовка данных для вывода
        attic = dict()
        attic["has"] = False
        for elem in self.constructions:
            if elem.purpose == 'Внутреняя чердака':
                attic["has"] = True
                attic["t_ext"] = elem.t_ext
        basement = dict()
        basement["has"] = False
        for elem in self.constructions:
            if elem.purpose == 'Внутреняя подвала':
                basement["has"] = True
                basement["t_ext"] = elem.t_ext
        # Подготовка площадей конструкций
        area = dict()
        area["area_fasad"] = 0.0
        area["area_okon"] = 0.0
        area["area_vitr"] = 0.0
        area["area_fonar"] = 0.0
        area["area_door"] = 0.0
        area["area_ogr"] = 0.0
        area["area_wall"] = 0.0
        area["area_pokr"] = 0.0
        area["area_attic"] = 0.0
        area["area_warm_attic"] = 0.0
        area["area_basement"] = 0.0
        area["area_proezd"] = 0.0
        area["area_ground"] = 0.0
        for elem in self.constructions:
            if elem.typ in ['Наружная стена', 'Окна', 'Витражи', 'Фонари', 'Двери', 'Ворота']:
                area["area_fasad"] += elem.area
                if elem.typ == 'Окна':
                    area["area_okon"] += elem.area
                if elem.typ == 'Витражи':
                    area["area_vitr"] += elem.area
                if elem.typ == 'Фонари':
                    area["area_fonar"] += elem.area
                if elem.typ in ['Двери', 'Ворота']:
                    area["area_door"] += elem.area
            if elem.purpose in ['Ограждающая', 'Внутреняя подвала', 'Внутреняя чердака']:
                area["area_ogr"] += elem.area
            if elem.typ == 'Наружная стена' and elem.purpose == 'Ограждающая':
                area["area_wall"] += elem.area
            if elem.typ == 'Покрытие':
                area["area_pokr"] += elem.area
            if elem.typ == 'Чердачное перекрытие' and elem.purpose == 'Ограждающая':
                area["area_attic"] += elem.area
            if elem.typ == 'Чердачное перекрытие' and elem.purpose == 'Внутреняя чердака':
                area["area_warm_attic"] += elem.area
            if elem.typ == 'Перекрытие над холодным подвалом':
                area["area_basement"] += elem.area
            if elem.typ == 'Перекрытие над проездом':
                area["area_proezd"] += elem.area
            if elem.typ == 'Конструкция в контакте с грунтом':
                area["area_ground"] += elem.area
        try:
            area["coef_ostekl"] = round((area["area_okon"] + area["area_vitr"] + area["area_fonar"]) /
                                        area["area_fasad"], 2)
            area["compact"] = round(area["area_ogr"] / self.v_heat, 2)
        except ZeroDivisionError:
            area["coef_ostekl"] = 0
            area["compact"] = 0
        # Подготовка сопротивлений теплопередаче конструкций
        r_con = dict()
        for elem in self.constructions:
            if elem.purpose in ['Внутреняя подвала', 'Внутреняя чердака', 'Ограждающая']:
                if elem.typ in r_con:
                    r_con[elem.typ][0] += elem.area
                    try:
                        r_con[elem.typ][1] += elem.area / elem.r_tr
                    except ZeroDivisionError:
                        pass
                    try:
                        r_con[elem.typ][2] += elem.area / elem.r_pr
                    except ZeroDivisionError:
                        pass
                else:
                    r_con[elem.typ] = [0.0, 0.0, 0.0]
                    r_con[elem.typ][0] = elem.area
                    try:
                        r_con[elem.typ][1] = elem.area / elem.r_tr
                    except ZeroDivisionError:
                        pass
                    try:
                        r_con[elem.typ][2] = elem.area / elem.r_pr
                    except ZeroDivisionError:
                        pass
        for key in r_con:
            try:
                r_con[key][1] = round(r_con[key][0] / r_con[key][1], 2)
            except ZeroDivisionError:
                r_con[key][1] = 0
            try:
                r_con[key][2] = round(r_con[key][0] / r_con[key][2], 2)
            except ZeroDivisionError:
                r_con[key][2] = 0
        index = ['R<sub>o,ст</sub><sup>пр</sup>', 'R<sub>o,ок1</sub><sup>пр</sup>', 'R<sub>o,ок2</sub><sup>пр</sup>',
                 'R<sub>o,ок3</sub><sup>пр</sup>', 'R<sub>o,ок4</sub><sup>пр</sup>', 'R<sub>o,дв</sub><sup>пр</sup>',
                 'R<sub>o,дв</sub><sup>пр</sup>', 'R<sub>o,покр</sub><sup>пр</sup>', 'R<sub>o,черд</sub><sup>пр</sup>',
                 'R<sub>o,черд.т</sub><sup>пр</sup>', 'R<sub>o,цок1</sub><sup>пр</sup>',
                 'R<sub>o,цок2</sub><sup>пр</sup>', 'R<sub>o,цок3</sub><sup>пр</sup>']
        name = ['стен', 'окон', 'витражей', 'фонарей', 'окон лестнично-лифтовых узлов',
                'балконных дверей наружных переходов', 'входных дверей и ворот', 'покрытий', 'чердачных перекрытий',
                'перекрытий "теплых" чердаков',
                'перекрытий над техническими подпольями или над неотапливаемыми подвалами',
                'перекрытий над проездами или под эркерами', 'стен в земле и пола по грунту']
        try:
            h_floor = self.v_heat / self.area_all
        except ZeroDivisionError:
            h_floor = 0.0

        # Вывод в html-формате
        file_loader = FileSystemLoader('templates')
        env = Environment(loader=file_loader)
        tm = env.get_template('passport.html')
        msg = tm.render(passp=self, attic=attic, basement=basement, area=area, r_con=r_con, index=index, name=name,
                        h_floor=h_floor)
        text.setHtml(msg)

    def get_class_html(self, text: object):
        """Генерация расчета класса энергетической эффективности"""
        # Подготовка данных
        try:
            otklon = round((self.q_ras - self.q_class) / self.q_class * 100, 2)
        except ZeroDivisionError:
            otklon = 0
        if otklon < -60:
            class_energ = ["A++", "Высочайший"]
        elif -60 <= otklon <= -50:
            class_energ = ["A+", "Высочайший"]
        elif -50 <= otklon <= -40:
            class_energ = ["A", "Очень высокий"]
        elif -40 <= otklon <= -30:
            class_energ = ["B", "Высокий"]
        elif -30 <= otklon <= -15:
            class_energ = ["C", "Повышенный"]
        elif -15 <= otklon <= 0:
            class_energ = ["D", "Нормальный"]
        elif 0 <= otklon <= 25:
            class_energ = ["E", "Пониженный"]
        elif 25 <= otklon <= 50:
            class_energ = ["F", "Низкий"]
        else:
            class_energ = ["G", "Очень низкий"]

        # Вывод в html-формате
        file_loader = FileSystemLoader('templates')
        env = Environment(loader=file_loader)
        tm = env.get_template('class_energo.html')
        msg = tm.render(energo=self, cls=class_energ, otklon=otklon)
        text.setHtml(msg)
