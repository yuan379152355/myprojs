#!usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
from PIL import Image,ImageDraw,ImageFilter

'''
#获得衣服衣领最上边像素在图像中的位置函数
def getTwoHightestPoint2(img):
	sp=img.size
	height=sp[1]
	width=sp[0]
	count = 0
	x1 = x2 = x3 = x4 = 0

	lastposition = False
	newposition = False
	for yh in range(height):
		count = 0
		for xw in range(width):
			color_d = img.getpixel((xw,yh))
			if(color_d[3] == 255): 
				newposition = True
			else:
				newposition = False
			if (newposition and (not lastposition) ) or ( (not newposition) and lastposition):
				if count == 2 and xw - x2 < 30:
					x2 = xw
				else:
					count += 1
				if count == 2:
					x2 = xw
				elif count == 3:
					x3 = xw
				elif count == 4:
					return x2,x3, yh-1
			# 记录上一次是否在头像上
			lastposition = newposition
'''
#获得衣服衣领最上边像素在图像中的位置函数
def getTwoHightestPoint(img):
	sp=img.size
	height=sp[1]
	width=sp[0]

	lastposition = False
	newposition = False

	diff = 50

	hightest_x1 = hightest_x2 = 0
	hightest_y1 = hightest_y1 = height - 1

	firstpoint = False
	secondpoint = False
	for xw in range(width):
		for yh in range(height):
		
			color_d = img.getpixel((xw,yh))
			if(color_d[3] == 255):
				if secondpoint == False:
					if xw - hightest_x1 <= diff and yh <= hightest_y1:
						hightest_x1 = xw
						hightest_y1 = yh
					if xw - hightest_x1 > diff:
						hightest_x2 = xw
						hightest_y2 = yh
						secondpoint = True
				else:
					if yh <= hightest_y2:
						hightest_x2 = xw
						hightest_y2 = yh
				break	
	return hightest_x1,hightest_x2, max(hightest_y1, hightest_y2)

# 覆盖图片
def coverImgs(img, imgs,x1,x3, y1,x2,y2):
	sp=img.size
	h1=sp[1]
	w1=sp[0]

	sp=imgs.size
	h2=sp[1]
	w2=sp[0]

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

	pixels = img.load()
	for yh in range(y1, y_end):
		for xw in range(x_begin, x_end):
			# 将不为透明的点覆盖到对应位置
			color_d = imgs.getpixel(((xw - x1) + x2,(yh - y1) + y2))
			if xw < x1 or xw > x3:
				pixels[xw,yh] = color_d
			else:
				if(color_d[3] == 255):
					pixels[xw,yh] = color_d

	# 裁剪边框  重置尺寸1寸
	img = img.crop((x_begin+3,0,x_end-3,y_end))#.resize((295,413))

	return img

# 覆盖图片
def changeBack(img, color):
	x,y = img.size

	p = Image.new('RGBA', img.size, color)
	p.paste(img, (0, 0, x, y), img)

	return p