from PyQt5.QtWidgets import QApplication, QStyledItemDelegate, QStyleOptionViewItem, QStyle
from PyQt5.QtGui import QTextOption, QTextDocument
from PyQt5.QtCore import QSizeF, QPointF, QRectF, QSize, Qt


class HighlightDelegate(QStyledItemDelegate):
    """
    Класс делегата для ячеек таблицы с переносом текста
    """
    def __init__(self, parent=None):
        super(HighlightDelegate, self).__init__(parent)
        self.doc = QTextDocument(self)
        mode = QTextOption.WordWrap
        text_option = QTextOption(self.doc.defaultTextOption())
        text_option.setWrapMode(mode)
        self.doc.setDefaultTextOption(text_option)
        self.parent().viewport().update()

    def paint(self, painter, option, index):
        painter.save()
        options = QStyleOptionViewItem(option)
        self.initStyleOption(options, index)
        self.doc.setPlainText(options.text)
        self.doc.setTextWidth(options.rect.width())
        options.text = ""
        style = QApplication.style() if options.widget is None else options.widget.style()
        style.drawControl(QStyle.CE_ItemViewItem, options, painter)
        painter.translate(options.rect.left(), options.rect.top())
        clip = QRectF(QPointF(), QSizeF(options.rect.size()))
        self.doc.drawContents(painter, clip)
        painter.restore()
        s = QSize(int(self.doc.idealWidth()), int(self.doc.size().height()))
        index.model().setData(index, s, Qt.SizeHintRole)
