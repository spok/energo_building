import os
import sys
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QFileDialog, QInputDialog, QMessageBox, QTreeView
from PyQt5 import QtCore, Qt, QtGui, QtWidgets
from PyQt5.Qt import QStandardItemModel, QStandardItem
import func
from construction import Building
import gui_form
import form_cities
import form_constructions


class MyWindow(QtWidgets.QMainWindow, QtWidgets.QWidget, gui_form.Ui_MainWindow):
    osn_ver_headers = ["Город расположения здания", "Тип здания", "Отапливаемый объем", "Этажность",
                       "Общая площадь здания", "Расчетная площадь", "", "Высота здания",
                       "Температура внутреннего воздуха", "Относительная влажность", "Условия экспплуатации"
                       ]
    cities = []
    name_cities = []
    build = Building()

    def __init__(self):
        # Инициализация родителей
        super().__init__()
        self.setupUi(self)
        # настройка таблицы основных параметров здания
        tab_row = 11
        self.tab_osn.setColumnCount(2)
        self.tab_osn.setRowCount(tab_row)
        self.tab_osn.setMaximumHeight(int(tab_row*self.tab_osn.rowHeight(0))+10)
        self.tab_osn.setVerticalHeaderLabels(self.osn_ver_headers)
        self.tab_osn.horizontalHeader().setVisible(False)
        self.tab_osn.setColumnWidth(0, 200)
        self.tab_osn.setColumnWidth(1, 20)
        for i in range(0, 10):
            self.tab_osn.setItem(i, 0, QTableWidgetItem())
            self.tab_osn.setItem(i, 1, QTableWidgetItem())
        # список с типами здания
        self.combo_typ = QtWidgets.QComboBox()
        self.combo_typ.addItems(Building.typ_buildings)
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
        for i in range(1, self.tab_osn.rowCount()-1):
            cell_item = self.tab_osn.item(i, 1)
            if cell_item:
                cell_item.setFlags(cell_item.flags() ^ QtCore.Qt.ItemIsEditable)
        # Список с условиями эксплуатации
        self.combo_ekspl = QtWidgets.QComboBox()
        self.combo_ekspl.addItems(['А', 'Б'])
        self.combo_ekspl.setCurrentIndex(0)
        self.tab_osn.setCellWidget(10, 0, self.combo_ekspl)
        # создаем таблицу с конструкциями
        self.table_cons = form_constructions.Constructions(self.tab3)
        self.table_cons.list_constr = self.build.constructions
        self.table_cons.draw_table()
        # таблица с нормативными значениями
        self.tab_norm.setColumnCount(4)
        hor_headers = ['Тип конструкции', 'Сопротивление Rтр', 'Коэффициент', 'Сопротивление Rmin']
        self.tab_norm.setHorizontalHeaderLabels(hor_headers)
        self.tab_norm.setColumnWidth(0, 250)
        self.tab_norm.setColumnWidth(1, 120)
        self.tab_norm.setColumnWidth(2, 120)
        self.tab_norm.setColumnWidth(3, 150)

        # настройка дерева
        self.tree.setHeaderHidden(True)
        treeModel = QStandardItemModel()
        rootNode = treeModel.invisibleRootItem()
        base = QStandardItem('Основные сведения')
        norm = QStandardItem('Нормативные требования')
        constr = QStandardItem('Конструкции')
        rootNode.appendRow(base)
        rootNode.appendRow(norm)
        rootNode.appendRow(constr)
        self.tree.setModel(treeModel)
        self.tree.expandAll()

        # Обработка сигналов
        self.get_data_building()
        self.combo_typ.activated.connect(self.get_change)
        self.combo_cities.activated.connect(self.get_change)
        self.combo_ekspl.activated.connect(self.get_change)
        self.show_cities.clicked.connect(self.view_cities)
        self.tab_osn.itemChanged.connect(self.check_input)
        self.tree.clicked.connect(self.getTreeValue)
        self.get_change()


    def bild_tree(self):
        """Построение структуры конструкций здания"""
        pass

    def getTreeValue(self, val):
        if val.data() == "Основные сведения":
            self.tabWidget.setCurrentIndex(0)
        elif val.data() == "Нормативные требования":
            self.tabWidget.setCurrentIndex(1)
        elif val.data() == "Конструкции":
            self.tabWidget.setCurrentIndex(2)

    def set_data_building(self):
        """Установка параметров здания из элементов формы"""
        self.tab_osn.blockSignals(True)
        self.change_cities()
        self.change_typ_building()
        self.build.v_heat = float(self.tab_osn.item(2, 0))
        self.build.floors = int(self.tab_osn.item(3, 0))
        self.build.area_all = float(self.tab_osn.item(4, 0))
        self.build.area_calc = float(self.tab_osn.item(5, 0))
        self.build.area_live = float(self.tab_osn.item(6, 0))
        self.build.height_building = float(self.tab_osn.item(7, 0))
        self.build.t_int = float(self.tab_osn.item(8, 0))
        self.build.w_int = float(self.tab_osn.item(9, 0))
        self.change_ekspl()
        self.tab_osn.blockSignals(False)

    def get_data_building(self):
        """Заполнение элементов в соответствии с данными"""
        # Изменение типа здания
        self.combo_typ.setCurrentText(self.build.typ)
        # Изменение текущего города
        self.combo_cities.setCurrentText(self.build.citi)
        # Вывод параметров здания
        self.tab_osn.setItem(2, 0, QTableWidgetItem(str(self.build.v_heat)))
        self.tab_osn.setItem(3, 0, QTableWidgetItem(str(self.build.floors)))
        self.tab_osn.setItem(4, 0, QTableWidgetItem(str(self.build.area_all)))
        self.tab_osn.setItem(5, 0, QTableWidgetItem(str(self.build.area_calc)))
        self.tab_osn.setItem(6, 0, QTableWidgetItem(str(self.build.area_live)))
        self.tab_osn.setItem(7, 0, QTableWidgetItem(str(self.build.height_building)))
        self.tab_osn.setItem(8, 0, QTableWidgetItem(str(self.build.t_int)))
        self.tab_osn.setItem(9, 0, QTableWidgetItem(str(self.build.w_int)))
        # вывод условия эксплуатации
        self.combo_ekspl.setCurrentText(self.build.ekspl)

    def check_input(self):
        """Проверка вводимых данных в ячейках"""
        self.error_mes.clear()
        cur_row = self.tab_osn.currentRow()
        cur_str = self.tab_osn.item(cur_row, 0)
        if cur_str:
            if cur_row == 3:
                try:
                    self.build.floors = int(cur_str)
                except ValueError:
                    self.error_mes.insertPlainText("Количество этажей должно быть целым числом \n")
            else:
                try:
                    n = float(cur_str)
                except ValueError:
                    self.error_mes.insertPlainText(f"Неверные данные для значения: {self.osn_ver_headers[cur_row]} \n")
        self.set_data_building()
        self.calc_norm()

    def view_cities(self):
        """Отображение окна с климатическими параметрами городов"""
        dialog = form_cities.ShowCities(self)
        dialog.resize(800, 600)
        dialog.table_show(self.cities)
        dialog.exec_()
        if dialog.table.currentRow() > 0:
            self.combo_cities.setCurrentIndex(dialog.table.currentRow())
        else:
            self.combo_cities.setCurrentIndex(0)

    def get_change(self):
        """Изменние обозначения строк в зависимости от типа здания"""
        self.tab_osn.blockSignals(True)
        # при изменении типа здания
        cur_typ = self.combo_typ.currentText()
        if cur_typ == "Жилое" or cur_typ == "Общежитие":
            self.osn_ver_headers[5] = 'Общая площадь квартир'
            self.osn_ver_headers[6] = 'Жилая площадь'
        else:
            self.osn_ver_headers[5] = 'Расчетная площадь'
            self.osn_ver_headers[6] = ''
        self.tab_osn.setVerticalHeaderLabels(self.osn_ver_headers)
        self.build.typ = cur_typ
        # при изменении города
        cur_citi = self.combo_cities.currentData()
        self.build.citi = cur_citi[0]
        self.build.t_nhp = cur_citi[4]
        if self.build.typ == "Детское учреждение":
            self.build.t_ot = cur_citi[13]
            self.build.z_ot = cur_citi[12]
        else:
            self.build.t_ot = cur_citi[11]
            self.build.z_ot = cur_citi[10]
        # при изменении условий эксплуатаций
        self.build.ekspl = self.combo_ekspl.currentText()
        self.tab_osn.blockSignals(False)
        # пересчет после изменений параметров
        if not self.tab_osn.signalsBlocked():
            self.build.calc()
            self.out_calc_gsop()
            self.out_norm()

    def out_calc_gsop(self):
        """Вывод расчета ГСОП"""
        self.text_gsop.clear()
        s = self.build.get_gsop_text()
        self.text_gsop.insertPlainText(s)

    def out_norm(self):
        self.tab_norm.setRowCount(len(self.build.typ_constr)-1)
        for i, val in enumerate(self.build.norm):
            elem = self.build.norm[val]
            if 'Rtr' in elem:
                self.tab_norm.setItem(i, 0, QTableWidgetItem(elem['name']))
                self.tab_norm.item(i, 0).setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
                self.tab_norm.item(i, 0).setFlags(self.tab_norm.item(i, 0).flags() ^ QtCore.Qt.ItemIsEditable)
                self.tab_norm.setItem(i, 1, QTableWidgetItem(str(elem['Rtr'])))
                self.tab_norm.item(i, 1).setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                self.tab_norm.item(i, 1).setFlags(self.tab_norm.item(i, 1).flags() ^ QtCore.Qt.ItemIsEditable)
                self.tab_norm.setItem(i, 2, QTableWidgetItem(str(elem['mp'])))
                self.tab_norm.item(i, 2).setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                self.tab_norm.item(i, 2).setFlags(self.tab_norm.item(i, 2).flags() ^ QtCore.Qt.ItemIsEditable)
                self.tab_norm.setItem(i, 3, QTableWidgetItem(str(elem['Rmin'])))
                self.tab_norm.item(i, 3).setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                self.tab_norm.item(i, 3).setFlags(self.tab_norm.item(i, 3).flags() ^ QtCore.Qt.ItemIsEditable)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())


