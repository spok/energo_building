import json
import sys
from PyQt5.QtWidgets import QTableWidgetItem, QFileDialog, QMessageBox, QTreeView, QComboBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QSize
from PyQt5.Qt import QStandardItemModel, QStandardItem
from PyQt5.QtGui import QTextCursor
from func import to_float, to_int, load_excel, MyCombo
from construction_class.building import Building
from construction_class.construction import Construction
from construction_class.windows import Windows
from construction_class.doors import Doors
from construction_class.ground import Grounds
import gui_form
import form_cities
import form_constructions
import form_one_construction
import form_windows
import form_doors
import form_grounds
import form_specif


class MyWindow(QtWidgets.QMainWindow, QtWidgets.QWidget, gui_form.Ui_MainWindow):
    osn_ver_headers = ["Город расположения здания", "Тип здания", "Отапливаемый объем", "Этажность",
                       "Общая площадь здания", "Расчетная площадь", "", "Высота здания",
                       "Температура внутреннего воздуха", "Относительная влажность", "Условия экспплуатации",
                       'Город для расчета солнечной энергии', 'Широта города', 'Количество жильцов, чел.',
                       'Год разработки проекта', 'Регулирование подачи тепла в здание',
                       'Объем лестнично-лифтового узла'
                       ]
    cities = []
    name_cities = []
    build = Building()
    filename = ''

    def __init__(self):
        # Инициализация родителей
        super().__init__()
        self.setupUi(self)
        for i in range(self.tabWidget.count()):
            self.tabWidget.setTabVisible(i, False)
        self.label.setMaximumSize(QSize(16777215, 20))
        # настройка таблицы основных параметров здания
        tab_row = len(self.osn_ver_headers)
        self.tab_osn.setColumnCount(2)
        self.tab_osn.setRowCount(tab_row)
        self.tab_osn.setMaximumHeight(int(tab_row*self.tab_osn.rowHeight(0))+10)
        self.tab_osn.setVerticalHeaderLabels(self.osn_ver_headers)
        self.tab_osn.horizontalHeader().setVisible(False)
        self.tab_osn.setColumnWidth(0, 200)
        self.tab_osn.setColumnWidth(1, 20)
        for i in range(0, tab_row):
            self.tab_osn.setItem(i, 0, QTableWidgetItem())
            self.tab_osn.setItem(i, 1, QTableWidgetItem())
        # список с типами здания
        self.combo_typ = MyCombo(Building.typ_buildings)
        self.tab_osn.setCellWidget(1, 0, self.combo_typ)
        # настройка списка с городами
        self.combo_cities = QtWidgets.QComboBox()
        self.tab_osn.setCellWidget(0, 0, self.combo_cities)
        # добавление кнопки для открытия окна с городами
        self.show_cities = QtWidgets.QPushButton('...')
        self.cities = load_excel()
        for i in self.cities:
            self.name_cities.append(i[0])
            self.combo_cities.addItem(i[0], i)
        completer = QtWidgets.QCompleter(self.name_cities)
        self.combo_cities.setCompleter(completer)
        self.tab_osn.setCellWidget(0, 1, self.show_cities)
        # в столбце с кнопкой убираем режим редактирования ячеек
        for i in range(1, self.tab_osn.rowCount()):
            cell_item = self.tab_osn.item(i, 1)
            if cell_item:
                cell_item.setFlags(cell_item.flags() ^ QtCore.Qt.ItemIsEditable)
        # Список с условиями эксплуатации
        self.combo_ekspl = QtWidgets.QComboBox()
        self.combo_ekspl.addItems(['А', 'Б'])
        self.combo_ekspl.setCurrentIndex(0)
        self.tab_osn.setCellWidget(10, 0, self.combo_ekspl)
        # список с городом для расчета солнечной радиации
        self.combo_solar_siti = QtWidgets.QComboBox()
        self.combo_solar_siti.addItems(self.build.solar_citi_dict.keys())
        self.tab_osn.setCellWidget(11, 0, self.combo_solar_siti)
        # список с широтой размещения города
        self.combo_latitude = QtWidgets.QComboBox()
        s = [str(x) for x in self.build.latitude_list]
        self.combo_latitude.addItems(s)
        self.tab_osn.setCellWidget(12, 0, self.combo_latitude)
        # список с системой регулирования подачи тепла
        self.combo_regular = MyCombo(Building.typ_regular)
        self.tab_osn.setCellWidget(15, 0, self.combo_regular)

        # настройка дерева
        self.tree.setHeaderHidden(True)
        treeModel = QStandardItemModel()
        rootNode = treeModel.invisibleRootItem()
        base = QStandardItem('Основные сведения')
        norm = QStandardItem('Нормативные требования')
        self.constructions_node = QStandardItem('Конструкции')
        spec = QStandardItem('Теплофизическая характеристика')
        result = QStandardItem('Удельный расход тепловой энергии')
        pasport = QStandardItem('Энергетический паспорт')
        class_energo = QStandardItem('Класс энергоэффективности')
        rootNode.appendRow(base)
        rootNode.appendRow(norm)
        rootNode.appendRow(self.constructions_node)
        rootNode.appendRow(spec)
        rootNode.appendRow(result)
        rootNode.appendRow(pasport)
        rootNode.appendRow(class_energo)
        self.tree.setModel(treeModel)
        self.tree.expandAll()

        # создаем таблицу с конструкциями
        self.table_cons = form_constructions.Constructions(self.tab3, tree_nod=self.constructions_node,
                                                           building=self.build)

        # создаем форму для многослойных конструкций
        self.tab_one_constr = form_one_construction.ConstructionLayer(self.vbox2, self.build)

        # создание формы для окон и витражей
        self.tab_windows = form_windows.Windows(self.vbox3)

        # создание формы для дверей и ворот
        self.tab_doors = form_doors.Doors(self.vbox4)

        # создание формы для конструкций в грунте
        self.tab_grounds = form_grounds.Grounds(self.vbox5)

        # создание формы для теплофизической характеристики
        self.tab_specif = form_specif.Specifications(self.vbox6)

        # Обработка сигналов
        self.get_data_building()
        self.but_save.clicked.connect(self.save_json)
        self.but_save_as.clicked.connect(self.save_as_json)
        self.but_load.clicked.connect(self.load_from_json)
        self.combo_typ.activated.connect(self.get_change)
        self.combo_cities.activated.connect(self.get_change)
        self.combo_ekspl.activated.connect(self.get_change)
        self.combo_solar_siti.activated.connect(self.get_change)
        self.combo_latitude.activated.connect(self.get_change)
        self.show_cities.clicked.connect(self.view_cities)
        self.tab_osn.itemChanged.connect(self.check_input)
        self.tree.clicked.connect(self.getTreeValue)
        self.get_change()
        self.bild_tree()
        self.tabWidget.setCurrentIndex(0)

    def bild_tree(self):
        """Построение структуры конструкций здания"""
        # очистка конструкции в дереве проекта
        self.constructions_node.removeRows(0, self.constructions_node.rowCount())
        for i, elem in enumerate(self.build.constructions):
            if type(elem) is Construction:
                elem_nod = QStandardItem(elem.get_construction_name())
                elem_nod.setData(elem)
                self.constructions_node.appendRow(elem_nod)
            if type(elem) is Windows:
                elem_nod = QStandardItem(elem.get_construction_name())
                elem_nod.setData(elem)
                self.constructions_node.appendRow(elem_nod)
            if type(elem) is Doors:
                elem_nod = QStandardItem(elem.get_construction_name())
                elem_nod.setData(elem)
                self.constructions_node.appendRow(elem_nod)
            if type(elem) is Grounds:
                elem_nod = QStandardItem(elem.get_construction_name())
                elem_nod.setData(elem)
                self.constructions_node.appendRow(elem_nod)

    def getTreeValue(self, val):
        if val.data() == "Основные сведения":
            self.tabWidget.setCurrentIndex(0)
        elif val.data() == "Нормативные требования":
            self.tabWidget.setCurrentIndex(1)
        elif val.data() == "Конструкции":
            self.tabWidget.setCurrentIndex(2)
            self.table_cons.draw_table()
        elif val.parent().data() == "Конструкции":
            # Отображение вкладки с составом конструкции
            if self.build.constructions[val.row()].typ in ['Наружная стена', 'Покрытие', 'Чердачное перекрытие',
                                                        'Перекрытие над холодным подвалом', 'Перекрытие над проездом']:
                self.tabWidget.setCurrentIndex(3)
                self.tab_one_constr.build_table(constr=self.build.constructions[val.row()], norm=self.build.norm)
            elif self.build.constructions[val.row()].typ in ['Окна', 'Витражи', 'Фонари']:
                self.tabWidget.setCurrentIndex(4)
                self.tab_windows.build_table(build=self.build, index=val.row())
            elif self.build.constructions[val.row()].typ in ['Двери', 'Ворота']:
                self.tabWidget.setCurrentIndex(5)
                self.tab_doors.build_table(build=self.build, index=val.row())
            elif self.build.constructions[val.row()].typ == 'Конструкция в контакте с грунтом':
                self.tabWidget.setCurrentIndex(6)
                self.tab_grounds.build_table(build=self.build, index=val.row())
        elif val.data() == "Теплофизическая характеристика":
            self.tabWidget.setCurrentIndex(7)
            self.tab_specif.draw_specif(building=self.build)
        elif val.data() == "Удельный расход тепловой энергии":
            self.tabWidget.setCurrentIndex(7)
            self.tab_specif.draw_result(building=self.build)
        elif val.data() == "Энергетический паспорт":
            self.tabWidget.setCurrentIndex(7)
            self.tab_specif.draw_pasport(building=self.build)
        elif val.data() == "Класс энергоэффективности":
            self.tabWidget.setCurrentIndex(7)
            self.tab_specif.draw_class(building=self.build)

    def set_data_building(self):
        """Установка параметров здания из элементов формы"""
        self.tab_osn.blockSignals(True)
        self.get_change()
        self.build.v_heat = to_float(self.tab_osn.item(2, 0).text())
        self.build.floors = to_int(self.tab_osn.item(3, 0).text())
        self.build.area_all = to_float(self.tab_osn.item(4, 0).text())
        self.build.area_calc = to_float(self.tab_osn.item(5, 0).text())
        self.build.area_live = to_float(self.tab_osn.item(6, 0).text())
        self.build.height_building = to_float(self.tab_osn.item(7, 0).text())
        self.build.t_int = to_float(self.tab_osn.item(8, 0).text())
        self.build.w_int = to_float(self.tab_osn.item(9, 0).text())
        self.build.tenants = to_int(self.tab_osn.item(13, 0).text())
        self.build.year = to_int(self.tab_osn.item(14, 0).text())
        self.build.v_llu = to_float(self.tab_osn.item(16, 0).text())
        self.tab_osn.blockSignals(False)

    def get_data_building(self):
        """Заполнение элементов формы в соответствии с данными"""
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
        self.tab_osn.setItem(13, 0, QTableWidgetItem(str(self.build.tenants)))
        self.tab_osn.setItem(14, 0, QTableWidgetItem(str(self.build.year)))
        self.tab_osn.setItem(16, 0, QTableWidgetItem(str(self.build.v_llu)))
        # вывод условия эксплуатации
        self.combo_ekspl.setCurrentText(self.build.ekspl)
        # вывод города для солнечной радиации
        self.combo_solar_siti.setCurrentText(self.build.solar_citi)
        # вывод широты
        self.combo_latitude.setCurrentText(str(self.build.latitude))
        # вывод типа авторегулирования на вводе
        self.combo_regular.setCurrentText(self.build.regular)

    def check_input(self):
        """Проверка вводимых данных в ячейках таблицы"""
        cur_row = self.tab_osn.currentRow()
        cur_str = self.tab_osn.item(cur_row, 0).text()
        if cur_str:
            if cur_row == 3:
                try:
                    self.build.floors = int(cur_str)
                except:
                    self.build.floors = 0
                    print('Некорректно введено количество этажей')
            else:
                try:
                    n = float(cur_str)
                except:
                    print(f'Некорректно введено значение в строке {cur_row}')
        self.set_data_building()
        self.build.calc()
        self.out_norm()

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
            self.osn_ver_headers[13] = 'Количество жильцов'
            self.osn_ver_headers[16] = 'Объем лестнично-лифтового узла'
        else:
            self.osn_ver_headers[5] = 'Расчетная площадь'
            self.osn_ver_headers[6] = ''
            self.osn_ver_headers[13] = 'Количество работников'
            self.osn_ver_headers[16] = 'Объем приточного воздуха'
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
        # при изменении широты
        self.build.latitude = int(self.combo_latitude.currentText())
        # при изменении широты
        self.build.latitude = int(self.combo_latitude.currentText())
        # при изменении авторегулирования подачи тепла
        self.build.regular = self.combo_regular.currentText()
        self.tab_osn.blockSignals(False)
        # пересчет после изменений параметров
        if not self.tab_osn.signalsBlocked():
            self.build.calc()
            self.out_norm()

    def out_norm(self):
        """Вывод расчета нормативных требований"""
        # self.text_norm.clear()
        self.build.get_norm_html(self.text_norm)
        # перенос в начало текста
        # cursor = self.text_norm.textCursor()
        # cursor.movePosition(QTextCursor.Start)
        # self.text_norm.setTextCursor(cursor)

    def save_json(self):
        """Сохранение данных в формате json"""
        if self.filename == '':
            name = QFileDialog.getSaveFileName(self, caption="Save data building", filter="Data Files (*.json)")
            if name[0] != '':
                self.filename = name[0]
        if self.filename != '':
            save_dict = self.build.get_dict()
            with open(self.filename, 'w') as f:
                json.dump(save_dict, f, indent=2)

    def save_as_json(self):
        name = QFileDialog.getSaveFileName(self, caption="Save data building", filter="Data Files (*.json)")
        if name[0] != '':
            self.filename = name[0]
            save_dict = self.build.get_dict()
            with open(self.filename, 'w') as f:
                json.dump(save_dict, f, indent=2)

    def load_from_json(self):
        """Чтение данных из файла json"""
        name = QFileDialog.getOpenFileName(self, caption="Load data building", filter="Data Files (*.json)")
        if name[0] != '':
            self.filename = name[0]
            with open(self.filename, 'r') as f:
                load_dict = json.load(f)
                self.build.data_from_dict(load_dict)
                self.tab_osn.blockSignals(True)
                self.get_data_building()
                self.get_change()
                self.bild_tree()
                self.build.calc()
                self.tab_osn.blockSignals(False)
                self.tabWidget.setCurrentIndex(0)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
