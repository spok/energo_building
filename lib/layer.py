from material import Material


class Layer:
    def __init__(self):
        self.__number = 0
        self.__thickness = 0
        self.__ratio_lam = 0
        self.__resistance = 0
        self.__environment = "A"
        self.__material = Material()

    def calc_resistance(self):
        if self.__ratio_lam != 0:
            self.__resistance = round(self.__thickness / 1000 / self.__ratio_lam, 3)
        else:
            self.__resistance = 0

    @property
    def name(self):
        return self.__material.name

    @property
    def resistance(self):
        return self.__resistance

    @property
    def environment(self):
        return self.__environment

    @environment.setter
    def environment(self, new_value):
        if type(new_value) == str and new_value in "AB":
            self.__environment = new_value
            if new_value == "A":
                if self.__material.ratio_lama == 0 and self.__material.ratio_lamb != 0:
                    self.__ratio_lam = self.__material.ratio_lamb
                else:
                    self.__ratio_lam = self.__material.ratio_lama
            else:
                if self.__material.ratio_lamb == 0 and self.__material.ratio_lama != 0:
                    self.__ratio_lam = self.__material.ratio_lama
                else:
                    self.__ratio_lam = self.__material.ratio_lamb
            self.calc_resistance()

    @property
    def number(self):
        return self.__number

    @number.setter
    def number(self, new_number):
        if type(new_number) == int and new_number > 0:
            self.__number == new_number

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

    @ratio_lam.setter
    def ratio_lam(self, new_ratio_lam: float = 0):
        if type(new_ratio_lam) in [int, float]:
            self.__ratio_lam = new_ratio_lam
        else:
            raise ValueError("Значение коэффициент должно быть вещественным числом")
        if self.__environment == "A":
            self.__material.ratio_lama = new_ratio_lam
        else:
            self.__material.ratio_lamb = new_ratio_lam
        self.calc_resistance()

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
        return f'{self.__thickness}/{self.__ratio_lam}'

    def get_dict_from_data(self):
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

    def set_data_from_dict(self, new_data: dict = None):
        """
        Установка параметров слоя
        :param new_data: словарь с новыми данными
        :return: None
        """
        if new_data is None:
            new_data = dict()
        self.__material.set_data_from_dict(new_data.get("material", None))
        self.__number = new_data.get("number", 1)
        self.__thickness = new_data.get("thickness", 0.0)
        self.__ratio_lam = new_data.get("ratio_lam", 0.0)
