# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'problem_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import random
from matplotlib.collections import LineCollection
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Qt5Agg')


from static import resource_rc

class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=1, height=1, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(859, 533)
        self.main_widget = QtWidgets.QWidget(Form)
        self.main_widget.setGeometry(QtCore.QRect(9, 9, 841, 511))
        self.main_widget.setObjectName("main_widget")
        self.gridLayout = QtWidgets.QGridLayout(self.main_widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.body_widget = QtWidgets.QWidget(self.main_widget)
        self.body_widget.setObjectName("body_widget")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.body_widget)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.convergence_widget = QtWidgets.QWidget(self.body_widget)
        self.convergence_widget.setStyleSheet("border: 2px solid black;\n"
"background-color: rgb(255, 255, 255);")
        self.convergence_widget.setObjectName("convergence_widget")
        
        
        self.convergence_canvas = MplCanvas(self.convergence_widget, width=1, height=1, dpi=100)
        self.convergence_canvas.setGeometry(QtCore.QRect(0, 0, self.convergence_widget.width(), self.convergence_widget.height()))
        self.convergence_layout = QtWidgets.QHBoxLayout(self.convergence_widget)
        self.convergence_layout.addWidget(self.convergence_canvas)
        

        self.horizontalLayout.addWidget(self.convergence_widget)
        self.gridLayout_9.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.player_widget = QtWidgets.QWidget(self.body_widget)
        self.player_widget.setMinimumSize(QtCore.QSize(0, 30))
        self.player_widget.setMaximumSize(QtCore.QSize(16777215, 90))
        self.player_widget.setStyleSheet("\n"
"\n"
"#player_widget {\n"
"\n"
"background-color:  #00fa9a;\n"
"  border: 1px solid #3498db;\n"
"  display: flex;\n"
"  justify-content: center;\n"
"  align-items: center;\n"
"  font-size: 18px;\n"
"border-radius: 15px;\n"
"}\n"
"\n"
"#player_widget QLineEdit {\n"
"                background-color: #f2f2f2;\n"
"                border: 1px solid #ccc;\n"
"                border-radius: 5px;\n"
"                padding: 2px;\n"
"                font-size: 14px;\n"
"                color: #333;\n"
"  }\n"
"            \n"
"#player_widget  QPushButton{\n"
"  width: 60px;\n"
"  height: 60px;\n"
"  background-color: #a4a5a3;\n"
"  border-radius: 50%;\n"
"  display: flex;\n"
"  justify-content: center;\n"
"border-radius: 50%;\n"
"  align-items: center;\n"
"  cursor: pointer;\n"
"  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);\n"
"} ")
        self.player_widget.setObjectName("player_widget")
        self.parameters_frame = QtWidgets.QFrame(self.player_widget)
        self.parameters_frame.setGeometry(QtCore.QRect(110, 10, 701, 71))
        self.parameters_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.parameters_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.parameters_frame.setObjectName("parameters_frame")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.parameters_frame)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.frame = QtWidgets.QFrame(self.parameters_frame)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.lineEdit = QtWidgets.QLineEdit(self.frame)
        self.lineEdit.setGeometry(QtCore.QRect(10, 20, 90, 21))
        self.lineEdit.setMinimumSize(QtCore.QSize(90, 0))
        self.lineEdit.setMaximumSize(QtCore.QSize(90, 16777215))
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(10, 0, 91, 16))
        self.label.setObjectName("label")
        self.horizontalLayout_8.addWidget(self.frame)
        self.frame_2 = QtWidgets.QFrame(self.parameters_frame)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.frame_2)
        self.lineEdit_2.setGeometry(QtCore.QRect(10, 20, 90, 21))
        self.lineEdit_2.setMinimumSize(QtCore.QSize(90, 0))
        self.lineEdit_2.setMaximumSize(QtCore.QSize(90, 16777215))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_2 = QtWidgets.QLabel(self.frame_2)
        self.label_2.setGeometry(QtCore.QRect(10, 0, 47, 13))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_8.addWidget(self.frame_2)
        self.pushButton = QtWidgets.QPushButton(self.player_widget)
        self.pushButton.setGeometry(QtCore.QRect(40, 20, 41, 41))
        self.pushButton.setStyleSheet("border-radius: 50%;")
        self.pushButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/play-48.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QtCore.QSize(20, 20))
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_9.addWidget(self.player_widget, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.body_widget, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "No. Vehicles"))
        self.label_2.setText(_translate("Form", "Capacity"))
