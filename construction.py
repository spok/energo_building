from math import log
from func import get_string_index, r_unit, alfa_unit, l_unit, load_solar_radiation, load_orientation_coef
from copy import copy

class Material:
    def __init__(self):
        self.name = ''
        self.plotn = 0.0
        self.lam_a = 0.0
        self.lam_b = 0.0
        self.s_a = 0.0
        self.s_b = 0.0


class BaseConstruction:
    """Класс базовой конструкции"""
    def __init__(self):
        self.typ = ''
        self.name = ''
        self.area = 0.0
        self.r_pr = 0.0
        self.r_tr = 0.0
        self.r_tr_min = 0.0
        self.elements = []

    def get_dict(self):
        """Генерация словаря с данными
        :return - словарь"""
        data = dict()
        for key in self.__dict__:
            if key == 'elements':
                elements = []
                for elem in self.__dict__[key]:
                    elements.append(elem.get_dict())
                data[key] = elements
            else:
                data[key] = self.__dict__[key]
        return data

    def data_from_dict(self, data: dict):
        """Загрузка данных из словаря"""
        for key in data:
            if key == 'elements':
                self.elements.clear()
                for i, con in enumerate(data[key]):
                    self.add_layer()
                    self.elements[i].data_from_dict(con)
            else:
                if key in self.__dict__.keys():
                    self.__dict__[key] = data[key]

    def get_construction_name(self):
        """Генерация имени конструкции для дерева"""
        elem_text = ''
        if len(self.name) > 20:
            elem_text = self.name
        else:
            if len(self.name) == 0:
                elem_text = self.typ
            else:
                elem_text = self.typ + ' - ' + self.name
        return elem_text


class Doors(BaseConstruction):
    def __init__(self):
        super().__init__()


class WindowElement:
    def __init__(self):
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
        return area

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
        self.add_window(r=0.0, area=0.0, size='0*0')

    def add_window(self, r: float = 0.0, area: float = 0.0, size: str = '0*0'):
        elem = WindowElement()
        elem.r_pr = r
        elem.area = area
        elem.set_size(size)
        self.elements.append(elem)

    def del_window(self, index):
        """Удаления выбранной конструкции"""
        if len(self.elements) > 1:
            try:
                self.elements.pop(index)
            except:
                print(f'Невозможно удалить строку {index}')

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
            self.r_pr = sum_area/sum_r
        except:
            print('Ошибка деления на ноль')
        # Расчет солнечной радиации
        energy = dict()
        for elem in self.elements:
            area = elem.get_area_azimut()
            for key in self.orientation:
                if key in area:
                   energy[key] += solar_dict[key] * area[key]


class Layer:
    def __init__(self, name=''):
        self.name = ''
        self.thickness = 0.0
        self.lam = 0.0
        self.r = 0.0
        self.s = 0.0
        self.d = 0.0

    def calc(self):
        try:
            self.r = self.thickness/1000 / self.lam
        except ZeroDivisionError:
            self.r = 0.0
            print('Коэффициент теплопроводности не указан')
        self.d = self.r * self.s

    def get_dict(self) -> dict:
        """Генерация словаря с данными
        :return - словарь"""
        data = dict()
        for key in self.__dict__:
            data[key] = self.__dict__[key]
        return data

    def data_from_dict(self, data: dict):
        """Загрузка данных из словаря"""
        for key in data:
            if key in self.__dict__.keys():
                self.__dict__[key] = data[key]


class Construction(BaseConstruction):
    typ_surface_int = ['стен, полов, гладких потолков, потолков с выступающими ребрами при отношении высоты h ребер к расстоянию а между гранями соседних ребер h/a < 0,3',
                       'потолков с выступающими ребрами при отношении h/a > 0,3', 'окон', 'зенитных фонарей']
    typ_surface_ext = ['наружных стен, покрытий, перекрытий над проездами и над холодными (без ограждающих стенок) подпольями в Северной строительно-климатической зоне.',
                       'перекрытий над холодными подвалами, сообщающимися с наружным воздухом, перекрытий над холодными (с ограждающими стенками) подпольями и холодными этажами в Северной строительно-климатической зоне.',
                       'перекрытий чердачных и над неотапливаемыми подвалами со световыми проемами в стенах, а также наружных стен с воздушной прослойкой, вентилируемой наружным воздухом.',
                       'перекрытий над неотапливаемыми подвалами и техническими, подпольями не вентилируемых наружным воздухом.']
    list_alfa_int = [8.7, 7.6, 8.0, 9.9]
    list_alfa_ext = [23, 17, 12, 6]
    def __init__(self):
        super().__init__()
        self.alfa_int = 8.7
        self.alfa_ext = 23
        self.r_neodn = 1.0
        self.ro = 0.0
        self.b = 0.0
        self.y_int = 0.0
        self.add_layer('', 0.0, 0.0, 0.0)

    def add_layer(self, name='', thickness=0.0, lam=0.0, s=0.0):
        new_layer = Layer(name)
        new_layer.name = name
        new_layer.thickness = thickness
        new_layer.lam = lam
        new_layer.s = s
        self.elements.append(new_layer)

    def calc(self):
        """Расчет сопротивления теплопередаче конструкции"""
        rk = 0.0
        for i, elem in enumerate(self.elements):
            elem.calc()
            if elem.thickness > 0.00001 and elem.lam > 0.00001:
                rk += elem.r
        self.ro = round(1/self.alfa_int + rk + 1/self.alfa_ext, 2)
        self.r_pr = round(self.ro * self.r_neodn, 2)

    def get_text_r(self) -> str:
        """Генерация тектового представления расчета
        :return - строковое представление расчета"""

        s = 'Общее сопротивление теплопередаче конструкции:\n'
        s_elem = []
        rk = 0.0
        s_letters = ''
        s_numbers = ''
        for i, elem in enumerate(self.elements):
            if elem.thickness > 0.00001 and elem.lam > 0.00001:
                s_index = get_string_index(i+1)
                s_numbers += f' + {elem.thickness/1000}/{elem.lam}'
                s_letters += f' + δ{s_index}/λ{s_index}'
        s += f'Ro = 1/αв{s_letters} + 1/αн =\n'
        s += f'Ro = 1/{self.alfa_int}{s_numbers} + 1/{self.alfa_ext} = {self.ro} {r_unit()}\n'
        s += f'где αв = {self.alfa_int} {alfa_unit()} - коэффициент теплоотдачи внутренней поверхности конструкции,'
        s += f'определеяемый по таблице 4 СП 50.13330.2012 для {self.typ_surface_int[self.list_alfa_int.index(self.alfa_int)]};\n'
        s += f'где αн = {self.alfa_ext} {alfa_unit()} - коэффициент теплоотдачи наружной поверхности конструкции,'
        s += f'определеяемый по таблице 6 СП 50.13330.2012 для {self.typ_surface_ext[self.list_alfa_ext.index(self.alfa_ext)]}.\n'
        s += f'Теплотехническая однородность конструкции учитывается коэффициентом r = {self.r_neodn}.\n'
        s += 'Приведенное сопротивление теплопередаче будет равно:\n'
        s += f'Rпр = Ro · r = {self.ro} · {self.r_neodn} = {self.r_pr} {r_unit()}\n'
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
        return s


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
            if key not in ['constructions', 'norm']:
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
