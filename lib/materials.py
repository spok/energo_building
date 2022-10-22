import csv
import os
import json
from lib.material import Material
from lib.config import *


class Materials:
    def __init__(self):
        self.__materials = []
        self.__current = None
        self.load_json()

    def count_materials(self):
        """Возвращает количество материалов в списке"""
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

    def add_material(self, new_material: tuple):
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
        if self.count_materials() > 0:
            mat.number = self.__materials[-1].number + 1
        else:
            mat.number = 1
        self.__materials.append(mat)

    def edit_material(self, new_material: tuple, index: int):
        """
        Редактирование существующего материала
        :param new_material: кортеж из данных материалов в строковом формате
        :param index: позиция редактируемого материала
        :return: None
        """
        for mat in self.__materials:
            if mat.number == index:
                break
        mat.name = new_material[0]
        mat.density = self.to_float(new_material[1])
        mat.ratio_lama = self.to_float(new_material[2])
        mat.ratio_lamb = self.to_float(new_material[3])
        mat.ratio_sa = self.to_float(new_material[4])
        mat.ratio_sb = self.to_float(new_material[5])

    def del_material(self, index: int):
        """
        Удаление материала из списка
        :param index: номер материала
        :return: None
        """
        for i, mat in enumerate(self.__materials):
            if mat.number == index:
                break
        del self.__materials[i]

    def copy_material(self, index: int):
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
        if index >= self.count_materials() - 1:
            self.__materials.append(mat)
        else:
            self.__materials.insert(index + 1, mat)

    def load_csv(self, path: str):
        """
        Загрузка данных материалов из csv файла
        :param path: путь к файлу с csv-файла
        :return: None
        """
        if os.path.exists(path):
            with open(path, encoding='utf-8') as file:
                rows = list(csv.reader(file, delimiter=";", quoting=csv.QUOTE_NONE))[1:]
                for i, elem in enumerate(rows, 1):
                    if len(elem) > 0:
                        mat = Material()
                        mat.name = elem[0]
                        mat.density = float(elem[1].replace(",", "."))
                        mat.ratio_lama = float(elem[2].replace(",", "."))
                        mat.ratio_lamb = float(elem[3].replace(",", "."))
                        mat.ratio_sa = float(elem[4].replace(",", "."))
                        mat.ratio_sb = float(elem[3].replace(",", "."))
                        mat.number = i
                        self.__materials.append(mat)

    def load_json(self):
        """
        Загрузка данных материалов из json-файла
        :param path: путь к файлу
        :return: None
        """
        if os.path.exists(PATH_MATERIALS):
            with open(PATH_MATERIALS, "r", encoding="utf-8") as f:
                json_data = json.load(f)
            self.__materials = []
            for i, elem in enumerate(json_data, 1):
                mat = Material()
                mat.number = i
                mat.set_from_dict(elem)
                self.__materials.append(mat)

    def dump_json(self):
        """
        Сохранение данных материалов в json-файл
        :param path: путь к файлу
        :return: None
        """
        json_data = []
        for elem in self.__materials:
            json_data.append(elem.get_dict_from_data())
        with open(PATH_MATERIALS, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=3)

    def get_materials(self, text: str=""):
        """
        Фильтрация материалов по наличию текста в названии материала
        :param text: поисковый запрос
        :return: список словарей
        """
        if self.count_materials() == 0:
            self.load_json()
        for x in self.__materials:
            if len(text) > 2:
                if x.check_name(text):
                    yield x.get_tuple()
            else:
                yield x.get_tuple()

    def get_by_name(self, name: str, density: float) -> Material:
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

    def get_by_index(self, index: int) -> Material:
        """
        Возвращает материал по номеру материала
        :param index: индекс материала
        :return: объект класса Material
        """
        material = None
        for elem in self.__materials:
            if index == elem.number:
                material = elem
                break
        return material
