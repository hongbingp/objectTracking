from collections import deque
import numpy as np
import imutils
import cv2
import joblib
import time
#设定红色阈值，HSV空间
img = cv2.imread('C:/Users/panho/Desktop/testpic.jpg')
redLower = np.array([0, 0, 150])
redUpper = np.array([255, 255, 255])

#########
model = joblib.load('config.pkl')
coor = np.array(model['ROI'])
coor = coor.reshape((8, 2))

mask = np.zeros((img.shape[0], img.shape[1]))

cv2.fillConvexPoly(mask, coor, 1)
mask = mask.astype(np.bool)

out = np.zeros_like(img)
out[mask] = img[mask]

##########
frame = imutils.resize(out, width=600)
blurred = cv2.GaussianBlur(frame, (5, 5), 0)
#初始化追踪点的列表
mybuffer = 64
pts = deque(maxlen=mybuffer)
#判断是否成功打开摄像头
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#根据阈值构建掩膜
mask = cv2.inRange(hsv, redLower, redUpper)
#腐蚀操作
mask = cv2.erode(mask, None, iterations=2)
#膨胀操作，其实先腐蚀再膨胀的效果是开运算，去除噪点
mask = cv2.dilate(mask, None, iterations=2)
#轮廓检测
cnts = cv2.findContours(mask.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2]
print(len(cnts))


colored_img = frame
# colored_img = colored_img[100:, :, :]
for i in range(len(cnts)):
    if cnts[i].shape[0] > 10 and cnts[i].shape[0] < 15:
        cv2.drawContours(colored_img, cnts, i, (255, 255, 0), 5)
        print(cnts[i].shape[0])
        cv2.imshow('contour-%d'%i, colored_img)
        cv2.waitKey()
        colored_img = frame
        # colored_img = colored_img[100:, :, :]
cv2.destroyAllWindows()