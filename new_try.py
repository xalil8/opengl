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

        self.rot_x = 0.0
        self.rot_y = 0.0
        self.rot_z = 0.0

        self.scale_x = 5.0
        self.scale_y = 5.0
        self.scale_z = 5.0

        self.translate_x = 0
        self.translate_y = 0 
        self.translate_z = 0

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
        gl.glScale(self.scale_x, self.scale_y, self.scale_z) # second, scale cube
        gl.glRotate(self.rot_x, 1.0, 0.0, 0.0)
        gl.glRotate(self.rot_y, 0.0, 1.0, 0.0)
        gl.glRotate(self.rot_z, 0.0, 0.0, 1.0)

        gl.glTranslate(self.translate_x, self.translate_y, self.translate_z) # first, translate cube center to origin


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

    #rotation functions that take values from line edit 
    def set_rotation_x(self, val):
        self.rot_x = val

    def set_rotation_y(self, val):
        self.rot_y = val

    def set_rotation_z(self, val):
        self.rot_z = val

    #translation functions that take values from line edit 

    def set_translation_x(self,x):
        self.translate_x = x*0.2

    def set_translation_y(self,y):
        self.translate_y = y*0.2

    def set_translation_z(self,z):
        self.translate_z = z *0.2

    def set_scale_x(self,val):
        self.scale_x = val
    
    def set_scale_y(self,val):
        self.scale_y = val

    def set_scale_z(self,val):
        self.scale_z = val

    def reset_All(self):
        self.translate_x= 0
        self.translate_y = 0 
        self.translate_z = 0
        self.rot_x = 0.0
        self.rot_y = 0.0
        self.rot_z = 0.0
        self.scale_x = 5.0
        self.scale_y = 5.0
        self.scale_z = 5.0

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

    #####################################################################

        checkbox = QtWidgets.QCheckBox("Keep Scale\nRatio")
        #checkbox.setChecked(False)

    #####################################################################
        #translation variables
        label_width = 70
        label_with_text = 70
        translation_label_x = QtWidgets.QLabel("X")
        translation_label_x.setFixedSize(label_width, 20)
        self.translation_x = QtWidgets.QLineEdit()
        self.translation_x.setFixedSize(label_with_text, 20)
        self.translation_x.setText("0.0")

        translation_label_y = QtWidgets.QLabel("Y")
        translation_label_y.setFixedSize(label_width, 20)
        self.translation_y = QtWidgets.QLineEdit()
        self.translation_y.setFixedSize(label_with_text, 20)
        self.translation_y.setText("0.0")

        translation_label_z = QtWidgets.QLabel("Z")
        translation_label_z.setFixedSize(label_width, 20)
        self.translation_z = QtWidgets.QLineEdit()
        self.translation_z.setFixedSize(label_with_text, 20)
        self.translation_z.setText("0.0")

        translation_push_but = QtWidgets.QPushButton("Translation", self)
        translation_push_but.setFixedSize(70, 25)
    #####################################################################
    #####################################################################
        rotation_label_x = QtWidgets.QLabel("X")
        rotation_label_x.setFixedSize(label_width, 20)
        self.rotation_x = QtWidgets.QLineEdit()
        self.rotation_x.setFixedSize(label_with_text, 20)
        self.rotation_x.setText("0.0")

        rotation_label_y = QtWidgets.QLabel("Y")
        rotation_label_y.setFixedSize(label_width, 20)
        self.rotation_y = QtWidgets.QLineEdit()
        self.rotation_y.setFixedSize(label_with_text, 20)
        self.rotation_y.setText("0.0")

        rotation_label_z = QtWidgets.QLabel("Z")
        rotation_label_z.setFixedSize(label_width, 20)
        self.rotation_z = QtWidgets.QLineEdit()
        self.rotation_z.setFixedSize(label_width, 20)
        self.rotation_z.setText("0.0")

        rotation_push_but = QtWidgets.QPushButton("Rotation", self)
        rotation_push_but.setFixedSize(70, 25)
    #####################################################################
    #####################################################################
        scale_label_x = QtWidgets.QLabel("X")
        scale_label_x.setFixedSize(label_width, 20)
        self.scale_x = QtWidgets.QLineEdit()
        self.scale_x.setFixedSize(label_with_text, 20)
        self.scale_x.setText("5.0")

        scale_label_y = QtWidgets.QLabel("Y")
        scale_label_y.setFixedSize(label_width, 20)
        self.scale_y = QtWidgets.QLineEdit()
        self.scale_y.setFixedSize(label_with_text, 20)
        self.scale_y.setText("5.0")

        scale_label_z = QtWidgets.QLabel("Z")
        scale_label_z.setFixedSize(label_width, 20)
        self.scale_z = QtWidgets.QLineEdit()
        self.scale_z.setFixedSize(label_width, 20)
        self.scale_z.setText("5.0")

        scale_push_but = QtWidgets.QPushButton("Scale", self)
        scale_push_but.setFixedSize(70, 25)
    #####################################################################
    #####################################################################
        radio_width = 50
        self.mirror_x = QtWidgets.QRadioButton("X")
        self.mirror_x.setFixedSize(radio_width, 20)
        self.mirror_y = QtWidgets.QRadioButton("Y")
        self.mirror_y.setFixedSize(radio_width, 20)
        self.mirror_z = QtWidgets.QRadioButton("Z")
        self.mirror_z.setFixedSize(radio_width, 20)
        self.mirror_push_but = QtWidgets.QPushButton("Mirror", self)
        self.mirror_push_but.setFixedSize(70, 25)

    #####################################################################
    ##################################################################### 
        self.shear_x = QtWidgets.QRadioButton("X")
        self.shear_x.setFixedSize(radio_width, 20)
        self.shear_y = QtWidgets.QRadioButton("Y")
        self.shear_y.setFixedSize(radio_width, 20)
        self.shear_z = QtWidgets.QRadioButton("Z")
        self.shear_z.setFixedSize(radio_width, 20)
        self.shear_push_but = QtWidgets.QPushButton("Shear", self)
        self.shear_push_but.setFixedSize(70, 25)

    #####################################################################
    #####################################################################     
        reset_button = QtWidgets.QPushButton("Reset", self)
        reset_button.setFixedSize(100, 45)


    #####################################################################        
        hbox1 = QtWidgets.QHBoxLayout()
        hbox1.addWidget(self.translation_x)
        hbox1.addWidget(translation_label_x)
        hbox1.addWidget(self.translation_y)
        hbox1.addWidget(translation_label_y)
        hbox1.addWidget(self.translation_z)
        hbox1.addWidget(translation_label_z)
        hbox1.addWidget(translation_push_but)
    #####################################################################
        hbox2 = QtWidgets.QHBoxLayout()
        hbox2.addWidget(self.rotation_x)
        hbox2.addWidget(rotation_label_x)
        hbox2.addWidget(self.rotation_y)
        hbox2.addWidget(rotation_label_y)
        hbox2.addWidget(self.rotation_z)
        hbox2.addWidget(rotation_label_z)
        hbox2.addWidget(rotation_push_but)
    #####################################################################

       
        scale_box = QtWidgets.QVBoxLayout()
        scale_box.addWidget(checkbox)
        scale_box.addWidget(scale_push_but)

        hbox3 = QtWidgets.QHBoxLayout()
        hbox3.addWidget(self.scale_x)
        hbox3.addWidget(scale_label_x)
        hbox3.addWidget(self.scale_y)
        hbox3.addWidget(scale_label_y)
        hbox3.addWidget(self.scale_z)
        hbox3.addWidget(scale_label_z)
        hbox3.addLayout(scale_box)
    #####################################################################
        hbox4 = QtWidgets.QHBoxLayout()
        hbox4.addWidget(self.mirror_x)
        hbox4.addWidget(self.mirror_y)
        hbox4.addWidget(self.mirror_z)
        hbox4.addWidget(self.mirror_push_but)
    #####################################################################
        hbox5 = QtWidgets.QHBoxLayout()
        hbox5.addWidget(self.shear_x)
        hbox5.addWidget(self.shear_y)
        hbox5.addWidget(self.shear_z)
        hbox5.addWidget(self.shear_push_but)
