from openpyxl import load_workbook

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
