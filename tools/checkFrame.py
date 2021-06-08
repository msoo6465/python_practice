import pickle
import gzip
import cv2

baseeName = 'C:\\Users\\nexys\\Documents\\action\\2021-06-08_11-08-22'

print(baseeName+'.pickle')
with gzip.open(baseeName+'.pickle','rb') as f:
    datas = pickle.load(f)

cam = cv2.VideoCapture(baseeName+'.avi')
i=0
while True:
    ret, frame = cam.read()
    if i == 0:
        imgFrame = frame.shape
    if not ret:
        print(i)
        break
    i += 1

if i == len(datas):
    print('Frame length same')

else:
    print(f'Depth frame : {len(datas)} , Video Frame : {i}')

print(imgFrame,':', datas[0]['coordinate'].shape)