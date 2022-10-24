from PyQt5.QtWidgets import QWidget, QFrame, QTabWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, \
    QPushButton, QDialog, QLineEdit, QApplication, QLabel, QGridLayout, QTextEdit, QGroupBox, QRadioButton
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
from gui.gui_widgets import *
from gui.gui_materials import *
from lib.materials import Materials
from lib.construction import Construction
from lib.layer import Layer
from lib.config import *


class FormConstruction(QWidget):
    def __init__(self, construction: Construction, materials: Materials, parent=None):
        super(FormConstruction, self).__init__(parent)
        self.construction = construction
        self.materials = materials
        self.add_materials = AllMaterials(self.materials)
        vbox1 = QVBoxLayout()
        self.frame1 = QFrame()
        self.frame2 = QFrame()
        vbox2 = QVBoxLayout()
        label1 = QLabel('Состав конструкции')
        vbox2.addWidget(label1)
        # Таблица слоев конструкции
        self.table_layer = QTableWidget()
        self.table_layer.setMinimumHeight(200)
        self.table_layer.setMaximumHeight(800)
        self.table_layer.setColumnCount(6)
        self.table_layer.setHorizontalHeaderLabels(HEADER_CONSTRUCTION)
        self.table_layer.horizontalHeader().setVisible(True)
        self.table_layer.setColumnWidth(0, 380)
        self.table_layer.setColumnWidth(1, 60)
        self.table_layer.setColumnWidth(2, 70)
        self.table_layer.setColumnWidth(3, 70)
        self.table_layer.setColumnWidth(4, 70)
        self.table_layer.setColumnWidth(5, 60)
        self.table_layer.setSelectionBehavior(self.table_layer.SelectRows)
        self.table_layer.setFocusPolicy(Qt.StrongFocus)
        # Настройка делегата для таблицы
        self._delegate = HighlightDelegate(self.table_layer)
        self.table_layer.setItemDelegateForColumn(0, self._delegate)
        self._delegate.set_wordwrap(True)
        vbox2.addWidget(self.table_layer)
        # Итоговая строка под таблицей
        hbox_sum = QHBoxLayout()
        label_sum = QLabel("Итого")
        self.set_bold_text(label_sum, 380)
        self.label_thickness = QLabel("0.0")
        self.set_bold_text(self.label_thickness, 60)
        self.label_r = QLabel("0.0")
        self.set_bold_text(self.label_r, 70)
        self.label_d = QLabel("0.0")
        self.set_bold_text(self.label_d, 60)
        hbox_sum.addWidget(label_sum)
        hbox_sum.addWidget(self.label_thickness)
        hbox_sum.addSpacing(130)
        hbox_sum.addWidget(self.label_r)
        hbox_sum.addWidget(self.label_d)
        hbox_sum.addStretch(0)
        vbox2.addLayout(hbox_sum)
        # Управляющие кнопки к таблице
        hbox_button = QHBoxLayout()
        self.button_add = QPushButton("Новый слой")
        el_icon = QIcon('icons/add.png')
        self.button_add.setIcon(el_icon)
        self.button_edit = QPushButton("Редактировать")
        el_icon = QIcon('icons/edit.png')
        self.button_edit.setIcon(el_icon)
        self.button_up = QPushButton("Вверх")
        el_icon = QIcon('icons/up.png')
        self.button_up.setIcon(el_icon)
        self.button_down = QPushButton("Вниз")
        el_icon = QIcon('icons/down.png')
        self.button_down.setIcon(el_icon)
        self.button_del = QPushButton("Удалить слой")
        el_icon = QIcon('icons/minus-low.png')
        self.button_del.setIcon(el_icon)
        hbox_button.addWidget(self.button_add)
        hbox_button.addWidget(self.button_edit)
        hbox_button.addWidget(self.button_up)
        hbox_button.addWidget(self.button_down)
        hbox_button.addStretch(0)
        hbox_button.addWidget(self.button_del)
        vbox2.addLayout(hbox_button)
        # Параметры внутренней поверхности
        self.group_int = QGroupBox("Параметры внутренней поверхности")
        vbox_int = QVBoxLayout()
        for i, elem in enumerate(TYPE_SURFACE_INT):
            radio_int = QRadioButton(elem)
            if i == 0:
                radio_int.setChecked(True)
            vbox_int.addWidget(radio_int)
        self.group_int.setLayout(vbox_int)
        vbox2.addWidget(self.group_int)
        # Параметры наружной поверхности
        self.group_ext = QGroupBox("Параметры наружной поверхности")
        vbox_ext = QVBoxLayout()
        for i, elem in enumerate(TYPE_SURFACE_EXT):
            radio_ext = QRadioButton(elem)
            if i == 0:
                radio_ext.setChecked(True)
            vbox_ext.addWidget(radio_ext)
        self.group_ext.setLayout(vbox_ext)
        vbox2.addWidget(self.group_ext)
        # Добавление ввода коэффициента неоднородности
        hbox = QHBoxLayout()
        label4 = QLabel('Коэффициент теплотехнической однородности')
        hbox.addWidget(label4)
        self.edit_ratio_r = QLineEdit()
        self.edit_ratio_r.setText('1.0')
        hbox.addWidget(self.edit_ratio_r)
        hbox.addStretch(0)
        vbox2.addLayout(hbox)
        self.frame1.setLayout(vbox2)
        # Настройка вкладок
        self.tab = QTabWidget()
        self.tab.addTab(self.frame1, "Ввод данных")
        self.tab.addTab(self.frame2, "Результат")
        self.tab.setCurrentIndex(0)
        vbox1.addWidget(self.tab)
        self.setLayout(vbox1)
        # Обработка сигналов
        for elem in self.group_int.findChildren(QRadioButton):
            elem.clicked.connect(self.change_int)
        for elem in self.group_ext.findChildren(QRadioButton):
            elem.clicked.connect(self.change_ext)
        self.button_add.clicked.connect(self.add_layer)
        self.button_up.clicked.connect(self.move_up)
        self.button_down.clicked.connect(self.move_down)
        self.table_layer.itemChanged.connect(self.change_table)
        self.edit_ratio_r.editingFinished.connect(self.change_ratio_r)
        self.update_form()

    def select_row(self):
        """Выделение активной строки таблицы"""
        self.table_layer.setCurrentCell(self.table_layer.currentRow(), 1)
        self.table_layer.setFocus()

    @staticmethod
    def set_bold_text(label: QLabel, width: int):
        """Настройка размеров метки"""
        label.setFixedWidth(width)
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Times", 10, QFont.Bold))

    def change_int(self):
        """Обработка смены типа внутренней поверхности"""
        for i, elem in enumerate(self.group_int.findChildren(QRadioButton)):
            if elem.isChecked():
                self.construction.ratio_inner_surface = RATIO_ALFA_INT[i]
                break
        self.update_form()

    def change_ext(self):
        """Обработка смены типа наружной поверхности"""
        for i, elem in enumerate(self.group_ext.findChildren(QRadioButton)):
            if elem.isChecked():
                self.construction.ratio_outer_surface = RATIO_ALFA_EXT[i]
                break
        self.update_form()

    def change_ratio_r(self):
        """Обработка изменения коэффициента однородности"""
        self.construction.ratio_r = self.edit_ratio_r.text()
        self.update_form()

    def add_layer(self):
        """Добавление нового слоя"""
        new_material = self.add_materials.exec_()
        if new_material:
            cur_row = self.table_layer.currentRow()
            self.construction.add_layer(new_material, cur_row)
            self.update_form()
            self.table_layer.selectRow(cur_row + 1)
        self.select_row()

    def move_up(self):
        """Перемещение слоя вверх"""
        row = self.table_layer.currentRow()
        self.construction.move_up(row)
        self.update_form()
        if row > 0:
            self.table_layer.selectRow(row - 1)
        else:
            self.table_layer.selectRow(row)
        self.select_row()

    def move_down(self):
        """Перемещение слоя вниз"""
        row = self.table_layer.currentRow()
        self.construction.move_down(row)
        self.update_form()
        if row < self.table_layer.rowCount() - 1:
            self.table_layer.selectRow(row + 1)
        else:
            self.table_layer.selectRow(row)
        self.select_row()

    def change_table(self):
        cur_row = self.table_layer.currentRow()
        if cur_row > -1:
            new_layer = (self.table_layer.item(cur_row, 0).text(), self.table_layer.item(cur_row, 1).text(),
                         self.table_layer.item(cur_row, 2).text(), self.table_layer.item(cur_row, 3).text(),
                         self.table_layer.item(cur_row, 4).text(), self.table_layer.item(cur_row, 5).text())
            self.construction.set_layer(new_layer, cur_row)
            self.update_form()

    def update_form(self):
        """Обновление формы при изменении данных"""
        # Обновление таблицы
        self.table_layer.blockSignals(True)
        self.table_layer.setRowCount(0)
        for i, layer in enumerate(self.construction.get_layers()):
            self.table_layer.setRowCount(i + 1)
            for j in range(6):
                if j < 4:
                    value = str(layer[j])
                else:
                    value = f"{layer[j]:.3f}"
                new_item = QTableWidgetItem(value)
                self.table_layer.setItem(i, j, new_item)
        self.table_layer.blockSignals(False)
        # Обновление итоговой строки
        self.label_thickness.setText(str(self.construction.thickness))
        self.label_r.setText(f"{self.construction.resistance:.3f}")
        self.label_d.setText(f"{self.construction.inertia:.3f}")
        # Обновление настроек внутренней поверхности
        for i, elem in enumerate(self.group_int.findChildren(QRadioButton)):
            if self.construction.ratio_inner_surface == RATIO_ALFA_INT[i]:
                elem.blockSignals(True)
                elem.setChecked(True)
                elem.blockSignals(False)
        # Обновление настроек наружной поверхности
        for i, elem in enumerate(self.group_ext.findChildren(QRadioButton)):
            if self.construction.ratio_outer_surface == RATIO_ALFA_EXT[i]:
                elem.blockSignals(True)
                elem.setChecked(True)
                elem.blockSignals(False)
        # Обновление поля ввода коэффициента однородности
        self.edit_ratio_r.blockSignals(True)
        self.edit_ratio_r.setText(str(self.construction.ratio_r))
        self.edit_ratio_r.blockSignals(False)


# Для тестирования
import sys
from PyQt5.QtWidgets import QMainWindow

class TestWindow(QMainWindow):
    def __init__(self, parent=None):
        super(TestWindow, self).__init__()
        self.resize(800, 600)
        construction = Construction()
        materials = Materials()
        tab = FormConstruction(construction, materials)
        self.setCentralWidget(tab)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec_())
