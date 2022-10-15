import csv
import json
from lib.material import Material


class Materials:
    def __init__(self):
        self.__materials = []

    def len_materials(self):
        return len(self.__materials)

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
        except ValueError as err:
            result = 0.0
        return result

    def add_material(self, new_material: tuple, index: int = 0):
        """
        Добавление нового материала в список
        :param new_material: кортеж из данных материалов в строковом формате
        :param index: позиция вставляемого материала
        :return: None
        """
        mat = Material()
        mat.name = new_material[0]
        mat.density = self.to_float(new_material[1])
        mat.ratio_lama = self.to_float(new_material[2])
        mat.ratio_lamb = self.to_float(new_material[3])
        mat.ratio_sa = self.to_float(new_material[4])
        mat.ratio_sb = self.to_float(new_material[5])
        if index >= self.len_materials():
            self.__materials.append(mat)
        else:
            self.__materials.insert(index, mat)

    def dublicate_material(self, index: int):
        """
        Дублирование существующего материала
        :param index: текущий индекс дублируемого материала
        :return: None
        """
        cur_material = self.__materials[index]
        mat = Material()
        mat.name = cur_material.name
        mat.density = cur_material.density
        mat.ratio_lama = cur_material.ratio_lama
        mat.ratio_lamb = cur_material.ratio_lamb
        mat.ratio_sa = cur_material.ratio_sa
        mat.ratio_sb = cur_material.ratio_sb
        if index >= self.len_materials() - 1:
            self.__materials.append(mat)
        else:
            self.__materials.insert(index + 1, mat)

    def load_csv(self, path: str):
        """
        Загрузка данных материалов из csv файла
        :param path: путь к файлу с csv-файла
        :return: None
        """
        with open(path, encoding='utf-8') as file:
            rows = list(csv.reader(file, delimiter=";", quoting=csv.QUOTE_NONE))[1:]
            for elem in rows:
                if len(elem) > 0:
                    mat = Material()
                    mat.name = elem[0]
                    mat.density = float(elem[1].replace(",", "."))
                    mat.ratio_lama = float(elem[2].replace(",", "."))
                    mat.ratio_lamb = float(elem[3].replace(",", "."))
                    mat.ratio_sa = float(elem[4].replace(",", "."))
                    mat.ratio_sb = float(elem[3].replace(",", "."))
                    self.__materials.append(mat)

    def load_json(self, path: str):
        """
        Загрузка данных материалов из json-файла
        :param path: путь к файлу
        :return: None
        """
        with open(path, "r", encoding="utf-8") as f:
            json_data = json.load(f)
        self.__materials = []
        for elem in json_data:
            mat = Material()
            mat.set_data_from_dict(elem)
            self.__materials.append(mat)

    def dump_json(self, path: str):
        """
        Сохранение данных материалов в json-файл
        :param path: путь к файлу
        :return: None
        """
        json_data = []
        for elem in self.__materials:
            json_data.append(elem.get_dict_from_data())
        with open(path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=3)

    def filter_materials(self, text: str) -> list:
        """
        Фильтрация материалов по наличию текста в названии материала
        :param text: поисковый запрос
        :return: список словарей
        """
        if len(text) >= 3:
            filter_material = [x.get_dict_from_data() for x in self.__materials if text in x.name]
        else:
            filter_material = [x.get_dict_from_data() for x in self.__materials]
        return filter_material

    def get_by_name(self, name: str, density: float):
        """
        Возвращает материал из списка по названию и плотности
        :param name: название материала
        :param density: плотность материала
        :return: объект класса Material
        """
        material = None
        if type(name) == str and type(density) == float:
            for x in self.__materials:
                if x.name == name and x.density == density:
                    material = x
                    break
            if material is None:
                material = Material()
        else:
            raise ValueError("Параметры запрашиваемого материала не соответствуют требуемым")
        return material

    def get_by_index(self, index: int):
        """
        Возвращает материал по номеру в списке
        :param index: индекс материала
        :return: объект класса Material
        """
        material = None
        if index < self.len_materials():
            material = self.__materials[index]
        else:
            raise ValueError("Номер материала указан неверно")
        return material
