# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pso_window.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QWidget)
import resource_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(859, 533)
        self.main_widget = QWidget(Form)
        self.main_widget.setObjectName(u"main_widget")
        self.main_widget.setGeometry(QRect(9, 9, 841, 511))
        self.gridLayout = QGridLayout(self.main_widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.body_widget = QWidget(self.main_widget)
        self.body_widget.setObjectName(u"body_widget")
        self.gridLayout_9 = QGridLayout(self.body_widget)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.graph_widget_3 = QWidget(self.body_widget)
        self.graph_widget_3.setObjectName(u"graph_widget_3")
        self.graph_widget_3.setStyleSheet(u"border-right: 2px solid black;\n"
"background-color: rgb(255, 255, 255);")

        self.horizontalLayout_7.addWidget(self.graph_widget_3)

        self.convergence_widget_3 = QWidget(self.body_widget)
        self.convergence_widget_3.setObjectName(u"convergence_widget_3")
        self.convergence_widget_3.setStyleSheet(u"border-left: 2px solid black;\n"
"background-color: rgb(255, 255, 255);")

        self.horizontalLayout_7.addWidget(self.convergence_widget_3)


        self.gridLayout_9.addLayout(self.horizontalLayout_7, 0, 0, 1, 1)

        self.player_widget_3 = QWidget(self.body_widget)
        self.player_widget_3.setObjectName(u"player_widget_3")
        self.player_widget_3.setMinimumSize(QSize(0, 30))
        self.player_widget_3.setMaximumSize(QSize(16777215, 90))
        self.player_widget_3.setStyleSheet(u"\n"
"\n"
"#player_widget {\n"
"\n"
"background-color:  #3498db;\n"
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
        self.parameters_frame_3 = QFrame(self.player_widget_3)
        self.parameters_frame_3.setObjectName(u"parameters_frame_3")
        self.parameters_frame_3.setGeometry(QRect(110, 10, 701, 71))
        self.parameters_frame_3.setFrameShape(QFrame.StyledPanel)
        self.parameters_frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.parameters_frame_3)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.frame_11 = QFrame(self.parameters_frame_3)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setFrameShape(QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QFrame.Raised)
        self.lineEdit_12 = QLineEdit(self.frame_11)
        self.lineEdit_12.setObjectName(u"lineEdit_12")
        self.lineEdit_12.setGeometry(QRect(10, 20, 90, 21))
        self.lineEdit_12.setMinimumSize(QSize(90, 0))
        self.lineEdit_12.setMaximumSize(QSize(90, 16777215))
        self.label_11 = QLabel(self.frame_11)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(10, 0, 47, 13))

        self.horizontalLayout_8.addWidget(self.frame_11)

        self.frame_12 = QFrame(self.parameters_frame_3)
        self.frame_12.setObjectName(u"frame_12")
        self.frame_12.setFrameShape(QFrame.StyledPanel)
        self.frame_12.setFrameShadow(QFrame.Raised)
        self.lineEdit_13 = QLineEdit(self.frame_12)
        self.lineEdit_13.setObjectName(u"lineEdit_13")
        self.lineEdit_13.setGeometry(QRect(10, 20, 90, 21))
        self.lineEdit_13.setMinimumSize(QSize(90, 0))
        self.lineEdit_13.setMaximumSize(QSize(90, 16777215))
        self.label_12 = QLabel(self.frame_12)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(QRect(10, 0, 47, 13))

        self.horizontalLayout_8.addWidget(self.frame_12)

        self.frame_13 = QFrame(self.parameters_frame_3)
        self.frame_13.setObjectName(u"frame_13")
        self.frame_13.setFrameShape(QFrame.StyledPanel)
        self.frame_13.setFrameShadow(QFrame.Raised)
        self.lineEdit_14 = QLineEdit(self.frame_13)
        self.lineEdit_14.setObjectName(u"lineEdit_14")
        self.lineEdit_14.setGeometry(QRect(10, 20, 90, 21))
        self.lineEdit_14.setMinimumSize(QSize(90, 0))
        self.lineEdit_14.setMaximumSize(QSize(90, 16777215))
        self.label_13 = QLabel(self.frame_13)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QRect(10, 0, 47, 13))

        self.horizontalLayout_8.addWidget(self.frame_13)

        self.frame_14 = QFrame(self.parameters_frame_3)
        self.frame_14.setObjectName(u"frame_14")
        self.frame_14.setFrameShape(QFrame.StyledPanel)
        self.frame_14.setFrameShadow(QFrame.Raised)
        self.lineEdit_15 = QLineEdit(self.frame_14)
        self.lineEdit_15.setObjectName(u"lineEdit_15")
        self.lineEdit_15.setGeometry(QRect(10, 20, 90, 21))
        self.lineEdit_15.setMaximumSize(QSize(90, 16777215))
        self.label_14 = QLabel(self.frame_14)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setGeometry(QRect(10, 0, 47, 13))

        self.horizontalLayout_8.addWidget(self.frame_14)

        self.frame_15 = QFrame(self.parameters_frame_3)
        self.frame_15.setObjectName(u"frame_15")
        self.frame_15.setFrameShape(QFrame.StyledPanel)
        self.frame_15.setFrameShadow(QFrame.Raised)
        self.lineEdit_16 = QLineEdit(self.frame_15)
        self.lineEdit_16.setObjectName(u"lineEdit_16")
        self.lineEdit_16.setGeometry(QRect(10, 20, 90, 21))
        self.lineEdit_16.setMaximumSize(QSize(90, 16777215))
        self.label_15 = QLabel(self.frame_15)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setGeometry(QRect(10, 0, 47, 13))

        self.horizontalLayout_8.addWidget(self.frame_15)

        self.pushButton_5 = QPushButton(self.player_widget_3)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setGeometry(QRect(40, 20, 41, 41))
        self.pushButton_5.setStyleSheet(u"border-radius: 50%;")
        icon = QIcon()
        icon.addFile(u":/icons/icons/play-48.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_5.setIcon(icon)
        self.pushButton_5.setIconSize(QSize(20, 20))

        self.gridLayout_9.addWidget(self.player_widget_3, 1, 0, 1, 1)


        self.gridLayout.addWidget(self.body_widget, 0, 0, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label_11.setText(QCoreApplication.translate("Form", u"Population", None))
        self.label_12.setText(QCoreApplication.translate("Form", u"Iterations", None))
        self.label_13.setText(QCoreApplication.translate("Form", u"W", None))
        self.label_14.setText(QCoreApplication.translate("Form", u"C1", None))
        self.label_15.setText(QCoreApplication.translate("Form", u"C2", None))
        self.pushButton_5.setText("")
    # retranslateUi

