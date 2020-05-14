import cv2
import numpy as np
import pictools as pt
from PIL import Image,ImageDraw

#img = cv2.imread('5-88.png', cv2.IMREAD_UNCHANGED)  # 原图
#imgcloth = cv2.imread('01.png',cv2.IMREAD_UNCHANGED)#衣服图
img_h = Image.open("5-88.png")
img_h = img_h.convert('RGBA')
#img_h.show()
image = Image.open("01.png")
image = image.convert('RGBA')
#image.show()

#imgcloth = cv2.cvtColor(np.asarray(image),cv2.COLOR_RGB2BGR)

#cv2.imshow('img', img)
#cv2.imshow('imgcloth', imgcloth)

x1 = 105
x2 = 203
y1 = 310

point_size = 1
point_color = (0, 0, 255) # BGR
thickness = 4 # 可以为 0 、4、8

x3,x4,y3 = pt.getTwoHightestPoint2(image)
#image = lp.getArea(image)
draw =ImageDraw.Draw(image)
r = 1
draw.ellipse((x3-r, y3-r, x3+r, y3+r), fill=(255,0,0,255))
draw.ellipse((x4-r, y3-r, x4+r, y3+r), fill=(255,0,0,255))
#cv2.circle(image, (x3,y3), point_size, point_color, thickness)
#cv2.circle(image, (x4,y3), point_size, point_color, thickness)
#image.show()
print('衣领左坐标：(%d, %d)' % (x3,y3))
print('衣领右坐标：(%d, %d)' % (x4,y3))

rate = float((x2-x1)/(x4-x3))
sp = image.size
image=image.resize((int(sp[0] * rate),int(sp[1]*rate)))  #,Image.BILINEAR
#img2 = cv2.resize(img2, (0, 0), fx=rate, fy=1, interpolation=cv2.INTER_NEAREST)
pt.coverImgs(img_h, image,x1,y1,int(x3 * rate),y3)
img_h.show()
#cv2.namedWindow("image")
#cv2.imshow('image', image)
cv2.waitKey (10000)







