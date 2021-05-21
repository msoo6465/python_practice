import sys
from PySide2.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QGridLayout,
                               QPushButton, QHBoxLayout, QVBoxLayout)
from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt
#from PySide2.QtCore import SIGNAL, SLOT, QObject

import Logon_rc

if __name__ == '__main__':

    app = QApplication(sys.argv)
    logon = QWidget()

    labelId = QLabel('&Id :')
    labelId.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
    labelPW = QLabel('&Password:')

    lineEditId = QLineEdit()
    lineEditPW = QLineEdit()
    lineEditPW.setEchoMode(QLineEdit.Password)

    labelId.setBuddy(lineEditId)
    labelPW.setBuddy(lineEditPW)

    buttonOk = QPushButton("&Ok")
    buttonOk.setIcon(QIcon(":/ok.png"))

    layout1 = QGridLayout()
    layout1.addWidget(labelId,0,0)
    layout1.addWidget(lineEditId,0,1);
    layout1.addWidget(labelPW,1,0)
    layout1.addWidget(lineEditPW,1,1)

    layout2 = QHBoxLayout()
    layout2.addStretch()
    layout2.addWidget(buttonOk)

    mainLayout = QVBoxLayout()
    mainLayout.addLayout(layout1)
    mainLayout.addLayout(layout2)

    logon.setLayout(mainLayout)
    logon.setWindowTitle('Log on')
    logon.setWindowIcon(QIcon(":/images/ok.png"))  #

    buttonOk.clicked.connect(app.quit)

    logon.show()
    app.exec_()