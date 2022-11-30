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
        glClearColor(0,0,255,100)   # initialize the screen to blue
        glEnable(GL_DEPTH_TEST) 

        self.initGeometry()
        self.rotX = 0.0
        self.rotY = 0.0
        self.rotZ = 0.0
    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = width / float(height)
        gluPerspective(45.0, aspect, 1.0, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix() # push the current matrix to the current stack

        glTranslate(0.0, 0.0, -50.0) # third, translate cube to specified depth
        glScale(20.0, 20.0, 20.0) # second, scale cube
        glRotate(self.rotX, 1.0, 0.0, 0.0)
        glRotate(self.rotY, 0.0, 1.0, 0.0)
        glRotate(self.rotZ, 0.0, 0.0, 1.0)
        glTranslate(-0.5, -0.5, -0.5) # first, translate cube center to origin

        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)

        glVertexPointer(3, GL_FLOAT, 0, self.vertVBO)
        glColorPointer(3, GL_FLOAT, 0, self.colorVBO)

        glDrawElements(GL_QUADS, len(self.cubeIdxArray), GL_UNSIGNED_INT, self.cubeIdxArray)

        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)

        glPopMatrix() # restore the previous modelview matrix

        
    def initGeometry(self):
        self.cubeVtxArray = np.array(
        [[0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
        [1.0, 1.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
        [1.0, 0.0, 1.0],
        [1.0, 1.0, 1.0],
        [0.0, 1.0, 1.0]])
        self.vertVBO = vbo.VBO(np.reshape(self.cubeVtxArray,(1, -1)).astype(np.float32))
        self.vertVBO.bind()

        self.cubeClrArray = np.array(
        [[0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
        [1.0, 1.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0],
        [1.0, 0.0, 1.0],
        [1.0, 1.0, 1.0],
        [0.0, 1.0, 1.0 ]])
        self.colorVBO = vbo.VBO(np.reshape(self.cubeClrArray,(1, -1)).astype(np.float32))
        self.colorVBO.bind()

        self.cubeIdxArray = np.array(
        [0, 1, 2, 3,
        3, 2, 6, 7,
        1, 0, 4, 5,
        2, 1, 5, 6,
        0, 3, 7, 4,
        7, 6, 5, 4 ])
    def setRotX(self, val):
        self.rotX = np.pi * val

    def setRotY(self, val):
        self.rotY = np.pi * val

    def setRotZ(self, val):
        self.rotZ = np.pi * val

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)    # call the init for the parent class

        self.resize(300, 300)
        self.setWindowTitle('ulusun çakallari')

        glWidget = GLWidget(self)
        self.setCentralWidget(glWidget)
        self.glWidget = GLWidget(self)
        self.initGUI()

        timer = QtCore.QTimer(self)
        timer.setInterval(20) # period, in milliseconds
        timer.timeout.connect(self.glWidget.update)
        timer.start()

    def initGUI(self):
        central_widget = QtWidgets.QWidget()
        gui_layout = QtWidgets.QVBoxLayout()
        central_widget.setLayout(gui_layout)

        self.setCentralWidget(central_widget)

        gui_layout.addWidget(self.glWidget)

        sliderX = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        sliderX.valueChanged.connect(lambda val: self.glWidget.setRotX(val))

        sliderY = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        sliderY.valueChanged.connect(lambda val: self.glWidget.setRotY(val))

        sliderZ = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        sliderZ.valueChanged.connect(lambda val: self.glWidget.setRotZ(val))

        gui_layout.addWidget(sliderX)
        gui_layout.addWidget(sliderY)
        gui_layout.addWidget(sliderZ)

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)

    win = MainWindow()
    win.show()
    print("///////////////////////////////////////////////")
    sys.exit(app.exec_())
