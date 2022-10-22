from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QPushButton, QDialog, \
    QLineEdit, QApplication, QLabel, QHeaderView, QGridLayout, QTextEdit, QStyledItemDelegate, QStyleOptionViewItem, QStyle
from PyQt5 import QtCore, QtGui
from lib.materials import Materials
from lib.config import *


class HighlightDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(HighlightDelegate, self).__init__(parent)
        self._wordwrap = False
        self.doc = QtGui.QTextDocument(self)

    def paint(self, painter, option, index):
        painter.save()
        options = QStyleOptionViewItem(option)
        self.initStyleOption(options, index)
        self.doc.setPlainText(options.text)

        if self._wordwrap:
            self.doc.setTextWidth(options.rect.width())
        options.text = ""

        style = QApplication.style() if options.widget is None else options.widget.style()
        style.drawControl(QStyle.CE_ItemViewItem, options, painter)

        if self._wordwrap:
            painter.translate(options.rect.left(), options.rect.top())
            clip = QtCore.QRectF(QtCore.QPointF(), QtCore.QSizeF(options.rect.size()))
            self.doc.drawContents(painter, clip)
        else:
            ctx = QtGui.QAbstractTextDocumentLayout.PaintContext()
            if option.state & QStyle.State_Selected:
                ctx.palette.setColor(QtGui.QPalette.Text, option.palette.color(
                    QtGui.QPalette.Active, QtGui.QPalette.HighlightedText))
            else:
                ctx.palette.setColor(QtGui.QPalette.Text, option.palette.color(
                    QtGui.QPalette.Active, QtGui.QPalette.Text))
            text_rect = style.subElementRect(QStyle.SE_ItemViewItemText, options, None)
            if index.column() != 0:
                text_rect.adjust(5, 0, 0, 0)
            constant = 4
            margin = (option.rect.height() - options.fontMetrics.height()) // 2
            margin = margin - constant
            text_rect.setTop(text_rect.top() + margin)
            painter.translate(text_rect.topLeft())
            painter.setClipRect(text_rect.translated(-text_rect.topLeft()))
            self.doc.documentLayout().draw(painter, ctx)

        painter.restore()
        s = QtCore.QSize(int(self.doc.idealWidth()), int(self.doc.size().height()))
        index.model().setData(index, s, QtCore.Qt.SizeHintRole)

    def set_wordwrap(self, on):
        self._wordwrap = on
        mode = QtGui.QTextOption.WordWrap if on else QtGui.QTextOption.WrapAtWordBoundaryOrAnywhere

        text_option = QtGui.QTextOption(self.doc.defaultTextOption())
        text_option.setWrapMode(mode)
        self.doc.setDefaultTextOption(text_option)
        self.parent().viewport().update()


class AddMaterial(QDialog):
    def __init__(self, parent=None):
        super(AddMaterial, self).__init__(parent)
        self.resize(400, 200)
        self.setWindowTitle("Новый материал")
        vbox = QVBoxLayout()
        grid = QGridLayout()
        # Метки элементов
        for i, item in enumerate(HEADER_MATERIALS):
            label = QLabel(item)
            grid.addWidget(label, i, 0)
        # Элементы ввода текста
        self.line_name = QTextEdit()
        self.line_name.setMinimumHeight(60)
        self.line_name.setMaximumHeight(200)
        self.line_density = QLineEdit()
        self.line_lama = QLineEdit()
        self.line_lamb = QLineEdit()
        self.line_sa = QLineEdit()
        self.line_sb = QLineEdit()
        self.line_density.setMaximumWidth(150)
        self.line_lama.setMaximumWidth(150)
        self.line_lamb.setMaximumWidth(150)
        self.line_sa.setMaximumWidth(150)
        self.line_sb.setMaximumWidth(150)
        # Кнопки
        self.button_ok = QPushButton("Ok")
        self.button_ok.setMinimumWidth(150)
        self.button_cancel = QPushButton("Cancel")
        self.button_cancel.setMinimumWidth(150)
        self.button_ok.clicked.connect(self.set_ok)
        self.button_cancel.clicked.connect(self.set_cancel)
        # Компоновка элементов
        grid.addWidget(self.line_name, 0, 1)
        grid.addWidget(self.line_density, 1, 1)
        grid.addWidget(self.line_lama, 2, 1)
        grid.addWidget(self.line_lamb, 3, 1)
        grid.addWidget(self.line_sa, 4, 1)
        grid.addWidget(self.line_sb, 5, 1)
        hbox = QHBoxLayout()
        hbox.addWidget(self.button_ok)
        hbox.addStretch()
        hbox.addWidget(self.button_cancel)
        vbox.addLayout(grid)
        vbox.addStretch(0)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

    def set_ok(self):
        self.accept()

    def set_cancel(self):
        self.reject()

    def clear(self):
        self.line_name.clear()
        self.line_density.clear()
        self.line_lama.clear()
        self.line_lamb.clear()
        self.line_sa.clear()
        self.line_sb.clear()


