from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QComboBox, QPushButton, QMessageBox, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.Qt import QStandardItem
from construction import Construction, Building
from copy import copy


class Constructions(QWidget):
    hor_headers = ['Тип конструкции', 'Название конструкции', 'Ro', '', '', '']

    def __init__(self, parent=None, tree_nod=None, constr=None):
        super().__init__()
        self.nod_constr = tree_nod
        self.list_constr = constr
        vbox_tab2 = QVBoxLayout(parent)
        self.table_cons = QTableWidget()
        self.table_cons.setColumnCount(6)

        self.table_cons.setHorizontalHeaderLabels(self.hor_headers)
        self.table_cons.horizontalHeader().setVisible(True)
        self.table_cons.setColumnWidth(0, 250)
        self.table_cons.setColumnWidth(1, 200)
        self.table_cons.setColumnWidth(2, 50)
        self.table_cons.setColumnWidth(3, 30)
        self.table_cons.setColumnWidth(4, 30)
        self.table_cons.setColumnWidth(5, 30)
        self.table_cons.setRowCount(1)
        for i in range(self.table_cons.columnCount()):
            self.table_cons.horizontalHeaderItem(i).setTextAlignment(Qt.AlignHCenter)
        vbox_tab2.addWidget(self.table_cons)
        self.table_cons.itemChanged.connect(self.set_construction_name)

    def draw_table(self):
        """перерисовка таблицы в соответствии с структурой конструкций"""
        self.table_cons.blockSignals(True)
        self.table_cons.clear()
        self.table_cons.setHorizontalHeaderLabels(self.hor_headers)
        if len(self.list_constr) > 0:
            self.table_cons.setRowCount(len(self.list_constr))
            # очистка конструкции в дереве проекта
            self.nod_constr.removeRows(0, self.nod_constr.rowCount())
            for i, elem in enumerate(self.list_constr):
                if type(elem) is Construction:
                    # добавление элемента с списком конструкций
                    elem_typ = QComboBox()
                    elem_typ.addItems(Building.typ_constr)
                    elem_typ.setCurrentText(elem.typ)
                    self.table_cons.setCellWidget(i, 0,  elem_typ)
                    elem_typ.activated.connect(self.change_typ_constr)
                    # добавление элемента с названием конструкции
                    self.table_cons.setItem(i, 1, QTableWidgetItem(elem.name))
                    # добавление элемента с сопротивлением конструкции
                    el = QTableWidgetItem(str(elem.ro))
                    el.setTextAlignment(Qt.AlignRight)
                    el.setTextAlignment(Qt.AlignVCenter)
                    self.table_cons.setItem(i, 2, el)
                    # добавление кнопки для добавления конструкции
                    el_but = QPushButton()
                    el_but.setToolTip('Добавить пустую конструкцию')
                    el_icon = QIcon('add.png')
                    el_but.setIcon(el_icon)
                    el_but.clicked.connect(self.add_constr)
                    self.table_cons.setCellWidget(i, 3, el_but)
                    # добавление кнопки для копирования конструкции
                    el_but = QPushButton()
                    el_but.setToolTip('Сделать копию конструкции')
                    el_icon = QIcon('copy.png')
                    el_but.setIcon(el_icon)
                    el_but.clicked.connect(self.copy_constr)
                    self.table_cons.setCellWidget(i, 4, el_but)
                    # добавление кнопки для удаления конструкции
                    el_but = QPushButton()
                    el_but.setToolTip('Удалить конструкцию')
                    el_icon = QIcon('minus.png')
                    el_but.setIcon(el_icon)
                    el_but.clicked.connect(self.del_constr)
                    self.table_cons.setCellWidget(i, 5, el_but)
                    # добавление элемента в дерево конструкций
                    elem_nod = QStandardItem(elem.get_construction_name())
                    elem_nod.setData(elem)
                    self.nod_constr.appendRow(elem_nod)
        self.table_cons.blockSignals(False)

    def set_construction_name(self):
        """Смена названия конструкции"""
        index = self.table_cons.currentRow()
        self.list_constr[index].name = self.table_cons.item(index, 1).text()
        node = self.nod_constr.child(index)
        node.setText(self.list_constr[index].get_construction_name())

    def change_typ_constr(self):
        """Смена типа конструкции в таблице"""
        index = self.table_cons.currentRow()
        elem = self.table_cons.cellWidget(index, 0)
        self.list_constr[index].typ = elem.currentText()
        node = self.nod_constr.child(index)
        node.setText(self.list_constr[index].get_construction_name())

    def add_constr(self):
        """Добавление пустой конструкции под активной конструкции"""
        cur = self.table_cons.currentRow()
        elem = Construction()
        elem.typ = 'Наружная стена'
        if cur < (self.table_cons.rowCount() - 1):
            self.list_constr.insert(cur + 1, elem)
        else:
            self.list_constr.append(elem)
        self.draw_table()

    def copy_constr(self):
        """Создание копии активной конструкции"""
        cur = self.table_cons.currentRow()
        elem = copy(self.list_constr[cur])
        if cur < (self.table_cons.rowCount() - 1):
            self.list_constr.insert(cur + 1, elem)
        else:
            self.list_constr.append(elem)
        self.draw_table()

    def del_constr(self):
        """Удаление текущей конструкции"""
        if self.table_cons.rowCount() > 1:
            cur = self.table_cons.currentRow()
            try:
                self.list_constr.pop(cur)
            except ValueError:
                QMessageBox.about(self, "Ошибка", "Ошибка при удалении конструкции")
            self.draw_table()
        else:
            QMessageBox.about(self, "Ошибка", "Должна остаться одна конструкция")
