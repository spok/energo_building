from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QComboBox, QPushButton, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.Qt import QStandardItem
from construction_class.building import Building
from func import to_float


class Constructions(QWidget):
    hor_headers = ['Тип конструкции', 'Название конструкции', 'S, м²', 'Ro', 'Назначение', '', '', '']

    def __init__(self, parent=None, tree_nod=None, building=None):
        super().__init__()
        self.nod_constr = tree_nod
        self.building = building
        self.list_constr = building.constructions
        vbox_tab2 = QVBoxLayout(parent)
        self.table_cons = QTableWidget()
        self.table_cons.setColumnCount(8)

        self.table_cons.setHorizontalHeaderLabels(self.hor_headers)
        self.table_cons.horizontalHeader().setVisible(True)
        self.table_cons.setColumnWidth(0, 150)
        self.table_cons.setColumnWidth(1, 150)
        self.table_cons.setColumnWidth(2, 60)
        self.table_cons.setColumnWidth(3, 60)
        self.table_cons.setColumnWidth(4, 150)
        self.table_cons.setColumnWidth(5, 20)
        self.table_cons.setColumnWidth(6, 20)
        self.table_cons.setColumnWidth(7, 20)
        self.table_cons.setRowCount(1)
        for i in range(self.table_cons.columnCount()):
            self.table_cons.horizontalHeaderItem(i).setTextAlignment(Qt.AlignHCenter)
        vbox_tab2.addWidget(self.table_cons)
        self.table_cons.itemChanged.connect(self.get_change)

    def draw_table(self):
        """перерисовка таблицы в соответствии с структурой конструкций"""
        self.table_cons.blockSignals(True)
        self.table_cons.clear()
        self.table_cons.setHorizontalHeaderLabels(self.hor_headers)
        self.building.draw_table(self.table_cons, self.nod_constr)
        # Назначение элементам таблицы обработчики сигналов
        for i in range(self.table_cons.rowCount()):
            # обработчик списка типов конструкций
            elem = self.table_cons.cellWidget(i, 0)
            elem.activated.connect(self.change_typ)
            # обработчик списка назначения конструкций
            elem = self.table_cons.cellWidget(i, 4)
            elem.activated.connect(self.get_change)
            # обработчик кнопки добавить
            elem = self.table_cons.cellWidget(i, 5)
            elem.clicked.connect(self.add_constr)
            # обработки кнопки копировать
            elem = self.table_cons.cellWidget(i, 6)
            elem.clicked.connect(self.copy_constr)
            # обработки кнопки удалить
            elem = self.table_cons.cellWidget(i, 7)
            elem.clicked.connect(self.del_constr)
        self.table_cons.blockSignals(False)

    def get_change(self):
        """Получение изменений в таблице"""
        index = self.table_cons.currentRow()
        if index > -1:
            # Смена названия конструкции
            self.list_constr[index].name = self.table_cons.item(index, 1).text()
            self.nod_constr.child(index).setText(self.list_constr[index].get_construction_name())
            # Получение площади конструкции
            self.list_constr[index].area = to_float(self.table_cons.item(index, 2).text())
            # Смена назначения конструкции в таблице
            new_typ = self.table_cons.cellWidget(index, 4).currentText()
            self.building.change_purpose(new_typ=new_typ, index=index)

    def change_typ(self):
        """Смена типа конструкции с полным удалением предыдущей информации"""
        index = self.table_cons.currentRow()
        # Смена типа конструкции в таблице
        new_typ = self.table_cons.cellWidget(index, 0).currentText()
        self.building.change_typ(new_typ=new_typ, index=index)
        node = self.nod_constr.child(index)
        node.setText(self.list_constr[index].get_construction_name())

    def add_constr(self):
        """Добавление пустой конструкции"""
        cur = self.table_cons.currentRow()
        self.building.add_construction(typ='Наружная стена', name='', index=cur)
        self.draw_table()

    def copy_constr(self):
        """Создание копии активной конструкции"""
        cur = self.table_cons.currentRow()
        self.building.copy_construction(index=cur)
        self.draw_table()

    def del_constr(self):
        """Удаление текущей конструкции"""
        cur = self.table_cons.currentRow()
        self.building.del_construction(cur)
        self.draw_table()
