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

        rotation_label_y = QtWidgets.QLabel("Y")
        rotation_label_y.setFixedSize(label_width, 20)
        self.rotation_y = QtWidgets.QLineEdit()
        self.rotation_y.setFixedSize(label_with_text, 20)

        rotation_label_z = QtWidgets.QLabel("Z")
        rotation_label_z.setFixedSize(label_width, 20)
        self.rotation_z = QtWidgets.QLineEdit()
        self.rotation_z.setFixedSize(label_width, 20)

        rotation_push_but = QtWidgets.QPushButton("Rotation", self)
        rotation_push_but.setFixedSize(70, 25)
    #####################################################################
    #####################################################################
        scale_label_x = QtWidgets.QLabel("X")
        scale_label_x.setFixedSize(label_width, 20)
        self.scale_x = QtWidgets.QLineEdit()
        self.scale_x.setFixedSize(label_with_text, 20)

        scale_label_y = QtWidgets.QLabel("Y")
        scale_label_y.setFixedSize(label_width, 20)
        self.scale_y = QtWidgets.QLineEdit()
        self.scale_y.setFixedSize(label_with_text, 20)

        scale_label_z = QtWidgets.QLabel("Z")
        scale_label_z.setFixedSize(label_width, 20)
        self.scale_z = QtWidgets.QLineEdit()
        self.scale_z.setFixedSize(label_width, 20)

        self.scale_push_but = QtWidgets.QPushButton("Scale", self)
        self.scale_push_but.setFixedSize(70, 25)
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
        hbox3 = QtWidgets.QHBoxLayout()
        hbox3.addWidget(self.scale_x)
        hbox3.addWidget(scale_label_x)
        hbox3.addWidget(self.scale_y)
        hbox3.addWidget(scale_label_y)
        hbox3.addWidget(self.scale_z)
        hbox3.addWidget(scale_label_z)
        hbox3.addWidget(self.scale_push_but)         
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

# TODO:

        def this_func_work():
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

        translation_push_but.clicked.connect(this_func_work)
        reset_button.clicked.connect(self.glWidget.reset_translation)

