from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from OpenGL.GLU import *

import sys
from PyQt6 import QtCore, QtGui, QtWidgets,QtOpenGL, QtOpenGLWidgets
from PySide6 import *

from OpenGL.arrays import vbo
import numpy as np


verts = (
 (1, -1, -1),
 (1, 1, -1),
 (-1, 1, -1),
 (-1, -1, -1),
 (1, -1, 1),
 (1, 1, 1),
 (-1, -1, 1),
 (-1, 1, 1)
 )

edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )

surfaces = (
    (0,1,2,3),
    (3,2,7,6),
    (6,7,5,4),
    (4,5,1,0),
    (1,5,7,2),
    (4,0,3,6)

    )

colors = (
    (1,1,1),
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (1,1,0),
    (1,0,1),
    )

class GLWidget(QtOpenGLWidgets.QOpenGLWidget):
    def __init__(self, parent=None):
        self.parent = parent
        QtOpenGLWidgets.QOpenGLWidget.__init__(self, parent)

    def initializeGL(self):
        glClearColor(0,0,255,100)   # initialize the screen to blue

        glEnable(GL_DEPTH_TEST) 

    def resizeGL(self, width, height):
        glViewport(0,0,width,height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = width / float(height)
        gluPerspective(45.0, aspect, 1.0, 100.0)
        glMatrixMode(GL_MODELVIEW)


    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glPushMatrix()    # push the current matrix to the current stack

        glTranslate(0.0, 0.0, -50.0)    # third, translate cube to specified depth
        glScale(20.0, 20.0, 20.0)       # second, scale cube
        glTranslate(-0.5, -0.5, -0.5)   # first, translate cube center to origin

        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)

        glVertexPointer(3, GL_FLOAT, 0, self.vertVBO)
        glColorPointer(3, GL_FLOAT, 0, self.colorVBO)
        glDrawElements(GL_QUADS, len(self.cubeIdxArray), GL_UNSIGNED_INT, self.cubeIdxArray)

        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)
        glPopMatrix()    # restore the previous modelview matrix

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



"""    def cube(self):
        glBegin(GL_QUADS)
        for surface in surfaces:
            x = 0
            for vertex in surface:
                x += 1
                glColor3fv(colors[x])
                glVertex3fv(verts[vertex])
        glEnd()

        
        glBegin(GL_LINES)
        for edge in edges:
            for vertex in edge:
                glVertex3fv(verts[vertex])
        glEnd()"""


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)    # call the init for the parent class

        self.resize(300, 300)
        self.setWindowTitle('ulusun çakallari')

        glWidget = GLWidget(self)
        self.setCentralWidget(glWidget)
        timer = QtCore.QTimer(self)
        timer.setInterval(20)   # period, in milliseconds
        timer.timeout.connect(glWidget.update)
        timer.start()


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)

    win = MainWindow()
    win.show()
    print("///////////////////////////////////////////////")
    sys.exit(app.exec_())
