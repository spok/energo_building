from openpyxl import load_workbook
from PyQt5.QtWidgets import QComboBox, QListView
from PyQt5.QtCore import QStringListModel


def load_excel(fname: str) -> list:
    """Загрузка данных из файла Excel, fname - полный путь к файлу"""
    # ссылка на лист в таблице
    wb = load_workbook(fname)
    sheet = wb.worksheets[0]
    # количество заполненных строк
    max_row = sheet.max_row
    # чтение данных
    data_cities = []
    for i in range(6, max_row+1):
        row_citi = []
        for j in range(1, 21):
            row_citi.append(sheet.cell(row=i, column=j).value)
        data_cities.append(row_citi)
    return data_cities


def to_dot(s: str) -> str:
    if ',' in s:
        s = s.replace(',', '.')
    return s


def get_string_index(index: int) -> str:
    """Расчет нижнего индекса для значения
    :return - строковое представление индекса"""
    list_underline = ['₀', '₁', '₂', '₃', '₄', '₅', '₆', '₇', '₈', '₉']
    s_index = ''
    if type(index) == int:
        letters = str(index)
        for s in letters:
            try:
                i = int(s)
            except:
                print('Ошибка при конвертации номера слоя')
                i = -1
            if i > -1:
                s_index += list_underline[i]
    return s_index


def r_unit() -> str:
    """Возвращает единицу измерения сопротивления теплопередаче"""
    return 'м²·ºС/Вт'


def l_unit() -> str:
    """Возвращает единицу измерения коэффициент теплопроводности"""
    return 'Вт/(м·ºС)'


def alfa_unit() -> str:
    """Возвращает единицу измерения коэффициента теплоотдачи"""
    return 'Вт/(м²·ºС/Вт)'


class MyCombo(QComboBox):
    def __init__(self, elements: list):
        super().__init__()
        self.setModel(QStringListModel(elements))
        listview = QListView()
        listview.setWordWrap(True)
        self.setView(listview)
