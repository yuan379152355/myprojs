from transform import four_point_transform
import numpy as np
import argparse
import cv2
import imutils

# ap = argparse.ArgumentParser()
# ap.add_argument('-i','--image',required=True,help="Path to image file")
#
# args = vars(ap.parse_args())

#flag: 获取了图像路径

image = cv2.imread('1.png')
ratio = image.shape[0] /500.0
orig = image.copy()
image = imutils.resize(image,height=500)

gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) #灰度图像
gray = cv2.GaussianBlur(gray,(5,5),0)          #高斯模糊
edged = cv2.Canny(gray,75,200)                  #边缘检测

# 起点和终点的坐标
ptStart = (60, 60)
ptEnd = (260, 260)
point_color = (0, 255, 0) # BGR
thickness = 1 
lineType = 4



for x in range(edged.shape[0]):
		for y in range(edged.shape[1]):
			px = edged[x,y]
			ptStart = (x, 60)
			ptEnd = (x, 260)
			#cv2.line(edged, ptStart, ptEnd, point_color, thickness, lineType)

# flag : Test1 = BLOCK
print("STEP 1 Edge Detection")
cv2.imshow("Image",image)
cv2.imshow("Edge",edged)
cv2.waitKey(0)
cv2.destroyAllWindows()
