class Material:
    environment = "А"

    def __init__(self):
        self.__name = ''
        self.__density = 0.0
        self.__ratio_lama = 0.0
        self.__ratio_lamb = 0.0
        self.__ratio_sa = 0.0
        self.__ratio_sb = 0.0
        self.number = 0

    def __str__(self):
        return f"{self.name}, плотность {self.density} кг/куб. м"

    def __eq__(self, other):
        result = True
        if result and self.__name != other.name:
            result = False
        if result and self.__density != other.density:
            result = False
        if result and self.__ratio_lama != other.ratio_lama:
            result = False
        if result and self.__ratio_lamb != other.ratio_lamb:
            result = False
        if result and self.__ratio_sa != other.ratio_sa:
            result = False
        if result and self.__ratio_sb != other.ratio_sb:
            result = False
        return result

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name: str):
        if type(new_name) == str:
            self.__name = new_name
        else:
            raise ValueError("Название материала должно иметь строковой тип данных")

    def check_name(self, text: str) -> bool:
        """Проверка на вхождение текста в название материала"""
        if text in self.__name.lower():
            return True
        return False

    @property
    def density(self):
        return self.__density

    @density.setter
    def density(self, new_density: float):
        if type(new_density) in [int, float]:
            self.__density = new_density
        else:
            raise ValueError("Плотность должна иметь тип данных: целое или вещественное")

    @property
    def ratio_lama(self):
        return self.__ratio_lama

    @ratio_lama.setter
    def ratio_lama(self, new_ratio: float):
        if type(new_ratio) in [int, float]:
            self.__ratio_lama = new_ratio
        else:
            raise ValueError("Коэффициент теплопроводности должен иметь тип данных: целое или вещественное")

    @property
    def ratio_lamb(self):
        return self.__ratio_lamb

    @ratio_lamb.setter
    def ratio_lamb(self, new_ratio: float):
        if type(new_ratio) in [int, float]:
            self.__ratio_lamb = new_ratio
        else:
            raise ValueError("Коэффициент теплопроводности должен иметь тип данных: целое или вещественное")

    @property
    def ratio_sa(self):
        return self.__ratio_sa

    @ratio_sa.setter
    def ratio_sa(self, new_ratio: float):
        if type(new_ratio) in [int, float]:
            self.__ratio_sa = new_ratio
        else:
            raise ValueError("Коэффициент теплоусвоения должен иметь тип данных: целое или вещественное")

    @property
    def ratio_sb(self):
        return self.__ratio_sb

    @ratio_sb.setter
    def ratio_sb(self, new_ratio: float):
        if type(new_ratio) in [int, float]:
            self.__ratio_sb = new_ratio
        else:
            raise ValueError("Коэффициент теплоусвоения должен иметь тип данных: целое или вещественное")

    def get_tuple(self) -> tuple:
        """Возвращает кортеж с параметрами материала"""
        return self.number, self.__name, self.__density, self.__ratio_lama, self.__ratio_lamb, self.__ratio_sa, self.__ratio_sb

    def get_dict_from_data(self) -> dict:
        """
        Возвращает словарь с данными материала
        :return: dict
        """
        data = dict()
        data["name"] = self.__name
        data["density"] = self.__density
        data["ratio_lama"] = self.__ratio_lama
        data["ratio_lamb"] = self.__ratio_lamb
        data["ratio_sa"] = self.__ratio_sa
        data["ratio_sb"] = self.__ratio_sb
        return data

    def set_from_dict(self, new_data: dict = None):
        """
        Установка параметров материала
        :param new_data: словарь с новыми данными
        :return: None
        """
        if new_data == None:
            new_data = dict()
        self.__name = new_data.get("name", "")
        self.__density = new_data.get("density", 0.0)
        self.__ratio_lama = new_data.get("ratio_lama", 0.0)
        self.__ratio_lamb = new_data.get("ratio_lamb", 0.0)
        self.__ratio_sa = new_data.get("ratio_sa", 0.0)
        self.__ratio_sb = new_data.get("ratio_sb", 0.0)

    def get_lam(self):
        """Определение коэффициента в зависимости от условия эксплуатации"""
        if type(Material.environment) == str and Material.environment in "АВ":
            if Material.environment == "А":
                if self.__ratio_lama == 0 and self.__ratio_lamb != 0:
                    return self.__ratio_lamb
                else:
                    return self.__ratio_lama
            else:
                if self.__ratio_lamb == 0 and self.__ratio_lama != 0:
                    return self.__ratio_lama
                else:
                    return self.__ratio_lamb

    def get_s(self):
        """Определение коэффициента в зависимости от условия эксплуатации"""
        if type(Material.environment) == str and Material.environment in "АВ":
            if Material.environment == "А":
                if self.__ratio_sa == 0 and self.__ratio_sb != 0:
                    return self.__ratio_sb
                else:
                    return self.__ratio_sa
            else:
                if self.__ratio_sb == 0 and self.__ratio_sa != 0:
                    return self.__ratio_sa
                else:
                    return self.__ratio_sb

