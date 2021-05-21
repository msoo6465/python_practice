from PySide2.QtGui import QPixmap, QImage
import sys
from PySide2.QtWidgets import *
from PySide2.QtCore import Qt
import qimage2ndarray

class MainWindow(QWidget):
    def __init__(self,parent=None):
        QWidget.__init__(self,parent)
        # self.form = QFormLayout()
        # self.setLayout(self.form)
        # self.form.setLabelAlignment(Qt.AlignCenter)

        self.setWindowTitle('Image viewer')

        self.imageLabel=QLabel()
        self.imageLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored,QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)
        self.imageLabel.setPixmap(QPixmap())

        self.lbName = QLabel("")
        self.btnFind = QPushButton("Find image")
        self.btnTran = QPushButton("Detect")
        self.btnSave = QPushButton("Save")
        openButton = QPushButton("Load image")

        self.btnBox = QHBoxLayout()
        self.btnBox.addWidget(self.btnFind)
        self.btnBox.addWidget(self.btnTran)
        self.btnBox.addWidget(self.btnSave)

        self.boxTop = QVBoxLayout()
        self.boxTop.addWidget(self.imageLabel)
        self.boxTop.addLayout(self.btnBox)

        self.setLayout(self.boxTop)

        self.btnFind.clicked.connect(self.open)
        self.btnTran.clicked.connect(self.notyet)
        self.btnSave.clicked.connect(self.notyet)
        self.resize(QApplication.primaryScreen().availableSize()*2/5)

    def notyet(self):
        QMessageBox.information(self,QApplication.applicationName(),"Not Yet")

    def trans(self):
        pass

    def open(self):
        fileName, _ = QFileDialog.getOpenFileName(self,
                            "Open Image File",".","Images (*.png *.xpm *.jpg)")
        if fileName != "":
            self.load(fileName)

    def load(self,fileName):
        image = QImage(fileName)

        if image.isNull():
            QMessageBox.information(self,QApplication.applicationName(),
                                    "Cannot load "+fileName)
            self.setWindowTitle("Image viewer")
            self.setPixmap(QPixmap())

        self.imageLabel.setPixmap(QPixmap.fromImage(image))
        self.setWindowTitle(fileName)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec_()