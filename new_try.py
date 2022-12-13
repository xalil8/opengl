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
        self.scale = 5.0

        self.translateX = 0
        self.translateY = 0 
        self.translateZ = 0

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
        #gl.glColor3f(1, 0, 0)  #to make sinlge color 
        gl.glTranslate(0.0, 0.0, -50.0) # third, translate cube to specified depth
        gl.glScale(self.scale, self.scale, self.scale) # second, scale cube
        gl.glRotate(self.rotX, 1.0, 0.0, 0.0)
        gl.glRotate(self.rotY, 0.0, 1.0, 0.0)
        gl.glRotate(self.rotZ, 0.0, 0.0, 1.0)

        gl.glTranslate(self.translateX, self.translateY, self.translateZ) # first, translate cube center to origin


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
        self.rotX = np.pi * val*2

    def setRotY(self, val):
        self.rotY = np.pi * val*2

    def setRotZ(self, val):
        self.rotZ = np.pi * val*2

    def set_scale(self,val):
        self.scale = val
    
    def set_translation_x(self,x):
        self.translateX = x* 0.1

    def set_translation_y(self,y):
        self.translateY = y* 0.1

    def set_translation_z(self,z):
        self.translateZ = z * 0.1

    def reset_translation(self):
        self.translateX= 0
        self.translateY = 0 
        self.translateZ = 0
        self.rotX = 0.0
        self.rotY = 0.0
        self.rotZ = 0.0
        self.scale = 5.0

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self) # call the init for the parent class

        self.resize(600, 600)
        self.setWindowTitle("Ahmet's Cube")

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

        slider_x_label = QtWidgets.QLabel("Rotate in X axis")
        slider_x_label.setFixedSize(120, 20)
        slider_y_label = QtWidgets.QLabel("Rotate in Y axis")
        slider_y_label.setFixedSize(120, 20)
        slider_z_label = QtWidgets.QLabel("Rotate in Z axis")
        slider_z_label.setFixedSize(120, 20)

        slider_scale_label = QtWidgets.QLabel("Scaling Cube Size")
        slider_scale_label.setFixedSize(120, 20)


        sliderX = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        sliderX.valueChanged.connect(lambda val: self.glWidget.setRotX(val))
        sliderX.setTickPosition(QtWidgets.QSlider.TicksBelow)

        sliderY = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        sliderY.valueChanged.connect(lambda val: self.glWidget.setRotY(val))
        sliderY.setTickPosition(QtWidgets.QSlider.TicksBelow)

        sliderZ = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        sliderZ.valueChanged.connect(lambda val: self.glWidget.setRotZ(val))
        sliderZ.setTickPosition(QtWidgets.QSlider.TicksBelow)      


        slider_scale = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        slider_scale.valueChanged.connect(lambda val: self.glWidget.set_scale(val))
        slider_scale.setRange(5,25)
        slider_scale.setValue(0)
        slider_scale.setTickPosition(QtWidgets.QSlider.TicksBelow)


        move_label_x = QtWidgets.QLabel("X axis")
        move_label_x.setFixedSize(60, 20)
        self.move_val_x = QtWidgets.QLineEdit()
        self.move_val_x.setFixedSize(60, 20)

        move_label_y = QtWidgets.QLabel("Y axis")
        move_label_y.setFixedSize(60, 20)
        self.move_val_y = QtWidgets.QLineEdit()
        self.move_val_y.setFixedSize(60, 20)

        move_label_z = QtWidgets.QLabel("Z axis")
        move_label_z.setFixedSize(60, 20)
        self.move_val_z = QtWidgets.QLineEdit()
        self.move_val_z.setFixedSize(60, 20)


        push_button = QtWidgets.QPushButton("Apply Translation", self)
        push_button.setFixedSize(100, 45)

        reset_button = QtWidgets.QPushButton("Reset", self)
        reset_button.setFixedSize(100, 45)


        hbox5 = QtWidgets.QVBoxLayout()
        hbox5.addWidget(slider_x_label)
        hbox5.addWidget(sliderX)
        hbox5.addWidget(slider_y_label)
        hbox5.addWidget(sliderY) 

        hbox6 = QtWidgets.QVBoxLayout()
        hbox6.addWidget(slider_z_label)
        hbox6.addWidget(sliderZ)
        hbox6.addWidget(slider_scale_label)
        hbox6.addWidget(slider_scale)     

        hbox7 = QtWidgets.QHBoxLayout() 
        hbox7.addLayout(hbox5) 
        hbox7.addLayout(hbox6) 
        # Create a horizontal layout to hold the label and input field
        hbox1 = QtWidgets.QVBoxLayout()
        hbox1.addWidget(move_label_x)
        hbox1.addWidget(move_label_y)
        hbox1.addWidget(move_label_z)

        # Create a second horizontal layout to hold the label and input field
        hbox2 = QtWidgets.QVBoxLayout()
        hbox2.addWidget(self.move_val_x)
        hbox2.addWidget(self.move_val_y)
        hbox2.addWidget(self.move_val_z)


        hbox4 = QtWidgets.QHBoxLayout()
        hbox4.addLayout(hbox1)
        hbox4.addLayout(hbox2)
        hbox4.addWidget(push_button)
        hbox4.addWidget(reset_button)


        gui_layout.addLayout(hbox7)
        gui_layout.addLayout(hbox4)

        #self.glWidget.set_translation(x=self.move_val_x.text(),y=self.move_val_y.text(),z=self.move_val_z.text())
        

        def this_func_work():
            x = self.move_val_x.text()
            y = self.move_val_y.text()
            z = self.move_val_z.text()

            try:
                x = float(x)
            except ValueError:
                x = 0
            try:
                y = float(y)
            except ValueError:
                y = 0
            try:
                z = float(z)
            except ValueError:
                z = 0
                
            self.glWidget.set_translation_x(x)
            self.glWidget.set_translation_y(y)
            self.glWidget.set_translation_z(z)

        push_button.clicked.connect(this_func_work)
        reset_button.clicked.connect(self.glWidget.reset_translation)



if __name__ == '__main__':
    try:
        app = QtWidgets.QApplication(sys.argv)

        win = MainWindow()
        win.show()
        sys.exit(app.exec_())
    except:
        sys.exit(app.exec_())