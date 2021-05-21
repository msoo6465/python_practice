# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Logon.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import Logon_rc

class Ui_Logon(object):
    def setupUi(self, Logon):
        if not Logon.objectName():
            Logon.setObjectName(u"Logon")
        Logon.resize(328, 159)
        icon = QIcon()
        icon.addFile(u":/imges/ok.png/images/ok.png", QSize(), QIcon.Normal, QIcon.Off)
        Logon.setWindowIcon(icon)
        self.verticalLayout = QVBoxLayout(Logon)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.lineEditPW = QLineEdit(Logon)
        self.lineEditPW.setObjectName(u"lineEditPW")
        self.lineEditPW.setEchoMode(QLineEdit.Password)

        self.gridLayout.addWidget(self.lineEditPW, 1, 1, 1, 1)

        self.labelId = QLabel(Logon)
        self.labelId.setObjectName(u"labelId")

        self.gridLayout.addWidget(self.labelId, 0, 0, 1, 1)

        self.labelPW = QLabel(Logon)
        self.labelPW.setObjectName(u"labelPW")

        self.gridLayout.addWidget(self.labelPW, 1, 0, 1, 1)

        self.lineEditId = QLineEdit(Logon)
        self.lineEditId.setObjectName(u"lineEditId")

        self.gridLayout.addWidget(self.lineEditId, 0, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.buttonOk = QPushButton(Logon)
        self.buttonOk.setObjectName(u"buttonOk")
        self.buttonOk.setIcon(icon)

        self.gridLayout_2.addWidget(self.buttonOk, 0, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout_2)


        self.retranslateUi(Logon)

        QMetaObject.connectSlotsByName(Logon)
    # setupUi

    def retranslateUi(self, Logon):
        Logon.setWindowTitle(QCoreApplication.translate("Logon", u"Log on", None))
        self.labelId.setText(QCoreApplication.translate("Logon", u"&ID               : ", None))
        self.labelPW.setText(QCoreApplication.translate("Logon", u"&PASSWORD : ", None))
        self.buttonOk.setText(QCoreApplication.translate("Logon", u"&OK", None))
    # retranslateUi

