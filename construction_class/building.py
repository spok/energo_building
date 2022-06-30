from math import log
from copy import copy
from PyQt5.Qt import QStandardItem
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
        self.class_energ = []
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
        # Вставка расчета ГСОП
        s = '<h2 align="center">Климатические параметры отопительного периода</h2>'
        s += "<p>Градусо-сутки отопительного периода (ГСОП) определяется по формуле 5.2 СП 50.13330.2012</p>"
        s += '<p align="center"><i>ГСОП = (t<sub>в</sub> - t<sub>от</sub>)·z<sub>от</sub></i></p>'
        s += f'<p align="justify">где <i>t<sub>в</sub></i> = {self.t_int} °С - температура внутреннего воздуха помещений здания (определяется по ГОСТ 30494-96);</p>'
        s += f'<p align="justify"><i>t<sub>от</sub></i> = {self.t_ot} °С – средняя температура наружного воздуха отопительного периода '
        s += f"для г.{self.citi}, для периода со средней суточной температурой наружного воздуха не более "
        if self.typ == "Детское учреждение":
            s += f"{10} °С, определяется по табл. 1 СП 131.13330.2012; </p>"
        else:
            s += f"{8} °С, определяется по табл. 1 СП 131.13330.2012; </p>"
        s += f'<p align="justify"><i>z<sub>от</sub></i> = {self.z_ot} °С – продолжительность отопительного периода '
        s += f"для г.{self.citi}, для периода со средней суточной температурой наружного воздуха не более "
        if self.typ == "Детское учреждение":
            s += f"{10} °С, определяется по табл. 1 СП 131.13330.2012; </p>"
        else:
            s += f"{8} °С, определяется по табл. 1 СП 131.13330.2012; </p>"
        s += f'<p align="center"><i>ГСОП</i> = ({self.t_int} - ({self.t_ot}))·{self.z_ot} = {self.gsop} ºС·сут<p>'
        s += '<p></p>'
        s += '<h2 align="center">Требования к ограждающим конструкциям здания</h2>'
        s += '<p></p>'
        text.insertHtml(s)

        # вставка расчета нормативных сопротивлений теплопередаче
        name_low = ['наружной стены', 'покрытия', 'чердачного перекрытия', 'перекрытия над подвалом',
                    'перекрытия над проездом', 'окон', 'витражей', 'фонарей', 'дверей', 'ворот']
        for key in self.norm:
            con = self.norm[key]
            name_con = name_low[self.typ_constr.index(key)]
            if key in ['Наружная стена', 'Покрытие', 'Чердачное перекрытие', 'Перекрытие над холодным подвалом',
                       'Перекрытие над проездом', 'Окна', 'Витражи', 'Фонари']:
                s = '<p></p>'
                s += f'<h3 align="center">{key}</h3>'
                s += f'<p>Для {name_con} жилых зданий в климатических условиях ' \
                     f'г. {self.citi} требуемое сопротивление теплопередаче определяется по формуле интерполяции</p>'
                s += f'<p align="center">R<sub>о</sub><sup>тр</sup> = R<sub>1</sub> + (R<sub>2</sub> - R<sub>1</sub>)' \
                     f'/(ГСОП<sub>2</sub> - ГСОП<sub>1</sub>)∙ (ГСОП - ГСОП<sub>1</sub>)</p>'
                s += f'<p align="center">R<sub>о</sub><sup>тр</sup> = {con["R1"]} + ({con["R2"]} - {con["R1"]})' \
                     f'/({con["GSOP2"]} - {con["GSOP1"]})∙ ({self.gsop} - {con["GSOP1"]}) = {con["Rtr"]} м²·°С/Вт</p>'
                s += f'<p>где ГСОП<sub>1</sub> = {con["GSOP1"]}, ГСОП<sub>2</sub> = {con["GSOP2"]} - ' \
                     f'градусо-сутки отопительного периода по таблице 3 СП 50.13330.2012, между которыми ' \
                     f'находится рассчитанная величина ГСОП;</p>'
                s += f'<p>R<sub>1</sub> = {con["R1"]} м²·°С/Вт, R<sub>2</sub> = {con["R2"]} м²·°С/Вт - ' \
                     f'нормативное сопротивление ' \
                     f'теплопередаче конструкции, , соответствующие величинам градусо-суток отопительного периода' \
                     f' {con["GSOP1"]} и {con["GSOP2"]}, для {name_con} здания по табл. 3 СП 50.13330.2012.</p>'
                s += f'<p>Таким образом, приведенное сопротивление теплопередаче {name_con} должно быть ' \
                     f'не менее {con["Rtr"]} м²·°С/Вт.</p>'
                s += f'<p>Допускается снижение нормируемого значения сопротивления теплопередаче {name_con} ' \
                     'в соответствии с пунктом 5.2 и формулой 5.1 СП 50.13330.2012</p>'
                s += f'<p align="center">R<sub>o</sub><sup>тр</sup> = R<sub>o</sub><sup>тр</sup>·m<sub>p</sub> = ' \
                     f'{con["Rtr"]}·{con["mp"]} = {con["Rmin"]} м²·°С/Вт.</p>'
                s += f'<p>Таким образом, приведенное сопротивление теплопередаче {name_con} должно быть ' \
                     f'не менее {con["Rmin"]} м²·°С/Вт.</p>'
                s += f'<p></p>'
                text.insertHtml(s)
                # вывод при наличии теплого чердака
                has_attic = False
                elem_attic = None
                if key == 'Чердачное перекрытие':
                    for elem in self.constructions:
                        if elem.purpose == 'Внутреняя чердака':
                            has_attic = True
                            elem_attic = elem
                if has_attic == True:
                    s = """<p>В соответствии с пунктом 5.2 допускается снижать нормируемое сопротивление 
                    теплопередаче чердачного перекрытия, если температура воздуха чердака отличается от температуры 
                    наружного воздуха. Так как чердак не вентилируется наружным воздухом через проемы в наружных 
                    стенах, т.е. является теплым, то температура воздуха в чердаке будет значительно выше температуры 
                    наружного воздуха.</p>"""
                    s += """<p>Снижение уровня нормируемого сопротивления теплопередаче осуществляется умножением его 
                    на коэффициент <i>n</i>.</p>"""
                    s += """<p>Так как температура внутреннего воздуха чердака, под которым располагается перекрытие, 
                    отличается от температуры внутреннего воздуха помещений здания, необходимо рассчитать коэффициент 
                    по формуле 5.3</p>"""
                    s += f'<p align="center"> n = (t<sub>в</sub><sup>*</sup> - t<sub>н</sub><sup>*</sup>) / ' \
                         f'(t<sub>в</sub> - t<sub>н</sub>) = ({self.t_int} - {elem_attic.t_ext}) / ' \
                         f'({self.t_int} - ({self.t_ot})) = {elem_attic.n_coef}</p>'
                    s += f'<p>где t<sub>в</sub><sup>*</sup> = {self.t_int} °С - температура внутреннего воздуха для ' \
                         f'помещения находящегося под перекрытием;</p>'
                    s += f'<p>t<sub>н</sub><sup>*</sup> = {elem_attic.t_ext} °С - температура наружного воздуха по ' \
                         f'отношению к перекрытию чердака, т.е. температура воздуха в чердаке, определяемая по ' \
                         f'расчету теплового баланса </p>'
                    s += f'<p>t<sub>в</sub> = {self.t_int} °С - нормативная температура внутреннего воздуха;</p>'
                    s += f'<p>t<sub>н</sub> = {self.t_ot} °С - нормативная температура наружного воздуха, ' \
                         f'принимаемая равной температуре отопительного периода.</p>'
                    s += f'<p>Температура воздуха внутри чердачного пространства t<sub>н</sub><sup>*</sup>, ' \
                         f'определяется из уравнения теплового баланса в соответствии с разделом 11.1 ' \
                         f'СП 345.1325800.2017 «Здания жилые и общественные. Правила проектирования ' \
                         f'тепловой защиты» </p>'
                    s += '<p align="center"><img src="formuls/formula_tn.jpg"></p>'
                    s += '<p>В формуле значения с индексом «+» соответствуют ограждающими конструкциям, ' \
                         'расположенным между помещением, для которого рассчитывается температура воздуха, ' \
                         'и внутренними помещениями здания, имеющими температуру tв. В формуле значения с ' \
                         'индексом «-» соответствуют ограждающими конструкциям, расположенным между помещением, ' \
                         'для которого рассчитывается температура воздуха, и наружным воздухом, ' \
                         'имеющим температуру t<sub>н</sub>. </p>'
                    s += '<p>Согласно геометрическим показателям ограждений чердака, определены сопротивления ' \
                         'теплопередаче R и площади А (площади определены по внутренней поверхности ограждающих ' \
                         'конструкций) отдельных видов ограждений отраженные в таблицах. </p>'
                    text.insertHtml(s)
                    s = """<style type="text/css">
                           TABLE {
                            border-collapse: collapse;
                           }
                           TD, TH {
                            padding: 3px;
                            border: 1px solid black;
                           }
                          </style>
                       <table border="1">
                       <caption>Таблица. Конструкции, находящиеся между чердачным пространством и 
                       внутренними помещениями</caption>
                       <tr>
                        <th>Название конструкции</th>
                        <th>A, м²</th>
                        <th>R<sub>o</sub>,м²·ºС/Вт</th>
                       </tr>"""
                    s_plus = ''
                    s_minus = ''
                    for elem in self.constructions:
                        if elem.purpose == 'Внутреняя чердака':
                            s += f"""<tr><td>{elem.get_construction_name()}</td><td>{elem.area}</td>
                            <td>{elem.r_pr}</td></tr>"""
                            if len(s_plus) == 0:
                                s_plus += f'{elem.area}/{elem.r_pr}'
                            else:
                                s_plus += f' + {elem.area}/{elem.r_pr}'
                    s += """</table>"""
                    s += """<table border="1">
                       <caption>Таблица. Конструкции, находящиеся между чердачным пространством и 
                       наружной средой</caption>
                       <tr>
                        <th>Название конструкции</th>
                        <th>A, м²</th>
                        <th>R<sub>o</sub>,м²·ºС/Вт</th>
                       </tr>"""
                    for elem in self.constructions:
                        if elem.purpose == 'Наружная чердака':
                            s += f"""<tr><td>{elem.get_construction_name()}</td><td>{elem.area}</td>
                            <td>{elem.r_pr}</td></tr>"""
                            if len(s_minus) == 0:
                                s_minus += f'{elem.area}/{elem.r_pr}'
                            else:
                                s_minus += f' + {elem.area}/{elem.r_pr}'
                    s += '</table>'
                    s += '<p>Расчет температуры воздуха чердака при расчетных температурных условиях по формуле</p>'
                    s += f'<p align="center">t<sub>н</sub><sup>*</sup> = ({self.t_int}·({s_plus}) + ({self.t_ot})· ' \
                         f'({s_minus})/({s_plus} + {s_minus}) = {elem_attic.t_ext} ºС.</p>'
                    s += f'<p>Нормируемое значение сопротивления теплопередаче перекрытия определяется в ' \
                         f'соответствие с пунктом 5.2 СП 50.13330.2012</p>'
                    s += f'<p align="center"><i>R<sub>о</sub><sup>тр</sup> = n·R<sub>о</sub><sup>тр</sup></i> = ' \
                         f'{elem_attic.n_coef}·{con["Rtr"]} = {elem_attic.r_tr} м²·ºС/Вт</p>'
                    s += f'<p>Таким образом, приведенное сопротивление теплопередаче чердачного перекрытия ' \
                         f'должно быть не менее {elem_attic.r_tr} м²·ºС/Вт. </p>'
                    s += f'<p></p>'
                    text.insertHtml(s)

                has_basement = False
                elem_basement = None
                if key == 'Перекрытие над холодным подвалом':
                    for elem in self.constructions:
                        if elem.purpose == 'Внутреняя подвала':
                            has_basement = True
                            elem_basement = elem
                if has_basement == True:
                    s = """<p>В соответствии с пунктом 5.2 допускается снижать нормируемое сопротивление 
                    теплопередаче перекрытия подвала, если температура воздуха подвала отличается от температуры 
                    наружного воздуха. Так как подвал не вентилируется наружным воздухом через проемы в наружных 
                    стенах, т.е. является теплым, то температура воздуха в подвале будет значительно выше температуры 
                    наружного воздуха.</p>"""
                    s += """<p>Снижение уровня нормируемого сопротивления теплопередаче осуществляется умножением его 
                    на коэффициент <i>n</i>.</p>"""
                    s += """<p>Так как температура внутреннего воздуха подвала, над которым располагается перекрытие, 
                    отличается от температуры внутреннего воздуха помещений здания, необходимо рассчитать коэффициент 
                    по формуле 5.3</p>"""
                    s += f'<p align="center"> n = (t<sub>в</sub><sup>*</sup> - t<sub>н</sub><sup>*</sup>) / ' \
                         f'(t<sub>в</sub> - t<sub>н</sub>) = ({self.t_int} - {elem_basement.t_ext}) / ' \
                         f'({self.t_int} - ({self.t_ot})) = {elem_basement.n_coef}</p>'
                    s += f'<p>где t<sub>в</sub><sup>*</sup> = {self.t_int} °С - температура внутреннего воздуха для ' \
                         f'помещения находящегося над перекрытием;</p>'
                    s += f'<p>t<sub>н</sub><sup>*</sup> = {elem_basement.t_ext} °С - температура наружного воздуха по ' \
                         f'отношению к перекрытию подвала, т.е. температура воздуха в подвале, определяемая по ' \
                         f'расчету теплового баланса </p>'
                    s += f'<p>t<sub>в</sub> = {self.t_int} °С - нормативная температура внутреннего воздуха;</p>'
                    s += f'<p>t<sub>н</sub> = {self.t_ot} °С - нормативная температура наружного воздуха, ' \
                         f'принимаемая равной температуре отопительного периода.</p>'
                    s += f'<p>Температура воздуха внутри подвального пространства t<sub>н</sub><sup>*</sup>, ' \
                         f'определяется из уравнения теплового баланса в соответствии с разделом 11.1 ' \
                         f'СП 345.1325800.2017 «Здания жилые и общественные. Правила проектирования ' \
                         f'тепловой защиты» </p>'
                    s += '<p align="center"><img src="formuls/formula_tn.jpg"></p>'
                    s += '<p>В формуле значения с индексом «+» соответствуют ограждающими конструкциям, ' \
                         'расположенным между помещением, для которого рассчитывается температура воздуха, ' \
                         'и внутренними помещениями здания, имеющими температуру t<sub>в</sub>. В формуле значения с ' \
                         'индексом «-» соответствуют ограждающими конструкциям, расположенным между помещением, ' \
                         'для которого рассчитывается температура воздуха, и наружным воздухом, ' \
                         'имеющим температуру t<sub>н</sub>. </p>'
                    s += '<p>Согласно геометрическим показателям ограждений подвала, определены сопротивления ' \
                         'теплопередаче R и площади А (площади определены по внутренней поверхности ограждающих ' \
                         'конструкций) отдельных видов ограждений отраженные в таблицах. </p>'
                    text.insertHtml(s)
                    s = """<style type="text/css">
                           TABLE {
                            border-collapse: collapse;
                           }
                           TD, TH {
                            padding: 3px;
                            border: 1px solid black;
                           }
                          </style>
                       <table border="1">
                       <caption>Таблица. Конструкции, находящиеся между подвалом и 
                       внутренними помещениями</caption>
                       <tr>
                        <th>Название конструкции</th>
                        <th>A, м²</th>
                        <th>R<sub>o</sub>,м²·ºС/Вт</th>
                       </tr>"""
                    s_plus = ''
                    s_minus = ''
                    for elem in self.constructions:
                        if elem.purpose == 'Внутреняя подвала':
                            s += f"""<tr><td>{elem.get_construction_name()}</td><td>{elem.area}</td>
                            <td>{elem.r_pr}</td></tr>"""
                            if len(s_plus) == 0:
                                s_plus += f'{elem.area}/{elem.r_pr}'
                            else:
                                s_plus += f' + {elem.area}/{elem.r_pr}'
                    s += """</table>"""
                    s += """<table border="1">
                       <caption>Таблица. Конструкции, находящиеся между подвалом и 
                       наружной средой</caption>
                       <tr>
                        <th>Название конструкции</th>
                        <th>A, м²</th>
                        <th>R<sub>o</sub>,м²·ºС/Вт</th>
                       </tr>"""
                    for elem in self.constructions:
                        if elem.purpose == 'Наружная подвала':
                            s += f"""<tr><td>{elem.get_construction_name()}</td><td>{elem.area}</td>
                            <td>{elem.r_pr}</td></tr>"""
                            if len(s_minus) == 0:
                                s_minus += f'{elem.area}/{elem.r_pr}'
                            else:
                                s_minus += f' + {elem.area}/{elem.r_pr}'
                    s += '</table>'
                    s += '<p>Расчет температуры воздуха подвала при расчетных температурных условиях по формуле</p>'
                    s += f'<p align="center">t<sub>н</sub><sup>*</sup> = ({self.t_int}·({s_plus}) + ({self.t_ot})· ' \
                         f'({s_minus})/({s_plus} + {s_minus}) = {elem_basement.t_ext} ºС.</p>'
                    s += f'<p>Нормируемое значение сопротивления теплопередаче перекрытия определяется в ' \
                         f'соответствие с пунктом 5.2 СП 50.13330.2012</p>'
                    s += f'<p align="center"><i>R<sub>о</sub><sup>тр</sup> = n·R<sub>о</sub><sup>тр</sup></i> = ' \
                         f'{elem_basement.n_coef}·{con["Rtr"]} = {elem_basement.r_tr} м²·ºС/Вт</p>'
                    s += f'<p>Таким образом, приведенное сопротивление теплопередаче перекрытия подвала ' \
                         f'должно быть не менее {elem_basement.r_tr} м²·ºС/Вт. </p>'
                    s += f'<p></p>'
                    text.insertHtml(s)

            if key in ['Двери', 'Ворота']:
                s = f'<h3 align="center">{key}</h3>'
                s += f'<p>Нормируемое сопротивление {name_con} определяется в соответствии с пунктом 5.2 по формуле</p>'
                s += f'<p align="center">R<sub>o</sub><sup>норм</sup> = 0,6·R<sub>o</sub><sup>норм</sup> = ' \
                     f'0,6·{con["R_sten"]} = {con["Rtr"]} м²·°С/Вт.</p>'
                s += f'<p>где R<sub>o</sub><sup>норм</sup> = {con["R_sten"]} м²·°С/Вт - нормируемое сопротивление ' \
                     'теплопередачи определенное по формуле 5.4 СП 50.13330.2012</p>'
                s += f'<p align="center">R<sub>o</sub><sup>норм</sup> = (t<sub>в</sub> - t<sub>н</sub>)/' \
                     f'(Δt<sup>н</sup>·α<sub>в</sub>)) = ({self.t_int} - ({self.t_nhp}))/ ({con["delta_t"]}' \
                     f'·{con["alfa_int"]}) = {con["R_sten"]} м²·°С/Вт,</p>'
                s += f'<p>где t<sub>в</sub> = {self.t_int} °С - температура внутреннего воздуха;</p>'
                s += f'<p>t<sub>н</sub> = {self.t_nhp} °С - температура наружного воздуха при наиболее холодной ' \
                     'пятидневки обеспеченностью 0,92 по СП 131.13330.2012;</p>'
                s += '<p></p>'
                text.insertHtml(s)

        # Вставка расчета нормативной удельной теплозащитной характеристики
        s = '<p></p>'
        s += '<h2 align="center">Нормативная удельная теплозащитная характеристика</h2>'
        s += '<p></p>'
        if self.v_heat > 960:
            s += '<p>Для зданий с отапливаемым объемом больше 960 м³ нормируемое значение удельной теплозащитной '
            s += 'характеристики здания определяется по формуле 5.5 СП 50.13330.2012</p>'
            s += '<p align="center">k<sub>об</sub><sup>тр</sup> = (0,16 + 10/√V<sub>от</sub>)/(0,00013·ГСОП + 0,61)</p>'
            s += f'<p align="center">k<sub>об</sub><sup>тр</sup> = (0,16 + 10/√{self.v_heat})/(0,00013 · {self.gsop} ' \
                 f'+ 0,61) = {self.k_ob_tr} Вт/(м³∙°С).</p>'

        else:
            s += "<p>Для зданий с отапливаемым объемом меньше или равно 960 м³ нормируемое значение удельной "
            s += "теплозащитной характеристики здания определяется по формуле 5.5 СП 50.13330.2012.</p>"
            s += '<p align="center">k<sub>об</sub><sup>тр</sup> = (4,74/(0,00013·ГСОП + 0,61)·1/³√V<sub>от</sub></p>'
            s += f'<p align="center">k<sub>об</sub><sup>тр</sup> = (4,74/(0,00013 · {self.gsop} + ' \
                 f'0,61)·1/³√{self.v_heat} = {self.k_ob_tr} Вт/(м³∙°С).</p>'
        try:
            k_ob_tr_min = round(8.5 / (self.gsop ** 0.5), 2)
        except ZeroDivisionError:
            k_ob_tr_min = 0.0
        s += '<p>Нормируемое значение удельной теплозащитной характеристики здания также определяемое по формуле 5.6</p>'
        s += f'<p align="center">k<sub>об</sub><sup>тр</sup> = 8,5/√ГСОП = 8,5/√{self.gsop} = {k_ob_tr_min} ' \
             f'Вт/(м³∙°С).</p>'
        znak = '>' if self.k_ob_tr >= k_ob_tr_min else '<'
        form = '5.5' if self.k_ob_tr >= k_ob_tr_min else '5.6'
        s += f'<p>Так как {self.k_ob_tr} {znak} {k_ob_tr_min}, следовательно окончательное значение нормируемой ' \
             f'удельной теплозащитной'
        s += f'характеристики принимаем рассчитанной по формуле {form}, то есть равное {self.k_ob_tr} Вт/(м³∙°С).</p>'
        text.insertHtml(s)

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

    def get_text_spec_html(self, text: object):
        """Генерация текстового результата расчета"""
        s = """<style type="text/css">
           TABLE {
            border-collapse: collapse; /* Убираем двойные линии между ячейками */
           }
           TD, TH {
            padding: 3px; /* Поля вокруг содержимого таблицы */
            border: 1px solid black; /* Параметры рамки */
           }
          </style>"""
        s += f"""<h3>Удельная теплозащитная характеристика здания</h3>
        <p>Расчет удельной теплозащитной характеристики здания производится в соответствии с приложением Ж СП 50.133300.2012 [1] по формуле Ж.1 [1]</p>
        <p align="center"><img src="formuls/formula_k_ob.jpg"></p>
        <p>где V<sub>от</sub> = {self.v_heat} м³ – отапливаемый объем здания;</p>
        <p>А<sub>ф,i</sub> – площадь соответствующего фрагмента теплозащитной оболочки здания;</p>
        <p>R<sub>о,j</sub><sup>пр</sup> – приведенное сопротивление теплопередачи фрагмента теплозащитной оболочки здания;</p>
        <p>n<sub>i,j</sub> – коэффициент, учитывающий отличие внутренней или наружной температуры у конструкции от 
        принятых в расчете ГСОП, определяется по формуле 5.3 [1];</p>
        <p align="center"><img src="formuls/formula_n.jpg"></p>
        <p>t<sub>в</sub>, t<sub>от</sub> – температура внутреннего воздуха и температура наружного воздуха отопительного периода;</p>
        <p>t<sub>в</sub><sup>*</sup>, t<sub>от</sub><sup>*</sup> - средняя температура внутреннего и наружного воздуха помещения.</p>

        <table border="1">
           <caption>Таблица. Характеристики ограждающих конструкций здания</caption>
           <tr>
            <th>Название конструкции</th>
            <th>t<sub>в</sub>, °С</th>
            <th>t<sub>н</sub>, °С</th>
            <th>n</th>
            <th>A, м²</th>
            <th>R<sub>o</sub>,м²·ºС/Вт</th>
            <th>n·A/R<sub>o</sub></th>
            <th>%</th>
           </tr>"""
        sum_a = 0.0
        for con in self.constructions:
            if con.purpose in ['Внутреняя подвала', 'Внутреняя чердака', 'Ограждающая']:
                pr = 0.0
                sum_a += con.area
                try:
                    pr = round(con.nAR / self.sum_nAR * 100, 2)
                except ZeroDivisionError:
                    pr = 0
                s += f"""<tr><td>{con.get_construction_name()}</td><td>{self.t_int}</td><td>{round(con.t_ext, 2)}</td>
                <td>{round(con.n_coef, 2)}</td><td>{round(con.area, 2)}</td><td>{con.r_pr}</td>
                <td>{round(con.nAR, 2)}</td><td>{pr}</td></tr>"""
        s += f"""<tr><td><b>Итого:</td><td></td><td></td><td></td><td><b>{round(sum_a, 2)}</td><td></td>
                        <td><b>{self.sum_nAR}</td><td><b>100</td></tr>"""
        s += """</table>"""
        s += """<p>Удельная теплозащитная характеристика здания равна</p>"""
        s += f'<p align="center">k<sub>об</sub> = 1/{self.v_heat}·{self.sum_nAR} = {self.k_ob} Вт/(м³∙°С).</p>'
        znak = 'больше' if self.k_ob > self.k_ob_tr else 'меньше'
        s += f'<p>Так как расчетная удельная теплозащитная характеристика равная {self.k_ob} Вт/(м³∙°С), {znak} '
        znak = 'не' if self.k_ob > self.k_ob_tr else ''
        s += f'нормируемой величины, равной {self.k_ob_tr} Вт/(м³∙°С), то требование показателя б) пункта 5.1 '
        s += f'СП 50.133300.2012 {znak} <b>выполняется</b>.</p>'
        text.insertHtml(s)

    def get_text_calulation_html(self, text: object):
        """Генерация текстового результата расчета удельного расхода"""
        s = '<h2 align="center">Расчет удельной характеристики расхода тепловой энергии на отопление и вентиляцию</h2>'
        s += "<p>Расчетная удельная характеристика расхода тепловой энергии на отопление и вентиляцию здания " \
             "определяется по формуле Г.1 СП 50.13330.2012</p>"
        s += '<p align="center"><i>q<sub>от</sub><sup>р</sup> = k<sub>об</sub> + k<sub>вент</sub> - β<sub>КПИ</sub>' \
             '(k<sub>быт</sub> + k<sub>рад</sub>)</i></p>'
        s += f'<p align="center">q<sub>от</sub><sup>р</sup> = {self.k_ob} + {self.k_vent} - {self.beta_kpi}' \
             f'({self.k_bit} + {self.k_rad}) = {self.q_ot} Вт/(м³∙°С)</p>'
        s += f"<p>где <i>k<sub>об</sub></i> = {self.k_ob} Вт/(м³∙°С) - удельная теплозащитная характеристика здания, " \
             f"определяется в соответствии с приложением Ж СП 50.13330.2012;</p>"
        s += f"<p><i>k<sub>вент</sub></i> = {self.k_vent} Вт/(м³∙°С) - удельная вентиляционная характеристика " \
             f"здания, определяемая в соответствии с пунктом Г.2 приложения Г СП 50.13330.2012;</p>"
        s += f"<p><i>k<sub>быт</sub></i> = {self.k_bit} Вт/(м³∙°С) - удельная характеристика бытовых " \
             f"тепловыделений здания, определяемая в соответствии с пунктом Г.5 приложения Г СП 50.13330.2012;</p>"
        s += f"<p><i>k<sub>рад</sub></i> = {self.k_rad} Вт/(м³∙°С) - удельная характеристика теплопоступлений в здание " \
             f"от солнечной радиации, определяемая в соответствии с пунктом Г.6 приложения Г СП 50.13330.2012.</p>"
        s += f"<p><i>β<sub>КПИ</sub></i> = {self.beta_kpi} - коэффициент полезного использования теплопоступлений, " \
             f"определяемый по формуле Г.1а приложения Г СП 50.13330.2012</p>"
        s += f'<p align="center"><i>β<sub>КПИ</sub> = К<sub>рег</sub>/(1 + 0,5∙n<sub>в</sub>)</i> = ' \
             f'{self.coef_regular}/(1 + 0,5∙{self.n_v}) = {self.beta_kpi}</p>'
        s += f"<p>здесь <i>К<sub>рег</sub></i> = {self.coef_regular} - коэффициент эффективности регулирования " \
             f"подачи теплоты в системах отопления ({self.regular}), определяемое по пункту Г.1 приложения " \
             f"Г СП 50.13330.2012;</p>"
        s += f"<p><i>n<sub>в</sub></i> = {self.n_v} ч<sup>-1</sup> - средняя кратность воздухообмена здания за " \
             f"отопительный период, определяемая по формуле Г.4 приложения Г СП 50.13330.2012</p>"
        s += f'<p align="center"><i>n<sub>в</sub> = [(L<sub>вент</sub>∙n<sub>вент</sub>)/168 + ' \
             f'(G<sub>инф</sub>∙n<sub>инф</sub>)/(168∙ρ<sub>в</sub><sup>вент</sup>)]/' \
             f'(β<sub>v</sub>∙V<sub>от</sub>)</i></p>'
        s += f'<p align="center"><i>n<sub>в</sub></i> = [({self.L_vent} ∙ {self.n_vent})/168 + ({self.G_inf} ∙ ' \
             f'{self.n_inf})/(168 ∙ {self.p_vent})]/(0,85 ∙ {self.v_heat}) = {self.n_v} ч<sup>-1</sup></p>'
        try:
            h_floor = round(self.v_heat / self.area_all, 1)
        except ZeroDivisionError:
            h_floor = 0
        if self.typ in ["Жилое", "Общежитие"]:
            try:
                a_min = self.area_calc / self.tenants
            except ZeroDivisionError:
                a_min = 0.0
            if a_min < 20:
                s += f"<p>где <i>L<sub>вент</sub></i> = 3∙А<sub>ж</sub> = 3∙{self.area_live} = {self.L_vent} м³/ч - " \
                     f"количество приточного воздуха в здание при неорганизованном притоке и расчетной заселенностью " \
                     f"менее 20 м² общей площади на человека, определяемая по пункту Г.3 приложения Г СП 50.13330.2012;</p>"
            else:
                if 30 * self.tenants > self.L_vent:
                    s += f"<p>где <i>L<sub>вент</sub></i> = 30∙m = 3∙{self.tenants} = {self.L_vent} м³/ч - " \
                         f"количество приточного воздуха в здание при неорганизованном притоке и расчетной заселенностью " \
                         f"более 20 м² общей площади на человека, определяемая по пункту Г.3 приложения Г СП 50.13330.2012;</p>"
                    s += f"<p><i>m</i> = {self.tenants} чел - количество жителей;</p>"
                else:
                    s += f"<p>где <i>L<sub>вент</sub></i> = 0,35∙h<sub>эт</sub>∙А<sub>об</sub> = " \
                         f"0,35∙{h_floor}∙{self.area_calc} = {self.L_vent} м³/ч - количество приточного воздуха " \
                         f"в здание при неорганизованном притоке и расчетной заселенностью более 20 м² общей площади " \
                         f"на человека, определяемая по пункту Г.3 приложения Г СП 50.13330.2012;</p>"
                    s += f"<p><i>А<sub>об</sub></i> = {self.area_calc} м² - общая площадь квартир;</p>"
        else:
            s += f"<p>где <i>L<sub>вент</sub></i> = {self.L_vent} м³/ч - " \
                 f"количество приточного воздуха в здание при работе механической вентиляции;</p>"
        s += f"<p><i>n<sub>вент</sub></i> = 168 ч - число часов работы вентиляции в течение недели;</p>"
        s += f"<p><i>n<sub>инф</sub></i> = 168 ч - число часов инфильтрации в течение недели;</p>"
        s += f"<p><i>β<sub>v</sub></i> = 0,85 - коэффициент снижения объема воздуха в здании, " \
             f"учитывающий наличие внутренних ограждающих конструкций;</p>"
        s += f"<p><i>V<sub>от</sub></i> = {self.v_heat} м³ - отапливаемый объем здания;</p>"
        s += f"<p><i>G<sub>инф</sub></i> = {self.G_inf} кг/ч - количество инфильтрующегося воздуха в здание " \
             f"через ограждающие конструкции, определяемое согласно Г.4 СП 50.13330.2012;</p>"
        if self.typ in ["Жилое", "Общежитие"]:
            if self.floors <= 3:
                s += f'<p align="center"><i>G<sub>инф</sub> = 0,3 ∙ 0,85 ∙ V<sub>ЛЛУ</sub></i> = 0,3 ∙ 0,85 ∙' \
                     f' {self.v_llu} = {self.G_inf} кг/ч</p>'
            elif 4 <= self.floors <= 9:
                s += f'<p align="center"><i>G<sub>инф</sub> = 0,45 ∙ 0,85 ∙ V<sub>ЛЛУ</sub></i> = 0,3 ∙ 0,85 ∙' \
                     f' {self.v_llu} = {self.G_inf} кг/ч</p>'
            else:
                s += f'<p align="center"><i>G<sub>инф</sub> = 0,6 ∙ 0,85 ∙ V<sub>ЛЛУ</sub></i> = 0,3 ∙ 0,85 ∙' \
                     f' {self.v_llu} = {self.G_inf} кг/ч</p>'
        else:
            if self.floors <= 3:
                s += f'<p align="center"><i>G<sub>инф</sub> = 0,1 ∙ 0,85 ∙ V<sub>от</sub></i> = 0,3 ∙ 0,85 ∙' \
                     f' {self.v_heat} = {self.G_inf} кг/ч</p>'
            elif 4 <= self.floors <= 9:
                s += f'<p align="center"><i>G<sub>инф</sub> = 0,15 ∙ 0,85 ∙ V<sub>от</sub></i> = 0,3 ∙ 0,85 ∙' \
                     f' {self.v_heat} = {self.G_inf} кг/ч</p>'
            else:
                s += f'<p align="center"><i>G<sub>инф</sub> = 0,2 ∙ 0,85 ∙ V<sub>от</sub></i> = 0,3 ∙ 0,85 ∙' \
                     f' {self.v_heat} = {self.G_inf} кг/ч</p>'
        s += f"<p><i>ρ<sub>в</sub><sup>вент</sup></i> = {self.p_vent} кг/м³ - средняя плотность приточного воздуха " \
             f"за отопительный период определяемая по формуле Г.3 приложения Г СП 50.13330.2012</p>"
        s += f'<p align="center"><i>ρ<sub>в</sub><sup>вент</sup> = 353/[273 + t<sub>от</sub>] = ' \
             f'353/[273 + {self.t_ot}] = {self.p_vent} кг/м³</p>'
        # удельная вентиляционная характеристика
        s += "<p>Удельная вентиляционная характеристика здания определяется по формуле Г.2 приложения " \
             "Г СП 50.13330.2012</p>"
        s += '<p align="center"><i>k<sub>вент</sub> = 0,28с(L<sub>вент</sub>∙ρ<sub>в</sub><sup>вент</sup>∙' \
             f'n<sub>вент</sub>∙(1-k<sub>эф</sub>) + G<sub>инф</sub>∙n<sub>инф</sub>)/(168∙V<sub>от</sub>)</i></p>'
        s += f'<p align="center"><i>k<sub>вент</sub></i> = 0,28∙1({self.L_vent}∙{self.p_vent}∙{self.n_vent}(1 - 0) + ' \
             f'{self.G_inf}∙{self.n_inf})/(168∙{self.v_heat}) = {self.k_vent} Вт/(м³∙°С)</p>'
        s += "<p>где с - удельная теплоемкость воздуха, равная 1 кДж/(кг·°С)</p>"
        # удельная бытовая характеристика
        if self.typ in ["Жилое", "Общежитие"]:
            s += "<p>Удельная характеристика бытовых тепловыделений жилого здания определяется по формуле Г.6 " \
                 "приложения Г СП 50.13330.2012</p>"
            s += '<p align="center"><i>k<sub>быт</sub> = (q<sub>быт</sub>∙А<sub>ж</sub>)/[V<sub>от</sub>' \
                 '(t<sub>в</sub> - t<sub>от</sub>)]</i></p>'
            s += f'<p align="center"><i>k<sub>быт</sub></i> = ({self.q_bit}∙{self.area_live})/[{self.v_heat}' \
                 f'({self.t_int} - ({self.t_ot}))] = {self.k_bit} Вт/(м³∙°С)</p>'
            s += f"<p>где q<sub>быт</sub> = {self.q_bit} - величина бытовых тепловыделений на 1 м² площади " \
                 f"жилых помещений c расчетной заселенностью "
            try:
                a_ras = round(self.area_calc / self.tenants, 1)
            except ZeroDivisionError:
                a_ras = 0.0
            s += f'{a_ras} м² на человека.</p>'
            s += f"<p>где <i>V<sub>от</sub></i> = {self.v_heat} м³ - отапливаемый объем здания;</p>"
            s += f"<p><i>А<sub>ж</sub></i> = {self.area_live} м² - жилая площадь квартир;</p>"
            s += f"<p><i>t<sub>в</sub></i> = {self.t_int} °С - температура внутреннего воздуха;</p>"
            s += f"<p><i>t<sub>от</sub></i> = {self.t_ot} °С - средняя температура наружного воздуха в " \
                 f"отопительный период;</p>"
        else:
            # расчет для нежилых зданий
            s += "<p>Удельная характеристика бытовых тепловыделений нежилого здания определяется по формуле Г.6а " \
                 "приложения Г СП 50.13330.2012</p>"
            s += '<p align="center"><i>k<sub>быт</sub> = (q<sub>быт</sub>∙А<sub>р</sub>)/[V<sub>от</sub>' \
                 '(t<sub>в</sub> - t<sub>от</sub>)]</i></p>'
            s += f'<p align="center"><i>k<sub>быт</sub></i> = ({self.q_bit}∙{self.area_calc})/[{self.v_heat}' \
                 f'({self.t_int} - ({self.t_ot}))] = {self.k_bit} Вт/(м³∙°С)</p>'
            s += f"<p>где <i>А<sub>р</sub></i> = {self.area_calc} м² - расчетная площадь здания;</p>"

        # удельная радиационная характеристика
        s += "<p>Удельная характеристика теплопоступлений в здание от солнечной радиации определяется по формуле Г.7 " \
             "приложения Г СП 50.13330.2012</p>"
        s += '<p align="center"><i>k<sub>рад</sub> = (11,6∙Q<sub>рад</sub><sup>год</sup>)/(V<sub>от</sub>∙ГСОП)</i></p>'
        s += f'<p align="center"><i>k<sub>рад</sub></i> = (11,6∙{self.Q_solar})/[{self.v_heat} ∙ {self.gsop}) =' \
             f' {self.k_rad} Вт/(м³∙°С)</p>'
        s += f"<p>где <i>Q<sub>рад</sub><sup>год</sup></i> = {self.Q_solar} МДж/год - теплопоступления через окна и " \
             f"фонари от солнечной радиации в течение отопительного периода для четырех фасадов зданий, " \
             f"ориентированных по четырем направлениям определяемые по методике раздела 10 СП 345.1325800.2017;</p>"

        # удельный расход тепловой энергии
        s += "<p>Удельный расход тепловой энергии на отопление и вентиляцию здания за отопительный период " \
             "определяется по формуле Г.9 и Г.9а приложения Г СП 50.13330.2012</p>"
        s += f'<p align="center"><i>q = 0,024∙ГСОП∙q<sub>от</sub><sup>р</sup></i> = 0,024∙{self.gsop}∙{self.q_ot} = ' \
             f'{round(0.024 * self.gsop * self.q_ot, 2)} кВт·ч/(м³·год).</p>'
        s += f'<p align="center"><i>q = 0,024∙ГСОП∙q<sub>от</sub><sup>р</sup>∙h</i> = 0,024∙{self.gsop}∙{self.q_ot}∙' \
             f'{h_floor} = {round(0.024 * self.gsop * self.q_ot * h_floor, 2)} кВт·ч/(м²·год).</p>'
        s += f"<p>где <i>h</i> = {h_floor} м - средняя высота этажа здания;</p>"
        s += "<p>Расход тепловой энергии на отопление и вентиляцию здания за отопительный период " \
             "определяется по формуле Г.10 приложения Г СП 50.13330.2012</p>"
        s += f'<p align="center"><i>Q<sub>от</sub><sup>год</sup> = 0,024∙ГСОП∙V<sub>от</sub>∙' \
             f'q<sub>от</sub><sup>р</sup></i> = 0,024∙{self.gsop}∙{self.v_heat}∙{self.q_ot} = ' \
             f'{round(0.024 * self.gsop * self.q_ot * self.v_heat, 2)} кВт·ч/год.</p>'
        s += "<p>Общие теплопотери здания за отопительный период " \
             "определяется по формуле Г.11 приложения Г СП 50.13330.2012</p>"
        s += f'<p align="center"><i>Q<sub>общ</sub><sup>год</sup> = 0,024∙ГСОП∙V<sub>от</sub>(k<sub>об</sub> - ' \
             f'k<sub>вент</sub>)</i> = 0,024∙{self.gsop}∙{self.v_heat}∙({self.k_ob} + {self.k_vent}) = ' \
             f'{round(0.024 * self.gsop * self.v_heat * (self.k_ob + self.k_vent), 2)} кВт·ч/год.</p>'

        # вывод нормативной удельной характеристики
        s += f'<p>Нормируемая удельная характеристика расхода тепловой энергии на отопление и вентиляцию здания ' \
             f'определяется по таблице 14 СП 50.13330.2012 для типа здания - {self.typ.lower()}, и этажности ' \
             f'здания - {self.floors}, составляет q<sub>от</sub><sup>тр</sup> = {self.udeln} Вт/(м³∙°С) с учетом ' \
             f'требования по снижению на 20% с 1 июля 2018 г. в соответствии с Приказом Министерства строительства ' \
             f'и жилищно-коммунального хозяйства РФ от 17 ноября 2017 г. N 1550/пр "Об утверждении Требований ' \
             f'энергетической эффективности зданий, строений, сооружений" </p>'
        # вывод класса энергоэффективности
        s += f'<p>Величина отклонения расчетного (фактического) значения удельной характеристики расхода ' \
             f'тепловой энергии на отопление и вентиляцию здания от нормируемого составляет {self.otklon} %.</p>'
        s += f'<p>В соответствии с таблицей 15 СП 50.13330.2012 для здания определен класс энергосбережения -' \
             f' {self.class_energ[0]} ({self.class_energ[1]}).</p>'
        text.insertHtml(s)

    def get_text_pasport_html(self, text: object):
        """Генерация табличного представления энергетического паспорта"""
        s = """<style type="text/css">
           TABLE {
            border-collapse: collapse;
           }
           TD, TH {
            padding: 3px;
            border: 1px solid black;
           }
           table tr td{
           text-align: left;
           }
            table tr td+td{
           text-align: center;
           }
          </style>"""
        # вывод общей информации
        s += '<h2 align="center">1 Общая информация</h2>'
        s += f"""<table border="1">"""
        s += f"""<tr><td>Дата заполнения (число, месяц, год)</td>  <td></td></tr>"""
        s += f"""<tr><td>Адрес здания</td>  <td></td></tr>"""
        s += f"""<tr><td>Разработчик проекта</td>  <td></td></tr>"""
        s += f"""<tr><td>Адрес и телефон разработчика</td>  <td></td></tr>"""
        s += f"""<tr><td>Шифр проекта</td>  <td></td></tr>"""
        s += f"""<tr><td>Назначение здания, серия</td>  <td></td></tr>"""
        s += f"""<tr><td>Этажность, количество секций</td>  <td>{self.floors}</td></tr>"""
        s += f"""<tr><td>Количество квартир</td>  <td></td></tr>"""
        s += f"""<tr><td>Расчетное количество жителей или служащих</td>  <td></td>{self.tenants}</tr>"""
        s += f"""<tr><td>Размещение в застройке</td>  <td></td></tr>"""
        s += f"""<tr><td>Конструктивное решение</td>  <td></td></tr>"""
        s += """</table>"""

        # вывод расчетных условий
        s += '<h2 align="center">2 Расчетные условия</h2>'
        s += f"""<table border="1">
           <tr>
            <th>Наименование расчетных параметров</th>
            <th>Обозначение параметра</th>
            <th>Единица измерения</th>
            <th>Расчетное значение</th>
           </tr>"""
        s += f"""<tr><td>1 Расчетная температура наружного воздуха для проектирования теплозащиты</td>
        <td>t<sub>н</sub></td>  <td>°С</td>  <td>{self.t_nhp}</td></tr>"""
        s += f"""<tr><td>2 Средняя температура наружного воздуха за отопительный период</td>
        <td>t<sub>от</sub></td>  <td>°С</td>  <td>{self.t_ot}</td></tr>"""
        s += f"""<tr><td>3 Продолжительность отопительного периода</td>
        <td>z<sub>от</sub></td>  <td>сут/год</td>  <td>{self.z_ot}</td></tr>"""
        s += f"""<tr><td>4 Градусо-сутки отопительного периода</td>
        <td>ГСОП</td>  <td>°С·сут/год</td>  <td>{self.gsop}</td></tr>"""
        s += f"""<tr><td>5 Расчетная температура внутреннего воздуха для проектирования теплозащиты</td>
        <td>t<sub>в</sub></td>  <td>°С</td>  <td>{self.t_int}</td></tr>"""
        has_attic = False
        elem_attic = None
        for elem in self.constructions:
            if elem.purpose == 'Внутреняя чердака':
                has_attic = True
                elem_attic = elem
        if has_attic == True:
            s += f"""<tr><td>6 Расчетная температура чердака</td>
            <td>t<sub>черд</sub></td>  <td>°С</td>  <td>{elem_attic.t_ext}</td></tr>"""
        else:
            s += f"""<tr><td>6 Расчетная температура чердака</td>
            <td>t<sub>черд</sub></td>  <td>°С</td>  <td> - </td></tr>"""
        has_basement = False
        elem_basement = None
        for elem in self.constructions:
            if elem.purpose == 'Внутреняя подвала':
                has_basement = True
                elem_basement = elem
        if has_basement == True:
            s += f"""<tr><td>7 Расчетная температура техподполья</td>
                <td>t<sub>подп</sub></td>  <td>°С</td>  <td>{elem_basement.t_ext}</td></tr>"""
        else:
            s += f"""<tr><td>7 Расчетная температура техподполья</td>
                <td>t<sub>подп</sub></td>  <td>°С</td>  <td> - </td></tr>"""
        s += """</table>"""

        # вывод показателей геометрических
        s += '<h2 align="center">3 Показатели геометрические</h2>'
        s += f"""<table border="1">
           <tr>
            <th>Показатель</th>
            <th>Обозначение и единица измерения</th>
            <th>Расчетное проектное значение</th>
            <th>Фактическое значение</th>
           </tr>"""
        s += f"""<tr><td>8 Сумма площадей этажей здания</td>
        <td>А<sub>от</sub>, м²</td>  <td>{self.area_all}</td>  <td>  </td></tr>"""
        s += f"""<tr><td>9 Площадь жилых помещений</td>
        <td>А<sub>ж</sub>, м²</td>  <td>{self.area_live}</td>  <td>  </td></tr>"""
        s += f"""<tr><td>10 Расчетная площадь (общественных зданий)</td>
        <td>А<sub>р</sub>, м²</td>  <td>{self.area_calc}</td>  <td>  </td></tr>"""
        s += f"""<tr><td>11 Отапливаемый объем</td>
        <td>V<sub>от</sub>, м³</td>  <td>{self.v_heat}</td>  <td>  </td></tr>"""
        area_fasad = 0.0
        area_okon = 0.0
        area_vitr = 0.0
        area_fonar = 0.0
        area_door = 0.0
        area_ogr = 0.0
        area_wall = 0.0
        area_pokr = 0.0
        area_attic = 0.0
        area_warm_attic = 0.0
        area_basement = 0.0
        area_proezd = 0.0
        area_ground = 0.0
        for elem in self.constructions:
            if elem.typ in ['Наружная стена', 'Окна', 'Витражи', 'Фонари', 'Двери', 'Ворота']:
                area_fasad += elem.area
                if elem.typ == 'Окна':
                    area_okon += elem.area
                if elem.typ == 'Витражи':
                    area_vitr += elem.area
                if elem.typ == 'Фонари':
                    area_fonar += elem.area
                if elem.typ in ['Двери', 'Ворота']:
                    area_door += elem.area
            if elem.purpose in ['Ограждающая', 'Внутреняя подвала', 'Внутреняя чердака']:
                area_ogr += elem.area
            if elem.typ == 'Наружная стена' and elem.purpose == 'Ограждающая':
                area_wall += elem.area
            if elem.typ == 'Покрытие':
                area_pokr += elem.area
            if elem.typ == 'Чердачное перекрытие' and elem.purpose == 'Ограждающая':
                area_attic += elem.area
            if elem.typ == 'Чердачное перекрытие' and elem.purpose == 'Внутреняя чердака':
                area_warm_attic += elem.area
            if elem.typ == 'Перекрытие над холодным подвалом':
                area_basement += elem.area
            if elem.typ == 'Перекрытие над проездом':
                area_proezd += elem.area
            if elem.typ == 'Конструкция в контакте с грунтом':
                area_ground += elem.area
        try:
            coef_ostekl = round((area_okon + area_vitr + area_fonar) / area_fasad, 2)
            compact = round(area_ogr / self.v_heat, 2)
        except ZeroDivisionError:
            coef_ostekl = 0
            compact = 0
        s += f"""<tr><td>12 Коэффициент остекленности фасада здания</td>
        <td>f</td>  <td>{coef_ostekl}</td>  <td>  </td></tr>"""
        s += f"""<tr><td>13 Показатель компактности здания</td>
        <td>К<sub>комп</sub></td>  <td>{compact}</td>  <td>  </td></tr>"""
        s += f"""<tr><td>14 Общая площадь наружных ограждающих конструкций здания,</td>
        <td>А<sub>н</sub><sup>сум</sup>, м²</td>  <td>{round(area_ogr, 2)}</td>  <td>  </td></tr>"""
        s += f"""<tr><td>в том числе:</td>
        <td>  </td>  <td>  </td>  <td>  </td></tr>"""
        s += f"""<tr><td>    фасадов</td>
        <td>А<sub>фас</sub>, м²</td>  <td>{round(area_fasad, 2)}</td>  <td>  </td></tr>"""
        s += f"""<tr><td>    стен (раздельно по типу конструкции)</td>
        <td>А<sub>ст</sub>, м²</td>  <td>{round(area_wall, 2)}</td>  <td>  </td></tr>"""
        i = 0
        for elem in self.constructions:
            if elem.typ == 'Наружная стена' and elem.purpose == 'Ограждающая':
                i += 1
                s += f"""<tr><td>    {elem.get_construction_name().lower()}</td>
                <td>А<sub>ст{i}</sub>, м²</td>  <td>{round(elem.area, 2)}</td>  <td>  </td></tr>"""
        s += f"""<tr><td>окон и балконных дверей</td>
        <td>А<sub>ок.1</sub>, м²</td>  <td>{round(area_okon, 2)}</td>  <td>  </td></tr>"""
        s += f"""<tr><td>витражей</td>
        <td>А<sub>ок.2</sub>, м²</td>  <td>{round(area_vitr, 2)}</td>  <td>  </td></tr>"""
        s += f"""<tr><td>фонарей</td>
        <td>А<sub>ок.3</sub>, м²</td>  <td>{round(area_fonar, 2)}</td>  <td>  </td></tr>"""
        s += f"""<tr><td>окон лестнично-лифтовых узлов</td>
        <td>А<sub>ок.4</sub>, м²</td>  <td> - </td>  <td>  </td></tr>"""
        s += f"""<tr><td>балконных дверей наружных переходов</td>
        <td>А<sub>дв</sub>, м²</td>  <td> - </td>  <td>  </td></tr>"""
        s += f"""<tr><td>входных дверей и ворот (раздельно)</td>
        <td>А<sub>дв</sub>, м²</td>  <td>{round(area_door, 2)}</td>  <td>  </td></tr>"""
        s += f"""<tr><td>покрытий (совмещенных)</td>
        <td>А<sub>покр</sub>, м²</td>  <td>{round(area_pokr, 2)}</td>  <td>  </td></tr>"""
        s += f"""<tr><td>чердачных перекрытий</td>
        <td>А<sub>черд</sub>, м²</td>  <td>{round(area_attic, 2)}</td>  <td>  </td></tr>"""
        s += f"""<tr><td>перекрытий "теплых" чердаков (эквивалентная)</td>
        <td>А<sub>черд.т</sub>, м²</td>  <td>{round(area_warm_attic, 2)}</td>  <td>  </td></tr>"""
        s += f"""<tr><td>перекрытий над техническими подпольями или над неотапливаемыми подвалами</td>
        <td>А<sub>цок1</sub>, м²</td>  <td>{round(area_basement, 2)}</td>  <td>  </td></tr>"""
        s += f"""<tr><td>перекрытий над проездами или под эркерами</td>
        <td>А<sub>цок2</sub>, м²</td>  <td>{round(area_proezd, 2)}</td>  <td>  </td></tr>"""
        s += f"""<tr><td>стен в земле и пола по грунту</td>
        <td>А<sub>цок3</sub>, м²</td>  <td>{round(area_ground, 2)}</td>  <td>  </td></tr>"""
        s += """</table>"""

        # вывод показателей теплотехнических
        s += '<h2 align="center">4 Показатели теплотехнические</h2>'
        s += f"""<table border="1">
           <tr>
            <th>Показатель</th>
            <th>Обозначение и единица измерения</th>
            <th>Нормируемое значение</th>
            <th>Расчетное проектное значение</th>
            <th>Фактическое значение</th>
           </tr>"""
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
                pass
            try:
                r_con[key][2] = round(r_con[key][0] / r_con[key][2], 2)
            except ZeroDivisionError:
                pass

        s += f"""<tr><td>15 Приведенное сопротивление теплопередаче наружных ограждений, в том числе:</td>
        <td>R<sub>o</sub><sup>пр</sup>, м²·°С/Вт</td>  <td>{round(self.r_pr_norm, 2)}</td>  
        <td>{round(self.r_pr, 2)}</td>   <td>  </td></tr>"""
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
        i = 0
        for key in ['Наружная стена', 'Окна', 'Витражи', 'Фонари', 'Окон ЛЛУ', 'Дверей наружных переходов',
                    'Двери', 'Покрытие', 'Чердачное перекрытие', 'Чердачное перекрытие',
                    'Перекрытие над холодным подвалом', 'Перекрытие над проездом', 'Конструкция в контакте с грунтом']:
            s += f"""<tr><td>{name[i]}</td>
            <td>{index[i]}</td>  <td>{r_con[key][1] if key in r_con else '-'}</td>  
            <td>{r_con[key][2] if key in r_con else '-'}</td>   <td>  </td></tr>"""
            i += 1
        s += """</table>"""

        # вывод показателей вспомогательных
        s += '<h2 align="center">5 Показатели вспомогательные</h2>'
        s += f"""<table border="1">
           <tr>
            <th>Показатель</th>
            <th>Обозначение показателя и единица измерения</th>
            <th>Нормируемое значение показателя</th>
            <th>Расчетное проектное значение показателя</th>
           </tr>"""
        s += f"""<tr><td>16 Общий коэффициент теплопередачи здания</td>
        <td>K<sub>общ</sub>, Вт/м²·°С</td>  <td>{round(1 / self.r_pr_norm, 3) if self.r_pr_norm > 0 else '-'}</td>  
        <td>{round(1 / self.r_pr, 3) if self.r_pr > 0 else '-'}</td> </tr>"""
        s += f"""<tr><td>17 Средняя кратность воздухообмена здания за отопительный период при удельной 
        норме воздухообмена</td>
        <td>n<sub>в</sub>, ч<sup>-1</sup></td>  <td> - </td>  
        <td>{self.n_v}</td> </tr>"""
        s += f"""<tr><td>18 Удельные бытовые тепловыделения в здании</td>
        <td>q<sub>быт</sub>, Вт/м²</td>  <td> - </td>  
        <td>{self.q_bit}</td> </tr>"""
        s += f"""<tr><td>19 Тарифная цена тепловой энергии для проектируемого здания</td>
        <td>q<sub>быт</sub>, Вт/м²</td>  <td> - </td>  
        <td> - </td> </tr>"""
        s += """</table>"""

        # вывод удельных характеристик
        s += '<h2 align="center">6 Удельные характеристики</h2>'
        s += f"""<table border="1">
           <tr>
            <th>Показатель</th>
            <th>Обозначение показателя и единица измерения</th>
            <th>Нормируемое значение показателя</th>
            <th>Расчетное проектное значение показателя</th>
           </tr>"""
        s += f"""<tr><td>20 Удельная теплозащитная характеристика здания</td>
        <td>k<sub>об</sub>, Вт/м³·°С</td>  <td>{self.k_ob_tr}</td>  
        <td>{self.k_ob}</td> </tr>"""
        s += f"""<tr><td>21 Удельная вентиляционная характеристика здания</td>
        <td>k<sub>вент</sub>, Вт/м³·°С</td>  <td> - </td>  
        <td>{self.k_vent}</td> </tr>"""
        s += f"""<tr><td>22 Удельная характеристика бытовых тепловыделений здания</td>
        <td>k<sub>быт</sub>, Вт/м³·°С</td>  <td> - </td>  
        <td>{self.k_bit}</td> </tr>"""
        s += f"""<tr><td>23 Удельная характеристика теплопоступлений в здание от солнечной радиации</td>
        <td>k<sub>рад</sub>, Вт/м³·°С</td>  <td> - </td>  
        <td>{self.k_rad}</td> </tr>"""
        s += """</table>"""

        # вывод коэффициентов
        s += '<h2 align="center">7 Коэффициенты</h2>'
        s += f"""<table border="1">
           <tr>
            <th>Показатель</th>
            <th>Обозначение показателя и единица измерения</th>
            <th>Значение показателя</th>
           </tr>"""
        s += f"""<tr><td>26 Коэффициент эффективности рекуператора</td>
        <td>k<sub>эф</sub></td>  <td> - </td> </tr>"""
        s += """</table>"""

        # вывод показателей
        s += '<h2 align="center">8 Комплексные показатели расхода тепловой энергии</h2>'
        s += f"""<table border="1">
           <tr>
            <th>Показатель</th>
            <th>Обозначение показателя и единица измерения</th>
            <th>Значение показателя</th>
           </tr>"""
        s += f"""<tr><td>29 Расчетная удельная характеристика расхода тепловой энергии на отопление и вентиляцию 
        здания за отопительный период</td>
        <td>q<sub>от</sub><sup>р</sup>, Вт/м³·°С</td>  <td>{self.q_ot}</td> </tr>"""
        s += f"""<tr><td>30 Нормируемая удельная характеристика расхода тепловой энергии на отопление и вентиляцию 
        здания за отопительный период</td>
        <td>q<sub>от</sub><sup>тр</sup>, Вт/м³·°С</td>  <td>{self.udeln}</td> </tr>"""
        s += f"""<tr><td>31 Класс энергосбережения</td>
        <td>  </td>  <td>{self.class_energ[0]}</td> </tr>"""
        s += f"""<tr><td>32 Соответствует ли проект здания нормативному требованию по теплозащите</td>
        <td>  </td>  <td>Соответствует</td> </tr>"""
        s += """</table>"""

        # вывод удельных характеристик
        s += '<h2 align="center">9 Энергетические нагрузки здания</h2>'
        s += f"""<table border="1">
           <tr>
            <th>Показатель</th>
            <th>Обозначение</th>
            <th>Единица измерений</th>
            <th>Значение показателя</th>
           </tr>"""
        try:
            h_floor = self.v_heat / self.area_all
        except ZeroDivisionError:
            h_floor = 0.0
        s += f"""<tr><td>33 Удельный расход тепловой энергии на отопление и вентиляцию здания за отопительный период</td>
        <td> q </td>  <td><p align="center">кВт·ч/(м³·год)</p>  <p align="center">кВт·ч/(м²·год)</p></td>  
        <td><p align="center">{round(0.024 * self.gsop * self.q_ot, 2)}</p>  
        <p align="center">{round(0.024 * self.gsop * self.q_ot * h_floor, 2)}</p>
        </td> </tr>"""
        s += f"""<tr><td>34 Расход тепловой энергии на отопление и вентиляцию здания за отопительный период</td>
        <td> Q<sub>от</sub><sup>год</sup> </td>  <td>кВт·ч/год</td>  
        <td> {round(0.024 * self.gsop * self.q_ot * self.v_heat, 2)} </td> </tr>"""
        s += f"""<tr><td>35 Общие теплопотери здания за отопительный период</td>
        <td> Q<sub>общ</sub><sup>год</sup> </td>  <td>кВт·ч/год</td>  
        <td> {round(0.024 * self.gsop * self.v_heat * (self.k_ob + self.k_vent), 2)} </td> </tr>"""
        s += """</table>"""
        text.insertHtml(s)

    def get_text_class_html(self, text: object):
        """Генерация табличного представления расчета класса энергосбережения"""
        s = """<style type="text/css">
           TABLE {
            border-collapse: collapse;
           }
           TD, TH {
            padding: 3px;
            border: 1px solid black;
           }
           table tr td{
           text-align: left;
           }
            table tr td+td{
           text-align: center;
           }
          </style>"""
        # вывод общей информации
        s += '<h4 align="center">Показатели расчета</h4>'
        s += f"""<table border="1">
           <tr>
            <th>Наименование показателя</th>
            <th>Значение показателя</th>
           </tr>"""
        s += f"""<tr><td>Базовый уровень удельного годового расхода, кВт·ч/м²</td> <td> {self.q_class} </td> </tr>"""
        s += f"""<tr><td>Заселенность, м²/чел</td> <td> 17 </td> </tr>"""
        s += f"""<tr><td>Расчетное количество жителей, чел </td> <td> {self.calc_tenants} </td> </tr>"""
        s += f"""<tr><td>Нормативный воздухообмен на одного человека, м³/ч </td> <td> 30 </td> </tr>"""
        s += f"""<tr><td>Количество воздуха для обеспечения воздухообмена, м³/ч</td> <td> {self.volume_air} </td> </tr>"""
        s += f"""<tr><td>Средняя кратность воздухообмена, ч<sup>-1</sup></td> <td> {self.air_cratn} </td> </tr>"""
        s += f"""<tr><td>Удельная вентиляционная характеристика здания, Вт/(м³·°С)</td> <td> {self.k_vent2} </td> </tr>"""
        s += f"""<tr><td>Удельные бытовые теплопоступления, Вт/м²</td> <td> 17 </td> </tr>"""
        s += f"""<tr><td>Удельная характеристика бытовых теплопоступления, Вт/(м³·°С)</td> <td> {self.k_bit2} </td> </tr>"""
        s += f"""<tr><td>Расчетная удельная характеристика расхода тепловой энергии, 
              пересчитанная по Приказу от 6 июня 2016 г. N 399/пр, Вт/(м³·°С)</td> <td> {self.q_ot2} </td> </tr>"""
        s += f"""<tr><td>Удельный расход тепловой энергии на отопление и вентиляцию здания за 
                отопительный период, кВт·ч/м²</td> <td> {self.q_ras} </td> </tr>"""
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
        s += f"""<tr><td>Величина отклонения значения фактического удельного годового расхода энергетических ресурсов 
                 от базового уровня, %</td> <td> {otklon} </td> </tr>"""
        s += f"""<tr><td>Класс энергетической эффективности по Приказу от 6 июня 2016 г. N 399/пр</td> 
        <td> <p align='center'>{class_energ[0]}</p> <p align='center'>{class_energ[1]}</p> </td> </tr>"""
        s += """</table>"""

        text.insertHtml(s)
