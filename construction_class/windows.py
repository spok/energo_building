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
        if sum_area > 0:
            energy = dict()
            for elem in self.elements:
                area = elem.get_area_azimut()
                for key in self.orientation:
                    if key in area:
                        if key in energy:
                            energy[key] += solar_dict[key] * area[key]
                        else:
                            energy[key] = solar_dict[key] * area[key]
