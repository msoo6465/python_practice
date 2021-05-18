import json
import os
import cv2
from pprint import pprint

json_dir = "D:\\data\\2021_05_17_AdditionalData\\car_gagong\\data_json"
image_dir = "D:\\data\\2021_05_17_AdditionalData\\car_gagong\\train"

# json_dir = "D:\\data\\2021_05_17_AdditionalData\\plate_gagong\\test_coco.json"
# image_dir = "D:\\data\\2021_05_17_AdditionalData\\plate_gagong"


pad = 50

with open(os.path.join(json_dir,"last_result.json"),'r') as car_json:
    a = json.load(car_json)
# with open(os.path.join(json_dir), 'r') as car_json:
#     a = json.load(car_json)
print(a.keys())
for i in a['images']:
    i['file_name'] = i['file_name'].split('/')[-1]
category = {}
for i in a['categories']:
    category[i['id']]=i['name']

for image in a['images']:
    img_path = os.path.join(image_dir,image['file_name'])
    id = image['id']
    img = cv2.imread(img_path)
    h, w, c = img.shape
    img = cv2.resize(img,(w*2,h*2))
    h,w,c = img.shape
    img_back = img.copy()
    img_back = cv2.resize(img_back,(w, h+pad))
    img_back[:,:] = 0
    # print(img_back[100:,0:w].shape)

    for anno in a['annotations']:
        if anno['image_id']==id:
            cat = category[anno['category_id']]
            x,y,w,h = anno['bbox']
            x1, x2 = int(x)*2, int(x+w)*2
            y1, y2 = int(y)*2,int(y+h)*2
            img = cv2.rectangle(img,pt1=(x1,y1), pt2=(x2,y2), color=(0,255,255), thickness=2, lineType=None, shift=None)
            img_back = cv2.putText(img_back,cat, org=(x1,y1+15), fontFace=cv2.FONT_ITALIC, fontScale=1, color=(0,0,255), thickness=2)

    img_back[pad:,:] = img
    cv2.imshow('temp',img_back)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
