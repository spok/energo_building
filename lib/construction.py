from lib.layer import Layer
from lib.material import Material


class Construction:
    def __init__(self):
        self.__layers = []                               # Список слоев
        self.__ratio_inner_surface = 8.7                 # Коэффициент теплоотдачи внутренней поверхности
        self.__ratio_outer_surface = 23.0                # Коэффициент теплоотдачи наружной поверхности
        self.__ratio_r = 1.0                             # Коэффициент теплотехнической однородности
        self.__resistance = 0.0                          # Общее сопротивление теплопередаче
        self.__inertia = 0.0                             # Тепловая инерция здания
        self.__name = ""                                 # Дополнительное описание конструкции
        self.__type_construction = "Наружная стена"      # Тип конструкции
        self.__location = 'Ограждающая'                  # Коэффициент теплотехнической однородности
        self.__area = 0.0                                # Площадь конструкции
        self.__thickness = 0                             # Общая толщина

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
        self.renumbering()

    def move_up(self, index: int):
        """Перемещение слоя к внутренней поверхности"""
        if index > 0:
            self.__layers[index], self.__layers[index - 1] = self.__layers[index - 1], self.__layers[index]
            self.renumbering()

    def move_down(self, index: int):
        """Перемещение слоя к внутренней поверхности"""
        if index < len(self.__layers) - 1:
            self.__layers[index], self.__layers[index + 1] = self.__layers[index + 1], self.__layers[index]
            self.renumbering()

    @property
    def name(self):
        cur_name = self.__type_construction
        if len(self.__name) > 0:
            cur_name += ' - ' + self.__name
        return cur_name

    @name.setter
    def name(self, new_name: str):
        self.__name = new_name

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

    def renumbering(self):
        for index, layer in enumerate(self.__layers):
            layer.number = index + 1

    def get_dict(self):
        """
        Возвращает словарь с данными текущей конструкции
        :return: dict
        """
        curr = dict()
        curr["name"] = self.__name
        curr["type_construction"] = self.__type_construction
        curr["location"] = self.__location
        curr["ratio_inner_surface"] = self.__ratio_inner_surface
        curr["ratio_outer_surface"] = self.__ratio_outer_surface
        curr["ratio_r"] = self.__ratio_r
        curr["area"] = self.__area
        layers = []
        for item in self.__layers:
            layers.append(item.get_dict())
        curr["layers"] = layers
        return curr

    def set_from_dict(self, new_data: dict = None):
        """
        Установка параметров конструкции
        :param new_data: словарь с новыми данными
        :return: None
        """
        if new_data is None:
            new_data = dict()
        self.__name = new_data.get("name", "")
        self.__type_construction = new_data.get("type_construction", "Наружная стена")
        self.__location = new_data.get("location", "Ограждающая")
        self.__ratio_inner_surface = new_data.get("ratio_inner_surface", 8.7)
        self.__ratio_outer_surface = new_data.get("ratio_outer_surface", 23.0)
        self.__ratio_r = new_data.get("ratio_r", 1.0)
        self.__area = new_data.get("area", 0.0)
        new_layers = new_data.get("layers", [])
        for item in new_layers:
            new_layer = Layer()
            new_layer.set_from_dict(item)

    def get_html(self) -> dict:
        """Генерация словаря для вывода в html-шаблон"""
        data = dict()
        data["layers"] = [x.get_tuple() for x in self.__layers]


        return data