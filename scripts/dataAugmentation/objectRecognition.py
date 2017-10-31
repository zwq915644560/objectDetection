# -*-coding:utf-8-*-

import numpy as np 
import cv2

img=cv2.imread('伊利21.jpeg')
gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('gray', gray)

gradX = cv2.Sobel(gray, ddepth=cv2.cv.CV_32F, dx=1, dy=0, ksize=-1)
gradY = cv2.Sobel(gray, ddepth=cv2.cv.CV_32F, dx=0, dy=1, ksize=-1)

# subtract the y-gradient from the x-gradient
gradient = cv2.subtract(gradX, gradY)
gradient = cv2.convertScaleAbs(gradient)

# blur and threshold the image
blurred = cv2.blur(gradient, (9, 9))
(_, thresh) = cv2.threshold(blurred, 90, 255, cv2.THRESH_BINARY)
cv2.imshow('thresh', thresh)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))
closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
cv2.imshow('closed', closed)

# perform a series of erosions and dilations
closed1 = cv2.erode(closed, None, iterations=4)
closed1 = cv2.dilate(closed1, None, iterations=4)
cv2.imshow('closed1', closed1)

(cnts, _) = cv2.findContours(closed1.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#print cnts
c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
#print c
# compute the rotated bounding box of the largest contour
rect = cv2.minAreaRect(c)
print rect
box = np.int0(cv2.cv.BoxPoints(rect))
print box 
# draw a bounding box arounded the detected barcode and display the image
cv2.drawContours(img, [box], -1, (0, 255, 0), 3)

Xs = [i[0] for i in box]
Ys = [i[1] for i in box]
x1 = max(min(Xs), 0)
x2 = min(max(Xs), img.shape[1])
y1 = max(min(Ys), 0)
y2 = min(max(Ys), img.shape[0])
box1=np.array([[x1,y1],[x2,y1],[x2,y2],[x1,y2]])
cv2.drawContours(img, [box1], -1, (0, 0, 255), 3)
print 'location:(%d, %d),(%d, %d)' %(x1, y1, x2, y2)

cv2.imshow("Image", img)
cv2.waitKey(0)

