#!usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import pictools as pt
from PIL import Image,ImageDraw,ImageFilter

img_h = Image.open("5-88.png")      # head
img_c = Image.open("01.png")        # clouth

x1 = 105
x2 = 203
y1 = 305

x3,x4,y3 = pt.getTwoHightestPoint(img_c)

diff = 0
rate = float((x4-x3-2*diff)/(x2-x1))
sp = img_h.size
img_h=img_h.resize((int(sp[0] * rate),int(sp[1]*rate)))  #,Image.BILINEAR

# 裁剪衣服为三部分
sp_c = img_c.size
img_l = img_c.crop((0,0,x3, sp_c[1]))
img_m = img_c.crop((x3, 0, x4, sp_c[1]))
img_r = img_c.crop((x4, 0, sp_c[0], sp_c[1]))

img_l.show()
img_m.show()
img_r.show()

img = pt.coverImgs(img_h, img_c,int(rate*x1), int(rate*x2), int(rate*y1), x3 + diff, y3)

# 回复原来的尺寸
sp = img.size
img=img.resize((int(sp[0] / rate),int(sp[1] / rate)))  #,Image.BILINEAR

# 背景绘制颜色
img = pt.changeBack(img, (240,0,0))

img.save('result.png')