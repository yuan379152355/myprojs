import cv2
import numpy as np

src=cv2.imread('2.png')
dst=cv2.imread('1.png')  

# Create a rough mask around the airplane.
src_mask = np.zeros(src.shape, src.dtype)


poly = np.array([ [4,80], [30,54], [151,63], [254,37], [298,90], [272,134], [43,122] ], np.int32)
cv2.fillPoly(src_mask, [poly], (255, 255, 255))
center = (140,200)
output = cv2.seamlessClone(src, dst, src_mask, center, cv2.NORMAL_CLONE)
cv2.imwrite("result.jpg", output)
