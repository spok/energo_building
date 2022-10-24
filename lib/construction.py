from lib.layer import Layer
from lib.material import Material


class Construction:
    def __init__(self):
        self.__layers = []
        self.__ratio_inner_surface = 8.7
        self.__ratio_outer_surface = 23
        self.__ratio_r = 1
        self.__resistance = 0.0
        self.__inertia = 0.0
        self.__name = ""
        self.__type_construction = "Наружная стена"
        self.__location = 'Ограждающая'
        self.__area = 0.0
        self.__thickness = 0.0

    @staticmethod
    def to_float(text: str) -> float:
        """
        Конвертация строковой переменной в вещественное число
        :param text: строковой тип
        :return: вещественный тип
        """
        if len(text) > 0:
            text = text.replace(",", ".")
        else:
            text = '0'
        try:
            result = float(text)
        except ValueError:
            result = 0.0
        return result

    def add_layer(self, material: Material, index: int):
        """
        Добавление нового слоя в конец списка
        :return: None
        """
        new_layer = Layer()
        new_layer.material = material
        if index == len(self.__layers) - 1:
            self.__layers.append(new_layer)
        else:
            self.__layers.insert(index + 1, new_layer)
        self.calc_resistance()

    def move_up(self, index: int):
        """Перемещение слоя к внутренней поверхности"""
        if index > 0:
            self.__layers[index], self.__layers[index - 1] = self.__layers[index - 1], self.__layers[index]

    def move_down(self, index: int):
        """Перемещение слоя к внутренней поверхности"""
        if index < len(self.__layers) - 1:
            self.__layers[index], self.__layers[index + 1] = self.__layers[index + 1], self.__layers[index]

    @property
    def ratio_inner_surface(self):
        return self.__ratio_inner_surface

    @ratio_inner_surface.setter
    def ratio_inner_surface(self, ratio: float):
        self.__ratio_inner_surface = ratio
        self.calc_resistance()

    @property
    def ratio_outer_surface(self):
        return self.__ratio_outer_surface

    @ratio_outer_surface.setter
    def ratio_outer_surface(self, ratio: float):
        self.__ratio_outer_surface = ratio
        self.calc_resistance()

    @property
    def ratio_r(self):
        return self.__ratio_r

    @ratio_r.setter
    def ratio_r(self, value: str):
        self.__ratio_r = self.to_float(value)
        self.calc_resistance()

    @property
    def thickness(self):
        return self.__thickness

    @property
    def resistance(self):
        return self.__resistance

    @property
    def inertia(self):
        return self.__inertia

    def calc_resistance(self):
        """Расчет сопротивления теплопередаче"""
        self.__resistance = 0
        self.__thickness = 0
        self.__inertia = 0
        for layer in self.__layers:
            self.__resistance += layer.resistance
            self.__inertia += layer.inertia
            self.__thickness += layer.thickness
        self.__resistance += 1/self.__ratio_inner_surface
        self.__resistance += 1 / self.__ratio_outer_surface
        self.__resistance = self.__resistance * self.__ratio_r

    def get_layers(self):
        """Генератор параметров слоев"""
        for layer in self.__layers:
            yield layer.get_tuple()

    def set_layer(self, layer: tuple, index: int):
        self.__layers[index].thickness = self.to_float(layer[1])
        self.calc_resistance()
