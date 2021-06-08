import os.path
import sys
sys.coinit_flags = 2
import pythoncom

import pyrealsense2 as rs
import numpy as np
import cv2
import pickle
import gzip

from PySide2.QtGui import QPixmap, QImage
from PySide2 import QtGui

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtMultimediaWidgets import QVideoWidget
from PySide2.QtMultimedia import QMediaPlayer, QMediaContent
from PySide2.QtGui import QIcon
import qimage2ndarray
import time

import threading

class VideoWindow(QMainWindow):
    def __init__(self, parent=None):
        super(VideoWindow, self).__init__(parent)
        self.thread = threading.Thread(target=self.saveDepth)
        self.ing = False
        self.record_flag = False
        self.frame_id = 0
        self.fps = 30
        self.init_reasense()
        self.setbase()


    def init_reasense(self):
        # Configure depth and color streams
        self.pipeline = rs.pipeline()
        config = rs.config()

        # Get device product line for setting a supporting resolution
        pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
        pipeline_profile = config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()
        device_product_line = str(device.get_info(rs.camera_info.product_line))

        config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, self.fps)

        if device_product_line == 'L500':
            config.enable_stream(rs.stream.color, 1920, 1080, rs.format.bgr8, self.fps)
        else:
            config.enable_stream(rs.stream.color, 1920, 1080, rs.format.bgr8, self.fps)

        self.pc = rs.pointcloud()

        # Start streaming
        self.profile = self.pipeline.start(config)
        depth_sensor = self.profile.get_device().first_depth_sensor()
        self.depth_scale = depth_sensor.get_depth_scale()
        align_to = rs.stream.color
        self.align = rs.align(align_to)

    def setBtn(self):
        self.btn_record = QPushButton('Record')
        self.btn_record.setEnabled(False)
        self.btn_record.clicked.connect(self.record)

        self.btn_find = QPushButton('찾아보기')
        self.btn_find.setEnabled(True)
        self.btn_find.setSizePolicy(QSizePolicy.Fixed,
                                      QSizePolicy.Maximum)
        self.btn_find.clicked.connect(self.find)

        self.btn_view = QPushButton('View')
        self.btn_view.setEnabled(True)
        self.btn_view.setSizePolicy(QSizePolicy.Fixed,
                                    QSizePolicy.Maximum)
        self.btn_view.clicked.connect(self.view)

        self.btn_saveAction = QPushButton('Add')
        self.btn_saveAction.setEnabled(True)
        self.btn_saveAction.clicked.connect(self.saveAction)
        self.btn_saveAction.setSizePolicy(QSizePolicy.Fixed,
                                    QSizePolicy.Maximum)

        self.btn_delete = QPushButton('Delete')
        self.btn_delete.setEnabled(True)
        self.btn_delete.clicked.connect(self.deleteAction)
        self.btn_delete.setSizePolicy(QSizePolicy.Preferred,
                                          QSizePolicy.Maximum)

        self.actionInput = QLineEdit(self)
        self.actionInput.setPlaceholderText('Action')
        self.actionInput.setSizePolicy(QSizePolicy.Preferred,
                                QSizePolicy.Maximum)
        self.actionInput.returnPressed.connect(self.saveAction)

        self.actionList = QListWidget(self)

        self.actionBox_u = QHBoxLayout()
        self.actionBox_u.addWidget(self.actionInput)
        self.actionBox_u.addWidget(self.btn_saveAction)

        self.actionBox = QVBoxLayout()
        self.actionBox.addLayout(self.actionBox_u)
        self.actionBox.addWidget(self.actionList)
        self.actionBox.addWidget(self.btn_delete)

        self.actionWidget = QWidget()
        self.actionWidget.setLayout(self.actionBox)
        self.actionWidget.setFixedWidth(200)

    def setbase(self):
        self.setWindowTitle("Video Player")
        self.depthFrame = []

        self.setBtn()

        self.imageLabel = QLabel()
        self.imageLabel.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)
        self.imageLabel.setPixmap(QPixmap())

        self.frame_timer = QTimer()
        self.frame_timer.timeout.connect(self.videostart)

        self.path = QLabel()
        self.path.setSizePolicy(QSizePolicy.Preferred,
                                      QSizePolicy.Maximum)

        self.findBox = QHBoxLayout()
        self.findBox.addWidget(self.path)
        self.findBox.addWidget(self.btn_view)
        self.findBox.addWidget(self.btn_find)

        self.leftBox = QVBoxLayout()
        self.leftBox.setContentsMargins(0, 0, 0, 0)
        self.leftBox.addWidget(self.imageLabel)
        self.leftBox.addLayout(self.findBox)



        self.rightBox = QVBoxLayout()
        self.rightBox.setContentsMargins(0, 0, 0, 0)
        self.rightBox.addWidget(self.actionWidget)
        self.rightBox.addWidget(self.btn_record)


        wid = QWidget(self)
        self.setCentralWidget(wid)

        layout = QHBoxLayout()
        layout.addLayout(self.leftBox)
        layout.addLayout(self.rightBox)

        wid.setLayout(layout)

    def view(self):
        if self.ing == True:
            self.btn_view.setText('Start')
            self.frame_timer.stop()
        else:
            self.btn_view.setText('Stop')
            self.frame_timer.start(int(1000 // self.fps))
            self.btn_record.setEnabled(True)
        self.ing = not self.ing

    def videostart(self):
        try:
            start_time = time.time()
            # Wait for a coherent pair of frames: depth and color
            frames = self.pipeline.wait_for_frames()
            aligned_frames = self.align.process(frames)
            depth_frame = aligned_frames.get_depth_frame()
            color_frame = aligned_frames.get_color_frame()

            points = self.pc.calculate(depth_frame)

            coordinates = np.ndarray(buffer=points.get_vertices(), dtype=np.float32, shape=(1080, 1920, 3))

            if not depth_frame or not color_frame:
                self.message('Fail to load frame')

            # Convert images to numpy arrays
            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())

            # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

            depth_colormap_dim = depth_colormap.shape
            color_colormap_dim = color_image.shape


            # If depth and color resolutions are different, resize color image to match depth image for display
            if depth_colormap_dim != color_colormap_dim:
                resized_color_image = cv2.resize(color_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
                images = np.hstack((resized_color_image, depth_colormap))
            else:
                images = np.hstack((color_image, depth_colormap))

            frame = cv2.cvtColor(images, cv2.COLOR_BGR2RGB)

            image = qimage2ndarray.array2qimage(frame)

            self.imageLabel.setPixmap(QPixmap.fromImage(image))

            cor = coordinates.copy()
            self.data = {
                'frame_id' : self.frame_id,
                'coordinate' : cor
            }


            if self.record_flag:
                self.depthFrame.append(self.data)
                self.saveVideo(color_image)
                self.frame_id += 1
                print('Record Time : ',time.time()-start_time)
            else:
                if self.depthFrame == []:
                    pass
                else:
                    if not self.frame_id == 0:
                        self.thread.start()
                        print('Depth Record Time : ',time.time() - start_time)
                    else:
                        self.thread = threading.Thread(target=self.saveDepth)
            # print('Just view Time : ',time.time() - start_time)
        except Exception as e:
            print(e)

        finally:
            # self.pipeline.stop()
            pass
            # print(frame_id)
            # with gzip.open('testPickleFile.pickle', 'wb') as f:
            #     pickle.dump(depthFrame, f)
            # # Stop streaming
            # pipeline.stop()


    def saveDepth(self):
        self.frame_id = 0
        with gzip.open(self.savePath+'.pickle', 'wb') as f:
            pickle.dump(self.depthFrame, f)
        self.out.release()
        self.depthFrame = []

    def saveVideo(self, image):
        self.out.write(image)

    def record(self):
        if self.path.text() == '':
            self.message('Select save Directory!')
            return

        self.record_flag = not self.record_flag

        if self.record_flag == True:
            self.btn_record.setText('Stop')
            if self.actionList.currentItem():
                self.savePath = os.path.join(self.path.text(), self.actionList.currentItem().text())
            else:
                self.savePath = self.path.text()
            os.makedirs(self.savePath, exist_ok=True)
            from datetime import datetime
            now = datetime.now()
            date_time = now.strftime("%Y-%m-%d_%H-%M-%S")
            fourcc = cv2.VideoWriter_fourcc(*'DIVX')

            self.savePath = os.path.join(self.savePath, date_time)
            self.out = cv2.VideoWriter(self.savePath + '.avi', fourcc, self.fps, (1920, 1080))
        else:
            self.btn_record.setText('Record Start')


    def deleteAction(self):
        row = self.actionList.selectedIndexes()[0].row()
        self.actionList.takeItem(row)
        pass

    def saveAction(self):
        text = self.actionInput.text()

        items = []
        for x in range(self.actionList.count()):
            items.append(self.actionList.item(x).text())

        if text in items:
            pass
        else:
            self.actionList.addItem(text)
        self.actionInput.clear()

    def find(self):
        dirName = QFileDialog.getExistingDirectory(self, self.tr("Open Data files"), "./", QFileDialog.ShowDirsOnly)
        self.path.setText(dirName)

    def play(self):
        pass

    def message(self,message = 'Nothing'):
        QMessageBox.information(self,QApplication.applicationName(),message)

    def save(self):
        pass

def realsense_off():
    print('realsense stop')
    player.pipeline.stop()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoWindow()
    player.resize(640, 480)
    player.show()
    app.lastWindowClosed.connect(realsense_off)
    sys.exit(app.exec_())

