from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QTextEdit, QPushButton, QMessageBox, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
from construction import Construction, Layer
from func import to_dot, MyCombo


class ConstructionLayer(QWidget):
    hor_headers = ['Название материала', 'δ, \nмм', 'λ, \nВт/(м∙ºС)', 's, \nВт/(м²·°С)', '', '', '', '', '']

    def __init__(self, parent=None, building=None):
        super().__init__()
        self.build = building
        self.current_construction = None
        self.norm = None
        self.vbox = QVBoxLayout()
        self.label1 = QLabel('Состав конструкции')
        self.vbox.addWidget(self.label1)
        self.table_layer = QTableWidget()
        self.table_layer.setColumnCount(9)
        self.table_layer.setHorizontalHeaderLabels(self.hor_headers)
        self.table_layer.horizontalHeader().setVisible(True)
        self.table_layer.setColumnWidth(0, 300)
        self.table_layer.setColumnWidth(1, 60)
        self.table_layer.setColumnWidth(2, 70)
        self.table_layer.setColumnWidth(3, 70)
        self.table_layer.setColumnWidth(4, 20)
        self.table_layer.setColumnWidth(5, 20)
        self.table_layer.setColumnWidth(6, 20)
        self.table_layer.setColumnWidth(7, 20)
        self.table_layer.setColumnWidth(8, 20)
        self.vbox.addWidget(self.table_layer)
        self.label2 = QLabel('Внутреняя поверхность')
        self.vbox.addWidget(self.label2)
        # Настройка списка внутренней поверхности
        self.combo_alfa_int = MyCombo(Construction.typ_surface_int)
        self.vbox.addWidget(self.combo_alfa_int)
        # Вставка надписи
        self.label3 = QLabel('Наружная поверхность')
        self.vbox.addWidget(self.label3)
        # Настройка списка наружной поверхности
        self.combo_alfa_ext = MyCombo(Construction.typ_surface_ext)
        self.vbox.addWidget(self.combo_alfa_ext)
        # Добавление ввода коэффициента неоднородности
        self.hbox = QHBoxLayout()
        self.label4 = QLabel('Коэффициент теплотехнической однородности')
        self.hbox.addWidget(self.label4)
        self.coef_r = QLineEdit()
        self.coef_r.setText('1.0')
        self.hbox.addWidget(self.coef_r)
        self.vbox.addLayout(self.hbox)
        # Элементы для вывода результатов
        self.label5 = QLabel('Вывод результата')
        self.vbox.addWidget(self.label5)
        self.result_text = QTextEdit()
        self.vbox.addWidget(self.result_text)
        parent.addLayout(self.vbox)
        # Установка размеров
        self.table_layer.setMaximumSize(QSize(16777215, 16777215))
        self.table_layer.setMinimumSize(QSize(650, 0))
        self.combo_alfa_int.setMaximumSize(QSize(16777215, 16777215))
        self.combo_alfa_int.setMinimumSize(QSize(650, 0))
        self.combo_alfa_ext.setMaximumSize(QSize(16777215, 16777215))
        self.combo_alfa_ext.setMinimumSize(QSize(650, 0))
        self.coef_r.setMaximumSize(QSize(150, 20))
        self.result_text.setMaximumSize(QSize(16777215, 200))
        self.result_text.setMinimumSize(QSize(0, 150))
        self.label1.setMaximumSize(QSize(16777215, 20))
        self.label2.setMaximumSize(QSize(16777215, 20))
        self.label3.setMaximumSize(QSize(16777215, 20))
        self.label4.setMaximumSize(QSize(16777215, 20))
        self.label5.setMaximumSize(QSize(16777215, 20))
        # Установка сигналов
        self.table_layer.itemChanged.connect(self.get_change)
        self.combo_alfa_int.activated.connect(self.get_change)
        self.combo_alfa_ext.activated.connect(self.get_change)
        self.coef_r.editingFinished.connect(self.get_change)

    def build_table(self, constr=None, norm=None):
        self.current_construction = constr
        self.norm = norm
        self.draw_table()

    def draw_table(self):
        """Перерисовка таблицы со слоями конструкции и других элементов"""
        self.table_layer.blockSignals(True)
        self.combo_alfa_int.blockSignals(True)
        self.combo_alfa_ext.blockSignals(True)
        self.coef_r.blockSignals(True)
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
                    el.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                    self.table_layer.setItem(i, 1, el)
                    # добавление элемента с коэффициентом теплопроводности
                    el = QTableWidgetItem(str(elem.lam))
                    el.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                    self.table_layer.setItem(i, 2, el)
                    # добавление элемента с коэффициентом теплопроводности
                    el = QTableWidgetItem(str(elem.s))
                    el.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
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
        # вставка типов поверхностей конструкции
        self.combo_alfa_int.setCurrentIndex(Construction.list_alfa_int.index(self.current_construction.alfa_int))
        self.combo_alfa_ext.setCurrentIndex(Construction.list_alfa_ext.index(self.current_construction.alfa_ext))
        self.coef_r.setText(str(self.current_construction.r_neodn))
        self.result_text.clear()
        self.result_text.setText(self.current_construction.get_text_r())
        self.table_layer.blockSignals(False)
        self.combo_alfa_int.blockSignals(False)
        self.combo_alfa_ext.blockSignals(False)
        self.coef_r.blockSignals(False)

    def get_change(self):
        """Сохранение внесенных изменений"""
        # Сохранение изменений в таблице
        cur_row = self.table_layer.currentRow()
        if cur_row > -1:
            current_layer = self.current_construction.layer[cur_row]
            current_layer.name = self.table_layer.item(cur_row, 0).text()
            try:
                current_layer.thickness = float(to_dot(self.table_layer.item(cur_row, 1).text()))
            except:
                QMessageBox.about(self, "Ошибка", f"Неверно указана толщина слоя {cur_row}")
            try:
                current_layer.lam = float(to_dot(self.table_layer.item(cur_row, 2).text()))
            except:
                QMessageBox.about(self, "Ошибка", f"Неверно указан коэффициент теплопроводности слоя {cur_row}")
            try:
                current_layer.s = float(to_dot(self.table_layer.item(cur_row, 3).text()))
            except:
                QMessageBox.about(self, "Ошибка", f"Неверно указан коэффициент тепловосприятия слоя {cur_row}")
        # Сохранение изменений в выпадающих списках
        self.current_construction.alfa_int = Construction.list_alfa_int[self.combo_alfa_int.currentIndex()]
        self.current_construction.alfa_ext = Construction.list_alfa_ext[self.combo_alfa_ext.currentIndex()]
        try:
            self.current_construction.r_neodn = float(to_dot(self.coef_r.text()))
        except:
            self.current_construction.r_neodn = 1.0
            self.coef_r.setText('1.0')
        self.result_text.clear()
        self.build.calc()
        self.result_text.setText(self.current_construction.get_text_r())

    def add_layer(self):
        """Добавление нового слоя"""
        self.current_construction.add_layer()
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
                self.table_layer.selectRow(cur - 1)
                self.draw_table()

    def move_down(self):
        """Переестить слой вниз"""
        if self.table_layer.rowCount() > 1:
            cur = self.table_layer.currentRow()
            if cur < self.table_layer.rowCount() - 1:
                move_element = self.current_construction.layer.pop(cur)
                self.current_construction.layer.insert(cur + 1, move_element)
                self.table_layer.selectRow(cur + 1)
                self.draw_table()
