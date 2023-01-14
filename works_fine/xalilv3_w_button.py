from PyQt5 import QtCore # core Qt functionality, QtWidgets
from PyQt5 import QtGui # extends QtCore with GUI functionality, QtWidgets
from PyQt5 import QtOpenGL # provides QGLWidget, QtWidgets,a special OpenGL QWidget)
from PyQt5 import QtWidgets
import OpenGL.GL as gl # python wrapping of OpenGL
from OpenGL import GLU # OpenGL Utility Library, extends OpenGL functionality
import sys # we'll need this later to run our Qt application

from OpenGL.arrays import vbo
import numpy as np


class GLWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent=None):
        self.parent = parent
        QtOpenGL.QGLWidget.__init__(self, parent)

    def initializeGL(self):
        self.qglClearColor(QtGui.QColor(0, 153, 153)) # to adjust bacground
        gl.glEnable(gl.GL_DEPTH_TEST) # enable depth testing

        self.initGeometry()

        self.rotX = 0.0
        self.rotY = 0.0
        self.rotZ = 0.0
        self.scale = 15.0
    def resizeGL(self, width, height):

        gl.glViewport(0, 0, width, height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        aspect = width / float(height)

        GLU.gluPerspective(45.0, aspect, 1.0, 100.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)

    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        gl.glPushMatrix() # push the current matrix to the current stack
        gl.glColor3f(1, 0, 0)  #to make sinlge color 
        gl.glTranslate(0.0, 0.0, -50.0) # third, translate cube to specified depth
        gl.glScale(self.scale, self.scale, self.scale) # second, scale cube
        gl.glRotate(self.rotX, 1.0, 0.0, 0.0)
        gl.glRotate(self.rotY, 0.0, 1.0, 0.0)
        gl.glRotate(self.rotZ, 0.0, 0.0, 1.0)
        gl.glTranslate(-0.5, -0.5, -0.5) # first, translate cube center to origin

        #gl.glTranslate(0.2,0.2,0.2)
        
        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        gl.glEnableClientState(gl.GL_COLOR_ARRAY)

        gl.glVertexPointer(3, gl.GL_FLOAT, 0, self.vertVBO)
        gl.glColorPointer(3, gl.GL_FLOAT, 0, self.colorVBO)
        gl.glDrawElements(gl.GL_QUADS, len(self.cubeIdxArray), gl.GL_UNSIGNED_INT, self.cubeIdxArray)

        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)
        gl.glDisableClientState(gl.GL_COLOR_ARRAY)

        gl.glPopMatrix() # restore the previous modelview matrix

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
        print("resize worked\n1")
        self.rotX = np.pi * val

    def setRotY(self, val):
        self.rotY = np.pi * val

    def setRotZ(self, val):
        self.rotZ = np.pi * val

    def set_scale(self,val):
        self.scale = val


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self) # call the init for the parent class

        self.resize(600, 600)
        self.setWindowTitle("halil's Cube")

        self.glWidget = GLWidget(self)
        self.initGUI()

        timer = QtCore.QTimer(self)
        timer.setInterval(20) # period, in milliseconds
        timer.timeout.connect(self.glWidget.updateGL)
        timer.start()

    def initGUI(self):
        central_widget = QtWidgets.QWidget()
        gui_layout = QtWidgets.QVBoxLayout()
        central_widget.setLayout(gui_layout)
        self.setCentralWidget(central_widget)


        gui_layout.addWidget(self.glWidget)

        sliderX = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        sliderX.valueChanged.connect(lambda val: self.glWidget.setRotX(val))

        sliderY = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        sliderY.valueChanged.connect(lambda val: self.glWidget.setRotY(val))

        sliderZ = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        sliderZ.valueChanged.connect(lambda val: self.glWidget.setRotZ(val))
        sliderZ.setTickPosition(QtWidgets.QSlider.TicksBelow)       

        slider_scale = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        slider_scale.valueChanged.connect(lambda val: self.glWidget.set_scale(val))
        slider_scale.setRange(5,25)
        slider_scale.setValue(15)
        slider_scale.setTickPosition(QtWidgets.QSlider.TicksBelow)

        
        move_label_x = QtWidgets.QLabel("X axis")
        move_label_x.setAlignment(QtCore.Qt.AlignLeft)
        move_label_x.setFixedSize(60, 20)
        move_x = QtWidgets.QLineEdit()
        move_x.setFixedSize(60, 20)

        move_label_y = QtWidgets.QLabel("Y axis")
        move_label_y.setFixedSize(60, 20)
        move_y = QtWidgets.QLineEdit()
        move_y.setFixedSize(60, 20)

        move_label_z = QtWidgets.QLabel("Z axis")
        move_label_z.setFixedSize(60, 20)
        move_z = QtWidgets.QLineEdit()
        move_z.setFixedSize(60, 20)


        push_button_x = QtWidgets.QPushButton("X Coordinate", self)
        push_button_x.setGeometry(200,200,80,40) # (x,y) (w,h)

        gui_layout.addWidget(sliderX)
        gui_layout.addWidget(sliderY)
        gui_layout.addWidget(sliderZ)
        gui_layout.addWidget(slider_scale)
        

        gui_layout.addWidget(move_label_x)
        gui_layout.addWidget(move_x)

        gui_layout.addWidget(move_label_y)
        gui_layout.addWidget(move_y)

        gui_layout.addWidget(move_label_z)
        gui_layout.addWidget(move_z)


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)

    win = MainWindow()
    win.show()

    sys.exit(app.exec_())