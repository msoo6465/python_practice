import sys
sys.coinit_flags = 2
import pythoncom
import threading
import shutil
import pyrealsense2 as rs
import cv2
import numpy as np
import time
from npy_append_array import NpyAppendArray
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import QRunnable, Qt, QThreadPool
import PySide2
import os
dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

class Runnable(QRunnable):
    def __init__(self, coordinate):
        super().__init__()
        self.coordinate = coordinate

    def run(self):
        global npaa
        coordinate = np.ndarray(buffer=self.coordinate.get_vertices(), dtype=np.float32, shape=(1080, 1920, 3))
        coordinate = np.array([coordinate])
        npaa.append(coordinate)
        print("1")

class Ui_Dialog(QWidget):
    def setupUi(self, Dialog):
        global video_state

        video_state = 0
        self.img = 0

        Dialog.setObjectName("Dialog")
        Dialog.setFixedSize(840, 740)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 10, 820, 620))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 640, 311, 71))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(580, 600, 311, 71))
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(660, 660, 130, 30))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(660, 700, 130, 30))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(660, 620, 130, 30))
        self.pushButton_3.setObjectName("pushButton_3")

        #########################################################기본세팅
        # black_img = np.zeros((1980, 1980, 3), np.uint8)
        # image = QtGui.QImage(black_img, black_img.shape[1], black_img.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
        # pixmap = QPixmap.fromImage(image)
        # self.label.setPixmap(QtGui.QPixmap(pixmap))
        # self.label.resize(800, 600)
        # self.label.show()
        # back_img = cv2.imread("background.jpg")
        # back_img = cv2.resize(back_img,(280,85))
        # image2 = QtGui.QImage(back_img, back_img.shape[1], back_img.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
        # pixmap2 = QPixmap.fromImage(image2)
        # self.label_2.setPixmap(QtGui.QPixmap(pixmap2))
        # self.label_2.resize(311, 71)
        # self.label_2.show()
        ###########################################################

        self.pushButton_2.clicked.connect(self.record)
        self.pushButton.clicked.connect(self.record_start)
        self.pushButton_3.clicked.connect(self.connect)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def record(self):
        global video_state
        global npaa
        global out
        video_state = 2
        npaa.__del__()
        out.release()
        FileFolder = QFileDialog.getSaveFileName(self, "Save Data files","./")
        video_dir = "ins/video_ins.avi"
        depth_dir = "ins/depth_ins.npy"
        file_dir = FileFolder[0].split(".")[0]
        shutil.move(video_dir, file_dir + ".avi")
        shutil.move(depth_dir, file_dir + ".npy")

    def record_start(self):
        global video_state
        video_state = 1

    def connect(self):
        global video_state
        global npaa
        global out
        os.makedirs("ins", exist_ok=True)
        video_dir = "ins/video_ins.avi"
        depth_dir = "ins/depth_ins.npy"
        npaa = NpyAppendArray(depth_dir)
        test_i = 0
        i = 0
        while True:
            if test_i == 0:
                start_time = time.time()
            frames = pipeline.wait_for_frames()
            aligned_frames = align.process(frames)
            aligned_depth_frame = aligned_frames.get_depth_frame()
            color_frame = aligned_frames.get_color_frame()
            hole_filling = rs.hole_filling_filter()
            filled_depth = hole_filling.process(aligned_depth_frame)
            img = np.asanyarray(color_frame.get_data())
            points = pc.calculate(filled_depth)
            coordinates = np.ndarray(buffer=points.get_vertices(), dtype=np.float32, shape=(1080, 1920, 3))
            img = cv2.putText(img, "Frame calculation", (80, 80),  0, 3, (0, 0, 255), 3)
            coordinates = np.array([coordinates])
            npaa.append(coordinates)
            img = cv2.resize(img, (800, 600))
            image = QtGui.QImage(img, img.shape[1], img.shape[0],
                                 QtGui.QImage.Format_RGB888).rgbSwapped()
            pixmap = QPixmap.fromImage(image)
            self.label.setPixmap(QtGui.QPixmap(pixmap))
            self.label.resize(800, 600)
            self.label.show()
            cv2.waitKey(1)
            test_i += 1
            end_time = time.time() - start_time
            if end_time > 3:
                npaa.__del__()
                os.remove(depth_dir)
                fps = int(test_i / 3)
                self.label_3.setText(f"FPS : {fps}")
                break

        npaa = NpyAppendArray(depth_dir)
        fourcc = cv2.VideoWriter_fourcc('D', 'I', 'V', 'X')
        out = cv2.VideoWriter(video_dir, fourcc, fps, (1920, 1080), isColor=True)
        test_i = 0
        pool = QThreadPool.globalInstance()

        while True:
            if test_i == 0:
                start_time = time.time()
            frames = pipeline.wait_for_frames()
            aligned_frames = align.process(frames)
            aligned_depth_frame = aligned_frames.get_depth_frame()
            color_frame = aligned_frames.get_color_frame()
            hole_filling = rs.hole_filling_filter()
            filled_depth = hole_filling.process(aligned_depth_frame)
            img = np.asanyarray(color_frame.get_data())
            ori_img = img.copy()
            points = pc.calculate(filled_depth)
            coordinates = np.ndarray(buffer=points.get_vertices(), dtype=np.float32, shape=(1080, 1920, 3))

            if video_state == 1:
                img = cv2.putText(img, "rec", (80, 80), 0, 3, (0, 0, 255), 3)
                # coordinates = np.array([coordinates])
                out.write(ori_img)
                runnable = Runnable(points)
                pool.start(runnable)
                # npaa.append(coordinates)
                print("2")
                if time.time() - start_time > 1:
                    print(test_i)
                    start_time = time.time()
                    test_i = 0

            if video_state == 2:
                npaa = NpyAppendArray(depth_dir)
                fourcc = cv2.VideoWriter_fourcc('D', 'I', 'V', 'X')
                out = cv2.VideoWriter(video_dir, fourcc, fps, (1920, 1080), isColor=True)
                video_state = 0

            if video_state == 3:
                break
            runnable = Runnable(img)
            pool.start(runnable)

            img = cv2.resize(img, (800, 600))
            image = QtGui.QImage(img, img.shape[1], img.shape[0],
                                 QtGui.QImage.Format_RGB888).rgbSwapped()
            pixmap = QPixmap.fromImage(image)
            self.label.setPixmap(QtGui.QPixmap(pixmap))
            self.label.resize(800, 600)
            self.label.show()
            cv2.waitKey(1)
            print("-=-=-=-=-=")

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "RealSense 녹화 프로그램"))
        self.pushButton.setText(_translate("Dialog", "rec_start"))
        self.pushButton_2.setText(_translate("Dialog", "rec_end"))
        self.pushButton_3.setText(_translate("Dialog", "realsense_connect"))
        self.label_3.setText(f"FPS : None")

def realsense_off():
    global video_state
    global npaa
    global out
    if video_state != 0:
        npaa.__del__()
        out.release()
        pipeline.stop()
        file_list = os.listdir("ins")
        for file in file_list:
            os.remove(os.path.join("ins", file))

    video_state = 3
    exit()

if __name__ == "__main__":
    import sys
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 1920, 1080, rs.format.bgr8, 30)
    # threading.Thread(target=show_video).start()
    # evt = threading.Event()
    pc = rs.pointcloud()
    profile = pipeline.start(config)
    depth_sensor = profile.get_device().first_depth_sensor()
    depth_scale = depth_sensor.get_depth_scale()
    align_to = rs.stream.color
    align = rs.align(align_to)
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.lastWindowClosed.connect(realsense_off)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())