#####################################################################

        radio_gui = QtWidgets.QVBoxLayout()
        radio_gui.addLayout(hbox4)
        radio_gui.addLayout(hbox5)
    #####################################################################
        radio_reset = QtWidgets.QHBoxLayout()
        radio_gui.setAlignment(QtCore.Qt.AlignLeft)
        radio_reset.addLayout(radio_gui)

        radio_reset.addWidget(reset_button)

    #####################################################################
    #####################################################################

        gui_layout.addLayout(hbox1)
        gui_layout.addLayout(hbox2)
        gui_layout.addLayout(hbox3)
        gui_layout.addLayout(radio_reset)
        
        #self.glWidget.set_translation(x=self.move_val_x.text(),y=self.move_val_y.text(),z=self.move_val_z.text())


        def reset_line_edits():
            self.translation_x.setText("0.0")
            self.translation_y.setText("0.0")
            self.translation_z.setText("0.0")

            self.rotation_x.setText("0.0")
            self.rotation_y.setText("0.0")
            self.rotation_z.setText("0.0")

            self.scale_x.setText("5.0")
            self.scale_y.setText("5.0")
            self.scale_z.setText("5.0")

        def func_translation():
            x = self.translation_x.text()
            y = self.translation_y.text()
            z = self.translation_z.text()

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

        def func_rotation():
            x = self.rotation_x.text()
            y = self.rotation_y.text()
            z = self.rotation_z.text()

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
                
            self.glWidget.set_rotation_x(x)
            self.glWidget.set_rotation_y(y)
            self.glWidget.set_rotation_z(z)

        def func_scale():
            x = self.scale_x.text()
            y = self.scale_y.text()
            z = self.scale_z.text()

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



            if checkbox.isChecked() == True:
                print("checked")
                self.scale_y
                avg_scaling = (x + y + z)/3

                self.glWidget.scale_x = avg_scaling
                self.glWidget.scale_y = avg_scaling
                self.glWidget.scale_z = avg_scaling

            else:    
                self.glWidget.set_scale_x(x)
                self.glWidget.set_scale_y(y)
                self.glWidget.set_scale_z(z)


    #TODO: complete this ffunction 
        def func_mirror():
            if self.mirror_x.isChecked():
                x = self.translation_x.text()
                try:
                    x = float(x)
                    
                    if x == 0:
                        x = 5 
                        self.glWidget.set_translation_x(-x)
                        
                    else:
                        self.glWidget.set_translation_x(-x)

                except ValueError:
                    pass


            elif self.mirror_y.isChecked():
                y = self.translation_y.text()
                try:
                    y = float(y)
                    
                    if y == 0:
                        y = 5 
                        self.glWidget.set_translation_y(-y)
                        
                    else:
                        self.glWidget.set_translation_y(-y)

                except ValueError:
                    pass

            elif self.mirror_z.isChecked():
                z = self.translation_z.text()
                try:
                    z = float(z)
                    
                    if z == 0:
                        z = 5 
                        self.glWidget.set_translation_z(-z)
                        
                    else:
                        self.glWidget.set_translation_z(-z)

                except ValueError:
                    pass

        self.mirror_push_but.clicked.connect(func_mirror)
        translation_push_but.clicked.connect(func_translation)
        rotation_push_but.clicked.connect(func_rotation)
        scale_push_but.clicked.connect(func_scale)
        
        reset_button.clicked.connect(self.glWidget.reset_All)
        reset_button.clicked.connect(reset_line_edits)


        

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)

    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
