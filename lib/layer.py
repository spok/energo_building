from lib.material import Material


class Layer:
    def __init__(self):
        self.__number = 1
        self.__thickness = 0.0
        self.__ratio_lam = 0.0
        self.__ratio_s = 0.0
        self.__resistance = 0.0
        self.__inertia = 0.0
        self.__material = Material()

    def calc_resistance(self):
        """
        Расчет сопротивления теплопередаче слоя
        :return: None
        """
        if self.__ratio_lam != 0:
            self.__ratio_lam = self.__material.get_lam()
            self.__resistance = round(self.__thickness / 1000 / self.__ratio_lam, 3)
            self.__inertia = self.__resistance * self.__ratio_s
        else:
            self.__resistance = 0
            self.__inertia = 0

    @property
    def material(self):
        return self.__material

    @material.setter
    def material(self, new_material: Material):
        self.__material = new_material
        self.__ratio_lam = self.__material.get_lam()
        self.__ratio_s = self.__material.get_s()
        self.calc_resistance()

    @property
    def name(self):
        return self.__material.name

    @property
    def resistance(self):
        return self.__resistance

    @property
    def inertia(self):
        return self.__inertia

    @property
    def number(self):
        return self.__number

    @number.setter
    def number(self, new_number: int):
        if type(new_number) == int and new_number > 0:
            self.__number = new_number

    @property
    def thickness(self):
        return self.__thickness

    @thickness.setter
    def thickness(self, new_thickness: float = 0):
        if new_thickness >= 0:
            self.__thickness = new_thickness
        else:
            raise ValueError("Толщина слоя должна быть положительным числом")
        self.calc_resistance()

    @property
    def ratio_lam(self):
        return self.__ratio_lam

    @property
    def ratio_s(self):
        return self.__ratio_s

    def get_text_sym(self) -> str:
        """
        Генерация html представления формулы расчета сопротивления теплопередаче
        :return: str
        """
        return f'δ<sub>{self.__number}</sub>/λ<sub>{self.__number}</sub>'

    def get_text_num(self) -> str:
        """
        Генерация html представления расчета сопротивления теплопередаче
        :return: str
        """
        return f'{self.__thickness / 1000}/{self.__ratio_lam}'

    def get_dict(self):
        """
        Возвращает словарь с данными текущего слоя
        :return: dict
        """
        curr_dict = dict()
        curr_dict["number"] = self.__number
        curr_dict["thickness"] = self.__thickness
        curr_dict["ratio_lam"] = self.__ratio_lam
        curr_dict["material"] = self.__material.get_dict_from_data()
        return curr_dict

    def set_from_dict(self, new_data: dict = None):
        """
        Установка параметров слоя
        :param new_data: словарь с новыми данными
        :return: None
        """
        if new_data is None:
            new_data = dict()
        self.__material.set_from_dict(new_data.get("material", None))
        self.__number = new_data.get("number", 1)
        self.__thickness = new_data.get("thickness", 0.0)
        self.__ratio_lam = new_data.get("ratio_lam", 0.0)

    def get_tuple(self):
        """
        Возвращает кортеж с параметрами слоя
        :return: кортеж
        """
        return self.__number, str(self.__material), self.__thickness, self.__ratio_lam, self.__ratio_s, \
               self.__resistance, self.__inertia
