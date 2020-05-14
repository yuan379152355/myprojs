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
def coverImgs2(img, imgs,x1,x3, y1,x2,y2):
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
def coverImgs1(img, img_l, img_m, img_r,x1,x3, y1,y2):
	sp=img.size
	h1=sp[1]
	w1=sp[0]

	# 衣服
	sp=img_l.size
	h2=sp[1]
	w2_l=sp[0]
	sp=img_r.size
	w2_r=sp[0]

	x_begin = x_end = 0
	y_end = 0

	# 获取覆盖边界，以免超过图片范围
	# 头部左侧宽度
	# 头部对接点以下部分高度
	w_l = x1
	w_r = w1 - x3
	h_d = h1 - y1

	rate_l = w_l / w2_l
	rate_r = w_r / w2_r
	rate_y = h_d / (h2 - y2)

	h2_h = int(rate_y * h2) + 1
	# 重置左右侧衣服尺寸
	img_l = img_l.resize((w_l,h2_h))
	img_m = img_m.resize((x3-x1,h2_h))
	img_r = img_r.resize((w_r,h2_h))

	pixels = img.load()
	for yh in range(y1, h1):
		for xw in range(0, w1):
			# 将不为透明的点覆盖到对应位置
			try:
				if xw < x1:
					color_d = img_l.getpixel((xw, h2_h - (h1-yh)))
					pixels[xw,yh] = color_d
				elif xw >= x3:
					color_d = img_r.getpixel((xw - x3, h2_h - (h1-yh)))
					pixels[xw,yh] = color_d
				else:
					color_d = img_m.getpixel((xw - x1, h2_h - (h1-yh)))
					if(color_d[3] == 255):
						pixels[xw,yh] = color_d
			except:
				print(xw, x1, x3, w1,img_l.size, (xw, h2_h - (h1-yh)))
				break

	return img


# 覆盖图片
def coverImgs2(img, img_l, img_m, img_r,x1,x3, y1,y2):
	sp=img.size
	h1=sp[1]
	w1=sp[0]

	# 衣服
	sp=img_l.size
	h2=sp[1]
	w2_l=sp[0]
	sp=img_r.size
	w2_r=sp[0]

	x_begin = x_end = 0
	y_end = 0

	# 获取覆盖边界，以免超过图片范围
	# 头部左侧宽度
	# 头部对接点以下部分高度
	w_l = x1
	w_r = w1 - x3
	h_d = h1 - y1

	rate_l = w_l / w2_l
	rate_r = w_r / w2_r
	rate_y = h_d / (h2 - y2)

	diff = 0
	if rate_y > 1:
		h2_h = int(rate_y * h2)
	else:
		h2_h = h2
		diff = (h2 - y2) - (h1 - y1)
	# 重置左右侧衣服尺寸
	img_l = img_l.resize((w_l,h2_h))
	img_m = img_m.resize((x3-x1,h2_h))
	img_r = img_r.resize((w_r,h2_h))

	pixels = img.load()
	for yh in range(y1, h1):
		for xw in range(0, w1):
			# 将不为透明的点覆盖到对应位置
			try:
				if xw < x1:
					color_d = img_l.getpixel((xw, h2_h - (h1-yh) - diff))
					pixels[xw,yh] = color_d
				elif xw >= x3:
					color_d = img_r.getpixel((xw - x3, h2_h - (h1-yh) - diff))
					pixels[xw,yh] = color_d
				else:
					color_d = img_m.getpixel((xw - x1, h2_h - (h1-yh) - diff))
					if(color_d[3] == 255):
						pixels[xw,yh] = color_d
			except:
				print(xw, x1, x3, w1,img_l.size, (xw, h2_h - (h1-yh) - diff))
				break

	return img

def changeBack(img, color):
	x,y = img.size

	p = Image.new('RGBA', img.size, color)
	p.paste(img, (0, 0, x, y), img)

	return p