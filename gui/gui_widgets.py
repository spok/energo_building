from PyQt5.QtWidgets import QApplication, QStyledItemDelegate, QStyleOptionViewItem, QStyle
from PyQt5.QtGui import QAbstractTextDocumentLayout, QPalette, QTextOption, QTextDocument
from PyQt5.QtCore import QSizeF, QPointF, QRectF, QSize, Qt


class HighlightDelegate(QStyledItemDelegate):
    """
    Класс делегата для ячеек таблицы с переносом текста
    """
    def __init__(self, parent=None):
        super(HighlightDelegate, self).__init__(parent)
        self._wordwrap = False
        self.doc = QTextDocument(self)

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
            clip = QRectF(QPointF(), QSizeF(options.rect.size()))
            self.doc.drawContents(painter, clip)
        else:
            ctx = QAbstractTextDocumentLayout.PaintContext()
            if option.state & QStyle.State_Selected:
                ctx.palette.setColor(QPalette.Text, option.palette.color(
                    QPalette.Active, QPalette.HighlightedText))
            else:
                ctx.palette.setColor(QPalette.Text, option.palette.color(
                    QPalette.Active, QPalette.Text))
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
        s = QSize(int(self.doc.idealWidth()), int(self.doc.size().height()))
        index.model().setData(index, s, Qt.SizeHintRole)

    def set_wordwrap(self, on):
        self._wordwrap = on
        mode = QTextOption.WordWrap if on else QTextOption.WrapAtWordBoundaryOrAnywhere

        text_option = QTextOption(self.doc.defaultTextOption())
        text_option.setWrapMode(mode)
        self.doc.setDefaultTextOption(text_option)
        self.parent().viewport().update()
