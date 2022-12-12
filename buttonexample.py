import sys
from PyQt5 import QtCore, QtGui


class TextEditorDlg(QtGui.QDialog):
    def __init__(self, parent=None):
        super(TextEditorDlg, self).__init__(parent)
        self.resize(500, 400)

        self.button = QtGui.QPushButton(self)
        self.lineEdit = QtGui.QLineEdit(self)
        self.textEdit = QtGui.QTextEdit(self)

        self.button_layout = QtGui.QHBoxLayout()
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.button)
        self.button_layout.addStretch()

        self.grid = QtGui.QGridLayout(self)

        self.grid.addLayout(self.button_layout, 0, 0)
        self.grid.addWidget(self.lineEdit, 1, 0)
        self.grid.addWidget(self.textEdit, 2, 0)

        # Alternative using QVBoxLayout:
        #self.layout = QtGui.QVBoxLayout(self)
        #self.layout.addLayout(self.button_layout)
        #self.layout.addWidget(self.line_edit)
        #self.layout.addWidget(self.text_edit)



if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    myapp = TextEditorDlg()
    myapp.show()
    sys.exit(app.exec_())