from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from OpenGL.GLU import *

import sys
from PyQt6 import QtCore, QtGui, QtWidgets,QtOpenGL, QtOpenGLWidgets
from PySide6 import *

from OpenGL.arrays import vbo
import numpy as np
import OpenGL.GL as gl
import OpenGL.GLU as GLU
cubeVtxList = [
    [0.0, 0.0, 0.0],
    [1.0, 0.0, 0.0],
    [1.0, 1.0, 0.0],
    [0.0, 1.0, 0.0],
    [0.0, 0.0, 1.0],
    [1.0, 0.0, 1.0],
    [1.0, 1.0, 1.0],
    [0.0, 1.0, 1.0]]
        
cubeClrList = [
    [0.0, 0.0, 0.0],
    [1.0, 0.0, 0.0],
    [1.0, 1.0, 0.0],
    [0.0, 1.0, 0.0],
    [0.0, 0.0, 1.0],
    [1.0, 0.0, 1.0],
    [1.0, 1.0, 1.0],
    [0.0, 1.0, 1.0]]
        
cubeIdxList = [
    0, 1, 2, 3,
    3, 2, 6, 7,
    1, 0, 4, 5,
    2, 1, 5, 6,
    0, 3, 7, 4,
    7, 6, 5, 4 ]

class GLWidget(QtOpenGLWidgets.QOpenGLWidget):
    def __init__(self, parent=None):
        self.parent = parent
        QtOpenGLWidgets.QOpenGLWidget.__init__(self, parent)

    def initializeGL(self):
        gl.glClearColor(0,0,255,0)
        gl.glEnable(gl.GL_DEPTH_TEST) # enable depth testing
        self.initGeometry()

        self.rotX = 0.0
        self.rotY = 0.0
        self.rotZ = 0.0

    def resizeGL(self, width, height):
        gl.glViewport(0, 0, width, height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        aspect = width / float(height)

        GLU.gluPerspective(45.0, aspect, 1.0, 100.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)

    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        gl.glPushMatrix()

        gl.glTranslate(0.0, 0.0, -50.0) # third, translate cube to specified depth
        gl.glScale(20.0, 20.0, 20.0) # second, scale cube
        gl.glRotate(self.rotX, 1.0, 0.0, 0.0)
        gl.glRotate(self.rotY, 0.0, 1.0, 0.0)
        gl.glRotate(self.rotZ, 0.0, 0.0, 1.0)
        gl.glTranslate(-0.5, -0.5, -0.5) # first, translate cube center to origin

        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        gl.glEnableClientState(gl.GL_COLOR_ARRAY)

        self.vertVbo.bind()
        gl.glVertexPointer(3, gl.GL_FLOAT, 0, None)
        self.colorVbo.bind()
        gl.glColorPointer(3, gl.GL_FLOAT, 0, None)

        gl.glDrawElements(gl.GL_QUADS, len(self.cubeIdxArray), gl.GL_UNSIGNED_INT, self.cubeIdxArray)

        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)
        gl.glDisableClientState(gl.GL_COLOR_ARRAY)

        gl.glPopMatrix() # restore the previous modelview matrix

    def initGeometry(self):
        self.cubeVtxArray = np.array(cubeVtxList)
        self.vertVbo = vbo.VBO(np.reshape(self.cubeVtxArray, (1, -1)).astype(np.float32))
        self.vertVbo.bind()
        self.cubeClrArray = np.array(cubeClrList)
        self.colorVbo = vbo.VBO(np.reshape(self.cubeClrArray, (1, -1)).astype(np.float32))
        self.colorVbo.bind()
        self.cubeIdxArray = np.array(cubeIdxList,dtype=np.uint32)

    def setRotX(self, val):
        self.rotX = val

    def setRotY(self, val):
        self.rotY = val

    def setRotZ(self, val):
        self.rotZ = val


class MainWindow(QtWidgets.QMainWindow):


    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.resize(500, 500)
        self.setWindowTitle('titolo')
        self.glWidget = GLWidget(self)
        self.initGui()
        self.timer = QtCore.QTimer()
        self.timer.setInterval(20)
        self.timer.timeout.connect(self.glWidget.update)
        self.timer.start()
    
    def initGui(self):
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

    sys.exit(app.exec_())