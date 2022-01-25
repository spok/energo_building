from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QComboBox, QLabel, QLineEdit, \
    QTextEdit, QPushButton, QMessageBox, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from construction import Construction, Layer
from func import to_dot


class ConstructionLayer(QWidget):
    typ_surface_int = ['стен, полов, гладких потолков, потолков с выступающими ребрами при отношении высоты h ребер к расстоянию а между гранями соседних ребер h/a < 0,3',
                       'потолков с выступающими ребрами при отношении h/a > 0,3', 'окон', 'зенитных фонарей']
    typ_surface_ext = ['наружных стен, покрытий, перекрытий над проездами и над холодными (без ограждающих стенок) подпольями в Северной строительно-климатической зоне.',
                       'перекрытий над холодными подвалами, сообщающимися с наружным воздухом, перекрытий над холодными (с ограждающими стенками) подпольями и холодными этажами в Северной строительно-климатической зоне.',
                       'перекрытий чердачных и над неотапливаемыми подвалами со световыми проемами в стенах, а также наружных стен с воздушной прослойкой, вентилируемой наружным воздухом.',
                       'перекрытий над неотапливаемыми подвалами и техническими, подпольями не вентилируемых наружным воздухом.']
    hor_headers = ['Название материала', 'δ, мм', 'λ, Вт/(м∙ºС)', 's, Вт/(м²·°С)', '', '', '', '', '']

    def __init__(self, parent=None, constr=None):
        super().__init__()
        self.current_construction = constr
        self.vbox = QVBoxLayout()
        self.label1 = QLabel('Состав конструкции')
        self.vbox.addWidget(self.label1)
        self.table_layer = QTableWidget()
        self.table_layer.setColumnCount(9)
        self.table_layer.setHorizontalHeaderLabels(self.hor_headers)
        self.table_layer.horizontalHeader().setVisible(True)
        self.table_layer.setColumnWidth(0, 300)
        self.table_layer.setColumnWidth(1, 80)
        self.table_layer.setColumnWidth(2, 80)
        self.table_layer.setColumnWidth(3, 80)
        self.table_layer.setColumnWidth(4, 20)
        self.table_layer.setColumnWidth(5, 20)
        self.table_layer.setColumnWidth(6, 20)
        self.table_layer.setColumnWidth(7, 20)
        self.table_layer.setColumnWidth(8, 20)
        self.vbox.addWidget(self.table_layer)
        self.label2 = QLabel('Внутреняя поверхность')
        self.vbox.addWidget(self.label2)
        self.combo_alfa_int = QComboBox()
        self.combo_alfa_int.addItems(self.typ_surface_int)
        self.vbox.addWidget(self.combo_alfa_int)
        self.label3 = QLabel('Наружная поверхность')
        self.vbox.addWidget(self.label3)
        self.combo_alfa_ext = QComboBox()
        self.combo_alfa_ext.addItems(self.typ_surface_ext)
        self.vbox.addWidget(self.combo_alfa_ext)
        self.hbox = QHBoxLayout()
        self.label4 = QLabel('Коэффициент теплотехнической однородности')
        self.hbox.addWidget(self.label4)
        self.coef_r = QLineEdit()
        self.hbox.addWidget(self.coef_r)
        self.vbox.addLayout(self.hbox)
        self.label5 = QLabel('Вывод результата')
        self.vbox.addWidget(self.label5)
        self.result_text = QTextEdit()
        self.vbox.addWidget(self.result_text)
        parent.addLayout(self.vbox)
        # Установка размеров
        self.table_layer.setMaximumSize(QSize(16777215, 16777215))
        self.table_layer.setMinimumSize(QSize(650, 16777215))
        self.combo_alfa_int.setMaximumSize(QSize(16777215, 16777215))
        self.combo_alfa_int.setMinimumSize(QSize(650, 16777215))
        self.combo_alfa_ext.setMaximumSize(QSize(16777215, 16777215))
        self.combo_alfa_ext.setMinimumSize(QSize(650, 16777215))
        self.coef_r.setMaximumSize(QSize(150, 20))
        self.result_text.setMaximumSize(QSize(16777215, 200))
        self.result_text.setMinimumSize(QSize(16777215, 150))
        self.label1.setMaximumSize(QSize(16777215, 20))
        self.label2.setMaximumSize(QSize(16777215, 20))
        self.label3.setMaximumSize(QSize(16777215, 20))
        self.label4.setMaximumSize(QSize(16777215, 20))
        self.label5.setMaximumSize(QSize(16777215, 20))
        # Установка сигналов
        self.table_layer.itemChanged.connect(self.get_change)

    def draw_table(self):
        """Перерисовка таблицы со слоями конструкции"""
        self.table_layer.blockSignals(True)
        self.table_layer.clear()
        self.table_layer.setHorizontalHeaderLabels(self.hor_headers)
        if len(self.current_construction.layer) > 0:
            self.table_layer.setRowCount(len(self.current_construction.layer))
            for i, elem in enumerate(self.current_construction.layer):
                if type(elem) is Layer:
                    # добавление элемента с названием слоя
                    self.table_layer.setItem(i, 0, QTableWidgetItem(elem.name))
                    # добавление элемента с толщиной слоя
                    el = QTableWidgetItem(str(elem.thickness))
                    el.setTextAlignment(Qt.AlignRight)
                    el.setTextAlignment(Qt.AlignVCenter)
                    self.table_layer.setItem(i, 1, el)
                    # добавление элемента с коэффициентом теплопроводности
                    el = QTableWidgetItem(str(elem.lam))
                    el.setTextAlignment(Qt.AlignRight)
                    el.setTextAlignment(Qt.AlignVCenter)
                    self.table_layer.setItem(i, 2, el)
                    # добавление элемента с коэффициентом теплопроводности
                    el = QTableWidgetItem(str(elem.s))
                    el.setTextAlignment(Qt.AlignRight)
                    el.setTextAlignment(Qt.AlignVCenter)
                    self.table_layer.setItem(i, 3, el)
                    # добавление кнопки для добавления пустого слоя
                    el_but = QPushButton()
                    el_but.setToolTip('Добавить пустой слой')
                    el_icon = QIcon('add.png')
                    el_but.setIcon(el_icon)
                    el_but.clicked.connect(self.add_layer)
                    self.table_layer.setCellWidget(i, 4, el_but)
                    # добавление кнопки для удаления активного слоя
                    el_but = QPushButton()
                    el_but.setToolTip('Удалить слой')
                    el_icon = QIcon('minus.png')
                    el_but.setIcon(el_icon)
                    el_but.clicked.connect(self.delete_layer)
                    self.table_layer.setCellWidget(i, 5, el_but)
                    # добавление кнопки для открытия базы материалов
                    el_but = QPushButton()
                    el_but.setToolTip('Открыть базу материалов')
                    el_icon = QIcon('base.png')
                    el_but.setIcon(el_icon)
                    el_but.clicked.connect(self.show_base)
                    self.table_layer.setCellWidget(i, 6, el_but)
                    # добавление кнопки для перемещения слоя вверх
                    el_but = QPushButton()
                    el_but.setToolTip('Переместить слой вверх')
                    el_icon = QIcon('up.png')
                    el_but.setIcon(el_icon)
                    el_but.clicked.connect(self.move_up)
                    self.table_layer.setCellWidget(i, 7, el_but)
                    # добавление кнопки для перемещения слоя вниз
                    el_but = QPushButton()
                    el_but.setToolTip('Переместить слой вниз')
                    el_icon = QIcon('down.png')
                    el_but.setIcon(el_icon)
                    el_but.clicked.connect(self.move_down)
                    self.table_layer.setCellWidget(i, 8, el_but)
        self.table_layer.blockSignals(False)

    def get_change(self):
        """Сохранение внесенных изменений"""
        index = self.table_layer.currentRow()
        current_layer = self.current_construction.layer[index]
        current_layer.name = self.table_layer.item(index, 0).text()
        try:
            current_layer.thickness = float(to_dot(self.table_layer.item(index, 1).text()))
        except:
            QMessageBox.about(self, "Ошибка", f"Неверно указана толщина слоя {index}")
        try:
            current_layer.lam = float(to_dot(self.table_layer.item(index, 2).text()))
        except:
            QMessageBox.about(self, "Ошибка", f"Неверно указан коэффициент теплопроводности слоя {index}")
        try:
            current_layer.s = float(to_dot(self.table_layer.item(index, 3).text()))
        except:
            QMessageBox.about(self, "Ошибка", f"Неверно указан коэффициент тепловосприятия слоя {index}")

    def add_layer(self):
        """Добавление нового слоя"""
        self.current_construction.add_sloy()
        self.draw_table()

    def delete_layer(self):
        """Удаление активного слоя"""
        if self.table_layer.rowCount() > 1:
            cur = self.table_layer.currentRow()
            try:
                self.current_construction.layer.pop(cur)
            except ValueError:
                QMessageBox.about(self, "Ошибка", "Ошибка при удалении слоя")
            self.draw_table()
        else:
            QMessageBox.about(self, "Ошибка", "Должен остаться хотя бы один слой")

    def show_base(self):
        """Открыть окно с базой материалов"""
        pass

    def move_up(self):
        """Переместить слой вверх"""
        if self.table_layer.rowCount() > 1:
            cur = self.table_layer.currentRow()
            if cur > 0:
                move_element = self.current_construction.layer.pop(cur)
                self.current_construction.layer.insert(cur - 1, move_element)
                self.draw_table()

    def move_down(self):
        """Переестить слой вниз"""
        if self.table_layer.rowCount() > 1:
            cur = self.table_layer.currentRow()
            if cur < self.table_layer.rowCount() - 1:
                move_element = self.current_construction.layer.pop(cur)
                self.current_construction.layer.insert(cur + 1, move_element)
                self.draw_table()
