from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from OpenGL.GLU import *

import sys
from PyQt6 import QtCore, QtGui, QtWidgets,QtOpenGL, QtOpenGLWidgets
from PySide6 import *

from OpenGL.arrays import vbo
import numpy as np


class GLWidget(QtOpenGLWidgets.QOpenGLWidget):
    def __init__(self, parent=None):
        self.parent = parent
        QtOpenGLWidgets.QOpenGLWidget.__init__(self, parent)

    def initializeGL(self):
        glClearColor(0,0,255,100)    # initialize the screen to blue
        glEnable(GL_DEPTH_TEST)                  # enable depth testing

        QtOpenGLWidgets.QOpenGLWidget.Color

    def resizeGL(self, width, height):
        glViewport(0,0,width,height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = width / float(height)
        gluPerspective(45.0, aspect, 1.0, 100.0)
        glMatrixMode(GL_MODELVIEW)


    






class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)    # call the init for the parent class

        self.resize(300, 300)
        self.setWindowTitle('ulusun çakallari')

        glWidget = GLWidget(self)
        self.setCentralWidget(glWidget)


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)

    win = MainWindow()
    win.show()
    print("///////////////////////////////////////////////")
    sys.exit(app.exec())
