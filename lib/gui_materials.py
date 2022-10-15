from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QPushButton, QDialog, \
    QTableView, QLineEdit, QApplication, QLabel, QStyledItemDelegate, QStyleOptionViewItem, QStyle, QHeaderView
from PyQt5 import QtCore, QtGui


class HighlightDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super(HighlightDelegate, self).__init__(parent)
        self._filters = []
        self._wordwrap = False
        self.doc = QtGui.QTextDocument(self)

    def paint(self, painter, option, index):
        painter.save()
        options = QStyleOptionViewItem(option)
        self.initStyleOption(options, index)
        self.doc.setPlainText(options.text)
        self.apply_highlight()

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

    def apply_highlight(self):
        cursor = QtGui.QTextCursor(self.doc)
        cursor.beginEditBlock()
        fmt = QtGui.QTextCharFormat()
        fmt.setForeground(QtCore.Qt.red)
        for f in self.filters():
            highlight_cursor = QtGui.QTextCursor(self.doc)
            while not highlight_cursor.isNull() and not highlight_cursor.atEnd():
                highlight_cursor = self.doc.find(f, highlight_cursor)
                if not highlight_cursor.isNull():
                    highlight_cursor.mergeCharFormat(fmt)
        cursor.endEditBlock()

    @QtCore.pyqtSlot(list)
    def set_filters(self, filters):
        if self._filters == filters:
            return
        self._filters = filters
        self.parent().viewport().update()

    def filters(self):
        return self._filters

    def set_wordwrap(self, on):
        self._wordwrap = on
        mode = QtGui.QTextOption.WordWrap if on else QtGui.QTextOption.WrapAtWordBoundaryOrAnywhere

        text_option = QtGui.QTextOption(self.doc.defaultTextOption())
        text_option.setWrapMode(mode)
        self.doc.setDefaultTextOption(text_option)
        self.parent().viewport().update()


class ShowMaterials(QDialog):
    def __init__(self, parent=None):
        super(ShowMaterials, self).__init__(parent)
        self.resize(800, 600)
        # Основные контейнеры
        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()
        # Элементы для поиска материалов
        self.label1 = QLabel("Поиск:")
        self.query = QLineEdit(textChanged=self.on_textchanged)
        self.button_add = QPushButton("Добавить материал")
        self.button_clear = QPushButton("X")
        self.button_clear.setMaximumWidth(30)
        self.button_clear.setVisible(False)
        self.hbox.addWidget(self.label1)
        self.hbox.addWidget(self.query)
        self.hbox.addWidget(self.button_clear)
        self.hbox.addStretch()
        self.hbox.addWidget(self.button_add)
        self.vbox.addLayout(self.hbox)
        # Таблица с материалами
        self.materials = QTableWidget()
        self.materials.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self._delegate = HighlightDelegate(self.materials)
        self.materials.setItemDelegate(self._delegate)
        self._delegate.set_wordwrap(True)
        self.materials.setColumnCount(6)
        self.materials.setColumnWidth(0, 300)
        self.materials.setColumnWidth(1, 110)
        for i in range(2, 6):
            self.materials.setColumnWidth(i, 85)
        self.set_table_headers()
        self.vbox.addWidget(self.materials)
        self.setLayout(self.vbox)
        # Обработка событий
        self.query.textChanged.connect(self.input_text)
        self.button_clear.clicked.connect(self.clear_text)
        self.button_add.clicked.connect(self.add_material)

    @QtCore.pyqtSlot(str)
    def on_textchanged(self, text):
        self._delegate.set_filters(list(set(text.split())))

    def set_table_headers(self):
        headers = ["Название", "Плотность, кг/м³", "λа, Вт/(м∙ºС)", "λb, Вт/(м∙ºС)", "sa, Вт/(м²∙ºС)", "sb, Вт/(м²∙ºС)"]
        self.materials.setHorizontalHeaderLabels(headers)

    def input_text(self):
        """Обработка ввода текста в поле поиска"""
        if len(self.query.text()) > 0:
            self.button_clear.setVisible(True)
        else:
            self.button_clear.setVisible(False)

    def clear_text(self):
        """Очистка текстового поля для поиска материалов"""
        self.query.setText("")

    def add_material(self):
        """Добавление нового материала"""
        count = self.materials.rowCount() + 1
        self.materials.setRowCount(count)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = ShowMaterials()
    window.show()
    sys.exit(app.exec_())
