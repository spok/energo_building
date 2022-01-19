import os
import sys
from PyQt5.QtWidgets import QTableWidgetItem, QFileDialog, QInputDialog, QMessageBox, QTreeView
from PyQt5 import QtCore, Qt, QtGui, QtWidgets
from PyQt5.Qt import QStandardItemModel, QStandardItem

import func
import construction
import gui_form
import form_cities


class MyWindow(QtWidgets.QMainWindow, QtWidgets.QWidget, gui_form.Ui_MainWindow):
    osn_ver_headers = ["Город расположения здания", "Тип здания", "Отапливаемый объем", "Этажность",
                       "Общая площадь здания", "Расчетная площадь", "", "Высота здания",
                       "Температура внутреннего воздуха", "Относительная влажность"
                       ]
    typ_buildings = ["Жилое", "Лечебно-профилактическое", "Детское учреждение", "Школа", "Интернат", "Гостиница",
                     "Общежитие", "Общественное", "Административное", "Сервисного обслуживания", "Бытовое",
                     "Производственное и другое с влажным или мокрым режимом эксплуатации",
                     "Производственное с сухим и нормальным режимом эксплуатации"]
    cities = []
    name_cities = []
    build = construction.Building()

    def __init__(self):
        # Инициализация родителей
        super().__init__()
        self.setupUi(self)
        # настройка таблицы основных параметров здания
        self.tab_osn.setColumnCount(2)
        self.tab_osn.setRowCount(10)
        self.tab_osn.setVerticalHeaderLabels(self.osn_ver_headers)
        self.tab_osn.horizontalHeader().setVisible(False)
        self.tab_osn.setColumnWidth(0, 200)
        self.tab_osn.setColumnWidth(1, 20)
        for i in range(0, 10):
            self.tab_osn.setItem(i, 0, QTableWidgetItem())
            self.tab_osn.setItem(i, 1, QTableWidgetItem())
        # список с типами здания
        self.combo_typ = QtWidgets.QComboBox()
        self.combo_typ.addItems(self.typ_buildings)
        self.tab_osn.setCellWidget(1, 0, self.combo_typ)
        # настройка списка с городами
        self.combo_cities = QtWidgets.QComboBox()
        self.tab_osn.setCellWidget(0, 0, self.combo_cities)
        self.show_cities = QtWidgets.QPushButton('...')
        self.cities = func.load_excel('cities.xlsx')
        for i in self.cities:
            self.name_cities.append(i[0])
            self.combo_cities.addItem(i[0], i)
        completer = QtWidgets.QCompleter(self.name_cities)
        self.combo_cities.setCompleter(completer)
        # self.combo_cities.setEditable(True)
        self.tab_osn.setCellWidget(0, 1, self.show_cities)
        # в столбце с кнопкой убираем режим редактирования ячеек
        for i in range(1, 10):
            cell_item = self.tab_osn.item(i, 1)
            if cell_item:
                cell_item.setFlags(cell_item.flags() ^ QtCore.Qt.ItemIsEditable)

        # настройка дерева
        self.tree.setHeaderHidden(True)
        treeModel = QStandardItemModel()
        rootNode = treeModel.invisibleRootItem()
        base = QStandardItem('Основные сведения')
        constr = QStandardItem('Конструкции')
        new_constr = QStandardItem('Наружная стена')
        constr.appendRow(new_constr)
        new_constr = QStandardItem('Наружная стена')
        constr.appendRow(new_constr)

        rootNode.appendRow(base)
        rootNode.appendRow(constr)
        self.tree.setModel(treeModel)
        self.tree.expandAll()

        # Обработка сигналов
        self.get_data_building()
        self.combo_typ.activated.connect(self.change_typ_building)
        self.combo_cities.activated.connect(self.change_cities)
        self.show_cities.clicked.connect(self.view_cities)
        self.tab_osn.itemChanged.connect(self.check_input)
        self.tree.clicked.connect(self.getTreeValue)
        self.change_typ_building()
        self.change_cities()

    def getTreeValue(self, val):
        if val.data() == "Основные сведения":
            self.tabWidget.setCurrentIndex(0)
        elif val.data() == "Конструкции" or val.parent().data() == "Конструкции":
            self.tabWidget.setCurrentIndex(1)

    def get_data_building(self):
        """Заполнение элементов в соответствии с данными"""
        # Изменение текущего города
        self.combo_cities.setCurrentText(self.build.citi)
        # Изменение типа здания
        self.combo_typ.setCurrentText(self.build.typ)
        # Вывод параметров здания
        self.tab_osn.setItem(2, 0, QTableWidgetItem(str(self.build.v_heat)))
        self.tab_osn.setItem(3, 0, QTableWidgetItem(str(self.build.floors)))
        self.tab_osn.setItem(4, 0, QTableWidgetItem(str(self.build.area_all)))
        self.tab_osn.setItem(5, 0, QTableWidgetItem(str(self.build.area_calc)))
        self.tab_osn.setItem(6, 0, QTableWidgetItem(str(self.build.area_live)))
        self.tab_osn.setItem(7, 0, QTableWidgetItem(str(self.build.height_building)))
        self.tab_osn.setItem(8, 0, QTableWidgetItem(str(self.build.t_int)))
        self.tab_osn.setItem(9, 0, QTableWidgetItem(str(self.build.w_int)))

    def check_input(self):
        """Проверка вводимых данных в ячейках"""
        self.error_mes.clear()
        for i in range(2, 11):
            item = self.tab_osn.item(i, 0)
            if item:
                s = func.to_dot(item.text())
                n = 0
                if s:
                    try:
                        n = float(s)
                    except ValueError:
                        self.error_mes.insertPlainText(f"Неверные данные для значения: {self.osn_ver_headers[i]} \n")
                if i == 2:
                    self.build.v_heat = n
                elif i == 3:
                    try:
                        self.build.floors = int(n)
                    except ValueError:
                        self.error_mes.insertPlainText("Количество этажей должно быть целым числом \n")
                elif i == 4:
                    self.build.area_all = n
                elif i == 5:
                    self.build.area_calc = n
                elif i == 6:
                    self.build.area_live = n
                elif i == 7:
                    self.build.height_building = n
                elif i == 8:
                    self.build.t_int = n
                elif i == 9:
                    self.build.w_int = n
        self.calc_norm()

    def view_cities(self):
        """Отображение окна с климатическими параметрами городов"""
        dialog = form_cities.ShowCities(self)
        dialog.resize(800, 600)
        dialog.table_show(self.cities)
        dialog.exec_()
        self.combo_cities.setCurrentIndex(dialog.table.currentRow())

    def change_cities(self):
        cur_citi = self.combo_cities.currentData()
        self.build.citi = cur_citi[0]
        self.build.t_nhp = cur_citi[4]
        if self.build.typ == "Детское учреждение":
            self.build.t_ot = cur_citi[13]
            self.build.z_ot = cur_citi[12]
        else:
            self.build.t_ot = cur_citi[11]
            self.build.z_ot = cur_citi[10]
        self.calc_norm()

    def change_typ_building(self):
        """Изменние обозначения строк в зависимости от типа здания"""
        cur_typ = self.combo_typ.currentText()
        if cur_typ == "Жилое" or cur_typ == "Общежитие":
            self.osn_ver_headers[5] = 'Общая площадь квартир'
            self.osn_ver_headers[6] = 'Жилая площадь'
        else:
            self.osn_ver_headers[5] = 'Расчетная площадь'
            self.osn_ver_headers[6] = ''
        self.tab_osn.setVerticalHeaderLabels(self.osn_ver_headers)
        self.build.typ = cur_typ
        self.calc_norm()

    def calc_norm(self):
        """Расчет нормативов"""
        self.text_norm.clear()
        self.build.gsop = (self.build.t_int - self.build.t_ot) * self.build.z_ot
        s = "Градусо-сутки отопительного периода (ГСОП) определяется по формуле 5.2 СП 50.13330.2012 \n"
        s += "ГСОП = (tв - tн)*zот\n"
        s += f"где tв = {self.build.t_int} °С - температура внутреннего воздуха помещений здания (определяется по ГОСТ 30494-96);\n"
        s += f"tот = {self.build.t_ot} °С – средняя температура наружного воздуха отопительного периода "
        s += f"для г.{self.build.citi}, для периода со средней суточной температурой наружного воздуха не более "
        if self.build.typ == "Детское учреждение":
            s += f"{10} °С, определяется по табл. 1 СП 131.13330.2012; \n"
        else:
            s += f"{8} °С, определяется по табл. 1 СП 131.13330.2012; \n"
        s += f"zот = {self.build.z_ot} °С – продолжительность отопительного периода "
        s += f"для г.{self.build.citi}, для периода со средней суточной температурой наружного воздуха не более "
        if self.build.typ == "Детское учреждение":
            s += f"{10} °С, определяется по табл. 1 СП 131.13330.2012; \n"
        else:
            s += f"{8} °С, определяется по табл. 1 СП 131.13330.2012; \n"
        s += f"ГСОП = ({self.build.t_int} - {self.build.t_ot})*{self.build.z_ot} = {self.build.gsop} ºС·сут\n"
        self.text_norm.insertPlainText(s)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())


