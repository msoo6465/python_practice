import ctypes
import datetime
import time
import threading
import shutil
import logging
import logging.handlers

import numpy as np
import cv2
import os
from tkinter import filedialog
import tkinter
from npy_append_array import NpyAppendArray

root = tkinter.Tk()
root.withdraw()
move_path = filedialog.askdirectory(parent=root,initialdir="/",title='Please select a directory to move')

logger = logging.getLogger(__name__)

formatter = logging.Formatter('[%(asctime)s][%(levelname)s|%(filename)s:%(lineno)s] >> %(message)s')


streamHandler = logging.StreamHandler()
nowDate = datetime.datetime.now()
logname = nowDate.strftime('%Y-%m-%d_%H%M%S')
fileHandler = logging.FileHandler(logname)

logger.setLevel(level=logging.DEBUG)

streamHandler.setFormatter(formatter)
fileHandler.setFormatter(formatter)

logger.addHandler(streamHandler)
logger.addHandler(fileHandler)

logger.info("\ndir_path : " + str(move_path))

import pyrealsense2 as rs
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 15)
config.enable_stream(rs.stream.color, 1920, 1080, rs.format.bgr8, 15)
pc = rs.pointcloud()
try:
    profile = pipeline.start(config)
except:
    ctypes.windll.user32.MessageBoxW(0, "리얼센스를 연결하세요.", "Error", 1)
    logger.error('NO REALSENSE')
    exit()

depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()
align_to = rs.stream.color
align = rs.align(align_to)
is_save = False
end_save = False
exIndex = 1
temp_index = 0
is_init = True
with_depth = True
change = False
start_time = time.time()
init_fps_list = []

nowDate = datetime.datetime.now()
filename = nowDate.strftime('%Y-%m-%d_%H%M%S')

class save_npy(threading.Thread):
    def __init__(self,npaa,points):

        threading.Thread.__init__(self)
        self.npaa = npaa
        self.points = points
        self.count = 0

    def run(self):
        coordinate = np.ndarray(buffer=self.points.get_vertices(), dtype=np.float16, shape=(1080, 1920, 3))
        coordinate = np.array([coordinate], dtype=np.float16)
        self.npaa.append(coordinate)
        self.count += 1

class move_file(threading.Thread):
    def __init__(self,avi_path,npy_path,move_path):
        threading.Thread.__init__(self)
        self.avi_path = avi_path
        self.npy_path = npy_path
        self.move_path = move_path

    def run(self) -> None:
        time.sleep(3)
        shutil.move(self.avi_path, self.move_path)
        shutil.move(self.npy_path, self.move_path)
