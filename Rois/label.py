from PyQt4.QtGui import QGraphicsTextItem
from PyQt4.QtCore import Qt


class LabelItem(QGraphicsTextItem):
    # todo: Change the delegate to a combobox
    def __init__(self, text=None, parent=None, scene=None):
        super(LabelItem, self).__init__(text, parent, scene)
        self.setFlags(QGraphicsTextItem.ItemIsMovable | QGraphicsTextItem.ItemIsSelectable |
                      QGraphicsTextItem.ItemIsFocusable)
        self.setTextInteractionFlags(Qt.NoTextInteraction)

    def mouseDoubleClickEvent(self, event):
        self.setTextInteractionFlags(Qt.TextEditorInteraction)
        self.setFocus(Qt.MouseFocusReason)
        super(LabelItem, self).mouseDoubleClickEvent(event)
    #     activate editing

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            print "exit editing"
            self.clearFocus()
            return
        super(LabelItem, self).keyPressEvent(event)

    def focusOutEvent(self, event):
        c = self.textCursor()
        c.clearSelection()
        self.setTextCursor(c)
        self.setTextInteractionFlags(Qt.NoTextInteraction)
        super(LabelItem, self).focusOutEvent(event)
