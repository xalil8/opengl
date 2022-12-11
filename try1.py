from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QSurfaceFormat
from OpenGL.GL import *
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Set up the OpenGL format
        format = QSurfaceFormat()
        format.setVersion(3, 3)
        format.setProfile(QSurfaceFormat.CoreProfile)
        QSurfaceFormat.setDefaultFormat(format)

        # Create the OpenGL widget
        self.glWidget = GLWidget()
        self.setCentralWidget(self.glWidget)

        # Set the window title
        self.setWindowTitle("PyQt5 and OpenGL Example")

class GLWidget(QtWidgets.QOpenGLWidget):
    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)

    def initializeGL(self):
        # Set the clear color to black
        glClearColor(0, 0, 0, 1)

    def paintGL(self):
        vertices = ((-1, -1, -1), (-1, 1, -1), (-1, 1, 1), (-1, -1, 1), (1, -1, -1), (1, 1, -1), (1, 1, 1), (1, -1, 1))
        edges = ((0, 1), (0, 3), (0, 4), (1, 2), (1, 5), (2, 3), (2, 6), (3, 7), (4, 5), (4, 7), (5, 6), (6, 7))
        faces = ((0, 1, 2 , 3),(4,  5, 6, 7),(0, 4, 7, 3),(1, 5, 6, 2),(2, 6, 7, 3),(1, 5, 4, 0))

        # Clear the screen with the clear color
        glClear(GL_COLOR_BUFFER_BIT)
        glBegin(GL_QUADS)
        for face in faces:
            for vertex in face:
                glColor3fv((1, 1, 1))
                glVertex3fv(vertices[vertex])
        glEnd()

        glBegin(GL_LINES)
        glColor3fv((150, 150, 150))
        for edge in edges:
            for vertex in edge:
                glVertex3fv(vertices[vertex])
        glEnd()

    def resizeGL(self, width, height):
        # Set the viewport
        glViewport(0, 0, width, height)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
