from PyQt5 import QtCore # core Qt functionality, QtWidgets
from PyQt5 import QtGui # extends QtCore with GUI functionality, QtWidgets
from PyQt5 import QtOpenGL # provides QGLWidget, QtWidgets,a special OpenGL QWidget)
from PyQt5 import QtWidgets
import OpenGL.GL as gl # python wrapping of OpenGL
from OpenGL import GLU # OpenGL Utility Library, extends OpenGL functionality
import sys # we'll need this later to run our Qt application

from OpenGL.arrays import vbo
import numpy as np

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self) # call the init for the parent class

        self.resize(600, 600)
        self.setWindowTitle("halil's Cube")

        self.initGUI()


    def initGUI(self):
        central_widget = QtWidgets.QWidget()
        gui_layout = QtWidgets.QVBoxLayout()
        central_widget.setLayout(gui_layout)
        self.setCentralWidget(central_widget)



        move_label_x = QtWidgets.QLabel("X axis")
        #move_label_x.setAlignment(QtCore.Qt.AlignLeft)
        move_label_x.setFixedSize(60, 20)
        self.move_x = QtWidgets.QLineEdit()
        self.move_x.setFixedSize(60, 20)

        move_label_y = QtWidgets.QLabel("Y axis")
        move_label_y.setFixedSize(60, 20)
        self.move_y = QtWidgets.QLineEdit()
        self.move_y.setFixedSize(60, 20)

        move_label_z = QtWidgets.QLabel("Z axis")
        move_label_z.setFixedSize(60, 20)
        self.move_z = QtWidgets.QLineEdit()
        self.move_z.setFixedSize(60, 20)


        push_button_x = QtWidgets.QPushButton("Apply Translation", self)
        push_button_x.setFixedSize(100, 45)



        # Create a horizontal layout to hold the label and input field
        hbox1 = QtWidgets.QVBoxLayout()
        hbox1.addWidget(move_label_x)
        hbox1.addWidget(move_label_y)
        hbox1.addWidget(move_label_z)

        # Create a second horizontal layout to hold the label and input field
        hbox2 = QtWidgets.QVBoxLayout()
        hbox2.addWidget(self.move_x)
        hbox2.addWidget(self.move_y)
        hbox2.addWidget(self.move_z)


        hbox4 = QtWidgets.QHBoxLayout()
        hbox4.addLayout(hbox1)
        hbox4.addLayout(hbox2)
        hbox4.addWidget(push_button_x)

        gui_layout.addLayout(hbox4)



        
        push_button_x.clicked.connect(self.apply_translation)

    def apply_translation(self):
    # Get the text from the line edit widget
        try:
            x_val =float(self.move_x.text())
            y_val =float(self.move_y.text())
            z_val = float(self.move_z.text())
        except:
            raise TypeError
            
        print(x_val+y_val + z_val)
   



if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)

    win = MainWindow()
    win.show()

    sys.exit(app.exec_())