dt = 1
record_time = 0
fps = 0
record_fps = 15
logger.info('program start')
try:
    while 1:
        video_start_time = time.time()
        frames = pipeline.wait_for_frames()
        aligned_frames = align.process(frames)
        aligned_depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()
        if not aligned_depth_frame or not color_frame:
            continue
        hole_filling = rs.hole_filling_filter()
        filled_depth = hole_filling.process(aligned_depth_frame)
        img = np.asanyarray(color_frame.get_data())
        ori_img = img.copy()

        # points = pc.calculate(aligned_depth_frame)
        WINDOWNAME = 'Record Program'
        h,w,c = ori_img.shape
        saved_img = ori_img.copy()
        overlay_img = cv2.resize(ori_img.copy(), (w, 40))
        overlay_img[:] = 0
        ori_img[0:40,0:w] = overlay_img
        if is_init:

            cv2.putText(ori_img, f'Initializing Wait for Second...{int(time.time() - start_time)}', (0, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            if exIndex == 1:
                os.makedirs(os.path.join(move_path,'temp'),exist_ok=True)
                test_path = os.path.join(move_path,'temp')
                fourcc = cv2.VideoWriter_fourcc('D', 'I', 'V', 'X')
                avi_path = os.path.join(test_path, filename + '.avi')
                npy_path = os.path.join(test_path, filename + '.npy')
                out = cv2.VideoWriter(avi_path, fourcc, 15, (1920, 1080), isColor=True)
                npaa = NpyAppendArray(npy_path)
                is_save = True
                exIndex = 2

            if time.time() - start_time > 5:
                logger.info('Complete initialize')
                is_init = False
                is_save = False
                out.release()
                npaa.__del__()
                file_list = os.listdir(test_path)
                for file in file_list:
                    os.remove(os.path.join(test_path, file))
                avg = sum(init_fps_list)/len(init_fps_list)
                fps = 1/avg
                print(fps)
                logger.info('initial fps : '+str(fps))
                logger.info('Normal Mode')

        else:
            cv2.putText(ori_img, f's : record_start, d : with_Depth , e : stop_record, q : exit, t : change fps', (0, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        cv2.setWindowTitle(
            WINDOWNAME, "RealSense (%dx%d) %dFPS (%.2fms) %s %dsec initial fps : %d Record_fps : %d%s" %
                        (w, h, 1.0 / dt, dt * 1000, "Recording..." if is_save else "", -1 if record_time == 0 else int(time.time()-record_time),int(fps),int(record_fps),'ing' if change else ''))
        cv2.imshow(WINDOWNAME, cv2.resize(ori_img,(960,540)))
        ret = cv2.waitKey(1)

        if ret == ord('q') or ret == ord('Q'):
            break
        elif ret == ord('d') or ret == ord('D'):
            with_depth = True
            if is_save:
                pass
            else:
                logger.info('start record with depth')
                record_time = time.time()
                nowDate = datetime.datetime.now()
                filename = nowDate.strftime('%Y-%m-%d_%H%M%S')
                fourcc = cv2.VideoWriter_fourcc('D', 'I', 'V', 'X')

                exIndex = 1
                avi_path = os.path.join(move_path,filename+'.avi')
                npy_path = os.path.join(move_path,filename+'.npy')
                out = cv2.VideoWriter(avi_path, fourcc, record_fps, (1920, 1080), isColor=True)
                npaa = NpyAppendArray(npy_path)
                is_save = True

        elif ret == ord('s') or ret == ord('S'):

            if is_save:
                pass
            else:
                logger.info('start record')
                record_time = time.time()
                nowDate = datetime.datetime.now()
                filename = nowDate.strftime('%Y-%m-%d_%H%M%S')
                fourcc = cv2.VideoWriter_fourcc('D', 'I', 'V', 'X')

                exIndex = 1
                avi_path = os.path.join(move_path,filename+'.avi')
                npy_path = os.path.join(move_path,filename+'.npy')
                out = cv2.VideoWriter(avi_path, fourcc, record_fps, (1920, 1080), isColor=True)
                npaa = NpyAppendArray(npy_path)
                is_save = True

        elif ret == ord('e') or ret == ord('E'):
            logger.info('end record')
            end_save = True
            is_save = False
            with_depth = False
            record_time = 0

        elif ret == ord('t') or ret == ord('T'):
            logger.info('change fps')
            if change:
                change = False
            else:
                change = True

        if change:
            if ret == ord('o') or ret == ord('O'):
                record_fps += 1
                logger.info('up fps', record_fps)

            elif ret == ord('p') or ret == ord('P'):
                record_fps -= 1
                logger.info('down fps', record_fps)

        if is_save:
            if with_depth:
                points = pc.calculate(filled_depth)
                coordinate = np.ndarray(buffer=points.get_vertices(), dtype=np.float16, shape=(1080, 1920, 3))
                coordinate = np.array([coordinate], dtype=np.float16)
                npaa.append(coordinate)

            out.write(saved_img)

            # save_numpy = save_npy(npaa,points)
            # save_numpy.start()

        if end_save:
            if with_depth:
                logger.info('record save with depth')
            else:
                logger.info('record save only rgb')
            with_depth = False
            is_save = False
            end_save = False
            out.release()
            npaa.__del__()
            # move = move_file(avi_path,npy_path,move_path)
            # move.start()

        if is_init:
            init_fps_list.append(time.time() - video_start_time)

        dt = time.time() - video_start_time
except Exception as e:
    logger.error('Occured Error : '+ str(e))


pipeline.stop()
if end_save == False and is_save == True:
    out.release()