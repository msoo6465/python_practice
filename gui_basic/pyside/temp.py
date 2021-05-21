from PySide2.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                               QLabel, QFrame, QSizePolicy, QPushButton,
                               QFileDialog,QMessageBox)
from PySide2.QtGui import QPixmap,QImage
import sys

class MainWindow(QWidget):
    def __init__(self,parent=None):
        QWidget.__init__(self,parent)
        self.setWindowTitle('Image viewer')

        self.imageLabel=QLabel()
        self.imageLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored,QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)
        self.imageLabel.setPixmap(QPixmap())

        openButton = QPushButton("Load image")

        layout = QVBoxLayout()
        layout.addWidget(self.imageLabel)
        layout.addWidget(openButton)
        self.setLayout(layout)

        openButton.clicked.connect(self.open)
        self.resize(QApplication.primaryScreen().availableSize()*2/5)

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