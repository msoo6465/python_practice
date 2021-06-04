import cv2
from PySide2.QtGui import QPixmap, QImage
import sys
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtMultimediaWidgets import QVideoWidget
from PySide2.QtMultimedia import QMediaPlayer, QMediaContent
from PySide2.QtGui import QIcon
import qimage2ndarray

class VideoWindow(QMainWindow):

    def __init__(self, parent=None):
        super(VideoWindow, self).__init__(parent)
        self.setWindowTitle("Video Player")

        self.imageLabel = QLabel()
        self.imageLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)
        self.imageLabel.setPixmap(QPixmap())

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.btn_Trans = QPushButton('Trans')
        self.btn_Trans.setEnabled(False)
        self.btn_Trans.clicked.connect(self.Trans)

        self.btn_af_bf = QPushButton('After')
        self.btn_af_bf.setEnabled(False)
        self.btn_Trans.clicked.connect(self.After)

        self.btn_save = QPushButton('Save')
        self.btn_save.setEnabled(False)
        self.btn_Trans.clicked.connect(self.Save)

        self.frame_timer = QTimer()
        self.frame_timer.timeout.connect(self.videostart)
        self.frame_timer.timeout.connect(self.positionChanged)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Maximum)

        self.cap = cv2.VideoCapture()
        self.fps = 30
        self.pause = False

        # Create new action
        openAction = QAction(QIcon('open.png'), '&Video', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open movie')
        openAction.triggered.connect(self.openFile)

        # Create exit action
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.exitCall)

        # Load Model action
        loadAction = QAction(QIcon('open.png'), '&Model', self)
        loadAction.setShortcut('Ctrl+M')
        loadAction.setStatusTip('Load Model')
        loadAction.triggered.connect(self.openModel)

        # Create menu bar and add action
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(loadAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)

        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)

        # Create layouts to place inside widget
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)

        # Set List Widget
        self.listImage = QListWidget()
        self.listImage.setAlternatingRowColors(True)

        self.listObject = QListWidget()
        self.listObject.setAlternatingRowColors(True)

        layout = QHBoxLayout()

        # Set Left Box Layer
        L_VBox = QVBoxLayout()
        L_VBox.addWidget(self.imageLabel)
        L_VBox.addLayout(controlLayout)
        L_VBox.addWidget(self.errorLabel)

        # Set Right Box Layer
        R_widget = QWidget()
        R_VBox = QVBoxLayout()

        R_VBox.addWidget(self.listImage)
        R_VBox.addWidget(self.listObject)
        R_VBox.addWidget(self.btn_Trans)
        R_VBox.addWidget(self.btn_af_bf)
        R_VBox.addWidget(self.btn_save)
        R_widget.setLayout(R_VBox)
        R_widget.setFixedWidth(200)

        # Set Main window
        layout.addLayout(L_VBox)
        layout.addWidget(R_widget)

        # Set widget to contain window contents
        wid.setLayout(layout)

    def Trans(self):
        pass
    def After(self):
        pass
    def Save(self):
        pass
    def videostart(self):
        ret, frame = self.cap.read()

        if not ret:
            return False

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        image = qimage2ndarray.array2qimage(frame)
        self.imageLabel.setPixmap(QPixmap.fromImage(image))

    def openModel(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                                                  QDir.homePath())
        if fileName != '':
            self.listImage.addItem(fileName)


    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                QDir.homePath())

        if fileName != '':
            self.playButton.setEnabled(True)
            self.setWindowTitle(fileName.split('/')[-1])
            self.cap.open(fileName)
            self.fps = self.cap.get(cv2.CAP_PROP_FPS)

    def exitCall(self):
        sys.exit(app.exec_())

    def play(self):
        if not self.pause:
            self.frame_timer.start(int(1000 // self.fps))
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.frame_timer.stop()
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.pause = not self.pause

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.positionSlider.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoWindow()
    player.resize(640, 480)
    player.show()
    sys.exit(app.exec_())