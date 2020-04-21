import cv2
import numpy as np

# 取最短线所在的区域
# 纵向遍历竖线交点为4个，里面两个交点所在的范围内
def getShortestLineArea(img):
	sp=img.shape
	height=sp[0]
	width=sp[1]
	count = 0
	y1 = y2 = y3 = y4 = 0

	ptStart = (60, 60)
	ptEnd = (260, 260)
	point_color = (0, 255, 0) # BGR
	thickness = 1 
	lineType = 1

	# 记录上一个像素点是否在粉色头像图片上 默认初始不在上面
	lastposition = False
	newposition = False
	for xw in range(width):
		count = 0
		for yh in range(height):
			color_d=img[yh,xw]
			# 判断是否在粉色头像上
			if(color_d[3] == 255): 
				newposition = True
			else:
				newposition = False
			# 判断是否为线条交界处
			if (newposition and (not lastposition) ) or ( (not newposition) and lastposition):
				count += 1
				if count == 2:
					y2 = yh
				elif count == 3:
					y3 = yh
				elif count == 4:
					return xw,y2, y3

			# 记录上一次是否在头像上
			lastposition = newposition

# 取最短线位置，返回坐标点
def getShortestLineposition(img, x, y1, y2):
	sp=img.shape
	height=sp[0]
	width=sp[1]

	y = 0
	xl = xr = 0
	x_left = x_right = 0
	shortest = width
	lastposition = False
	newposition = False
	for yh in range(y1, y2):
		count = 0
		for xw in range(x , width):
			color_d=img[yh,xw]
			# 判断是否在粉色头像上
			if(color_d[3] == 255): 
				newposition = True
			else:
				newposition = False
			# 判断是否为线条交界处
			if (newposition and (not lastposition) ) or ( (not newposition) and lastposition):
				count += 1
				if count == 1:
					xl = xw
				elif count == 2:
					xr = xw
					# 判断是否为最短线条
					if shortest > (xr - xl):
						shortest = xr - xl
						x_left = xl
						x_right = xr - 1
						y = yh
			# 记录上一次是否在头像上
			lastposition = newposition

	return x_left,x_right, y

# 删除多余部分
def delExtraPart(img, xl, xr, y):
	sp=img.shape
	height=sp[0]
	width=sp[1]
	for yh in range(y, height):
		for xw in range(0 , width):
			color_d=img[yh,xw]
			if (xw < xl or xw > xr): 
				img[yh,xw] = [0,0,0,0]

def getTwoHightestPoint2(img):
	sp=img.shape
	height=sp[0]
	width=sp[1]

	count = 0
	x1 = x2 = x3 = x4 = 0

	point_color = (0, 255, 0) # BGR
	thickness = 1 
	lineType = 1

	# 记录上一个像素点是否在粉色头像图片上 默认初始不在上面
	lastposition = False
	newposition = False
	for yh in range(height):
		count = 0
		for xw in range(width):
			color_d=img[yh,xw]
			if(color_d[3] == 255): 
				newposition = True
			else:
				newposition = False
			if (newposition and (not lastposition) ) or ( (not newposition) and lastposition):
				count += 1
				if count == 2:
					x2 = xw
				elif count == 3:
					x3 = xw
				elif count == 4:
					return x2,x3, yh-1
			# 记录上一次是否在头像上
			lastposition = newposition

# 覆盖图片
def coverImgs(img, imgs,x1,y1,x2,y2):
	sp=img.shape
	h1=sp[0]
	w1=sp[1]

	sp=imgs.shape
	h2=sp[0]
	w2=sp[1]

	x_begin = x_end = 0
	y_end = 0

	# 获取覆盖边界，以免超过图片范围
	if w2 - x2 > w1 - x1:
		x_end = w1
	else:
		x_end = w1 - ((w1 - x1) - (w2 - x2))

	if x2 > x1:
		x_begin = 0
	else:
		x_begin = (x1) - (x2)

	if h2 - y2 > h1 - y1:
		y_end = h1
	else:
		y_end = h1 - ((h1 - y1) - (h2 - y2))

	for yh in range(y1, y_end):
		for xw in range(x_begin, x_end):
			# 将不为透明的点覆盖到对应位置
			if(imgs[(yh - y1) + y2, (xw - x1) + x2][3] == 255):
				img[yh,xw] = imgs[(yh - y1) + y2, (xw - x1) + x2]

if __name__=="__main__":
	# 读取图层
	img = cv2.imread('1.png', cv2.IMREAD_UNCHANGED)
	img2 = cv2.imread('2.png', cv2.IMREAD_UNCHANGED)

	# 取最短线所在的区域 
	x,y1,y2 = getShortestLineArea(img)
	# 取最短线位置，返回坐标点
	xl,xr,y = getShortestLineposition(img,x,y1,y2)
	# 删除多余部分
	delExtraPart(img,xl,xr,y)

	# 处理img2
	x2,x3,y0 = getTwoHightestPoint2(img2)

	# 缩放比例
	rate = float((xr-xl)/(x3-x2))
	img2 = cv2.resize(img2, (0, 0), fx=rate, fy=1, interpolation=cv2.INTER_NEAREST)

	# 覆盖
	img_bak = img.copy()
	coverImgs(img, img2,xl,y,int(x2 * rate),y0)

	cv2.imshow("result",img)
	cv2.waitKey(0)