class AllMaterials(QDialog):
    def __init__(self, mat: Materials, parent=None):
        super(AllMaterials, self).__init__(parent)
        self.materials = mat
        self.vertical_headers = []
        self.resize(800, 600)
        self.dialog_add = AddMaterial()
        # Основные контейнеры
        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()
        # Элементы для поиска материалов
        self.label1 = QLabel("Поиск:")
        self.query = QLineEdit()
        self.button_clear = QPushButton()
        self.button_clear.setIcon(QtGui.QIcon('icons/close.png'))
        self.button_clear.setStyleSheet("QPushButton {border : 0; background: transparent}")
        self.button_clear.setMaximumWidth(30)
        self.button_clear.setVisible(False)
        self.button_add = QPushButton("Новый")
        self.button_add.setIcon(QtGui.QIcon('icons/add.png'))
        self.button_del = QPushButton("Удалить")
        self.button_del.setIcon(QtGui.QIcon('icons/minus-low.png'))
        self.button_copy = QPushButton("Копия")
        self.button_copy.setIcon(QtGui.QIcon('icons/copy.png'))
        self.button_edit = QPushButton("Редактировать")
        self.button_edit.setIcon(QtGui.QIcon('icons/edit.png'))
        self.hbox.addWidget(self.label1)
        self.hbox.addWidget(self.query)
        self.hbox.addWidget(self.button_clear)
        self.hbox.addStretch()
        self.hbox.addWidget(self.button_add)
        self.hbox.addWidget(self.button_edit)
        self.hbox.addWidget(self.button_copy)
        self.hbox.addWidget(self.button_del)
        self.vbox.addLayout(self.hbox)
        # Таблица с материалами
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setColumnWidth(0, 300)
        self.table.setColumnWidth(1, 110)
        for i in range(2, 6):
            self.table.setColumnWidth(i, 85)
        self.set_table_headers()
        self.table.setSelectionBehavior(self.table.SelectRows)
        self.button_select = QPushButton("Выбрать")
        self.vbox.addWidget(self.table)
        self.vbox.addWidget(self.button_select)
        self.setLayout(self.vbox)
        # Настройка делегата
        self._delegate = HighlightDelegate(self.table)
        self.table.setItemDelegate(self._delegate)
        self._delegate.set_wordwrap(True)
        # Обработка событий
        self.query.textChanged.connect(self.input_text)
        self.button_clear.clicked.connect(self.clear_text)
        self.button_add.clicked.connect(self.add_material)
        self.button_edit.clicked.connect(self.edit_material)
        self.button_del.clicked.connect(self.del_material)
        self.button_copy.clicked.connect(self.copy_material)
        # Вывод списка материалов
        self.show_materials()
        if self.table.rowCount() > 0:
            self.table.setFocus()
            self.table.setCurrentCell(0, 0)

    def set_table_headers(self):
        self.table.setHorizontalHeaderLabels(HEADER_MATERIALS)
        self.table.setVerticalHeaderLabels([str(x) for x in self.vertical_headers])

    def show_materials(self):
        self.table.clear()
        self.table.setRowCount(0)
        row = 0
        self.vertical_headers = []
        if self.materials.count_materials() > 0:
            for material in self.materials.get_materials(self.query.text()):
                self.vertical_headers.append(material[0])
                row += 1
                self.table.setRowCount(row)
                for i in range(6):
                    newitem = QTableWidgetItem(str(material[i + 1]))
                    self.table.setItem(row - 1, i, newitem)
        self.set_table_headers()

    def input_text(self):
        """Обработка ввода текста в поле поиска"""
        if len(self.query.text()) > 0:
            self.button_clear.setVisible(True)
            if len(self.query.text()) > 2:
                self.show_materials()
        else:
            self.button_clear.setVisible(False)

    def clear_text(self):
        """Очистка текстового поля для поиска материалов"""
        self.query.setText("")
        self.show_materials()
        self.table.setCurrentCell(0, 0)
        self.table.setFocus()

    def add_material(self):
        """Добавление нового материала"""
        self.dialog_add.clear()
        result = self.dialog_add.exec_()
        if result:
            # Добавление нового материала
            result = (self.dialog_add.line_name.toPlainText(), self.dialog_add.line_density.text(),
                      self.dialog_add.line_lama.text(), self.dialog_add.line_lamb.text(),
                      self.dialog_add.line_sa.text(), self.dialog_add.line_sb.text())
            self.materials.add_material(result)
            self.show_materials()
            count = self.table.rowCount()
            self.table.setCurrentCell(count - 1, 0)
            self.table.setFocus()

    def edit_material(self):
        """Редактирование существующего материала"""
        self.dialog_add.clear()
        row = self.table.currentRow()
        item = self.get_item(row)
        index = int(self.table.verticalHeaderItem(row).text())
        self.dialog_add.line_name.setText(item[0])
        self.dialog_add.line_density.setText(item[1])
        self.dialog_add.line_lama.setText(item[2])
        self.dialog_add.line_lamb.setText(item[3])
        self.dialog_add.line_sa.setText(item[4])
        self.dialog_add.line_sb.setText(item[5])
        result = self.dialog_add.exec_()
        if result:
            # Изменение существующего материала
            result = (self.dialog_add.line_name.toPlainText(), self.dialog_add.line_density.text(),
                      self.dialog_add.line_lama.text(), self.dialog_add.line_lamb.text(),
                      self.dialog_add.line_sa.text(), self.dialog_add.line_sb.text())
            self.materials.edit_material(result, index)
            self.show_materials()
            self.table.setCurrentCell(row, 0)
            self.table.setFocus()

    def get_item(self, row: int = 0) -> tuple:
        """Кортеж из элементов строки"""
        if row < self.table.rowCount():
            item = (self.table.item(row, 0).text(), self.table.item(row, 1).text(), self.table.item(row, 2).text(),
                    self.table.item(row, 3).text(), self.table.item(row, 4).text(), self.table.item(row, 5).text())
            return item
        return None

    def del_material(self):
        """Удаление выбранного материала"""
        row = self.table.currentRow()
        index = int(self.table.verticalHeaderItem(row).text())
        self.materials.del_material(index)
        self.show_materials()
        if row > self.table.rowCount() - 1:
            row -= 1
        self.table.setCurrentCell(row, 0)
        self.table.setFocus()

    def copy_material(self):
        """Дубликат выбранного материала"""
        row = self.table.currentRow()
        item = self.get_item(row)
        self.materials.add_material(item)
        self.show_materials()
        self.table.setCurrentCell(self.table.rowCount() - 1, 0)
        self.table.setFocus()


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QMainWindow

    app = QApplication(sys.argv)
    materials = Materials()
    window = QMainWindow()
    dialog = AllMaterials(mat=materials, parent=window)
    dialog.setWindowModality(QtCore.Qt.WindowModal)
    window.resize(300, 200)
    button = QPushButton("Открыть новое окно", parent=window)
    button.resize(200, 40)
    button.move(50, 50)
    button.clicked.connect(dialog.show)
    window.show()
    sys.exit(app.exec_())
