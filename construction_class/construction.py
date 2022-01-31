from construction_class.base import *
from func import get_string_index, r_unit, alfa_unit, l_unit, load_solar_radiation, load_orientation_coef

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