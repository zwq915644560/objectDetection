#!/usr/bin/env python3
#-*-coding:utf-8-*-

import cv2
import sys

srcImg=cv2.imread(sys.argv[1])
print (srcImg.dtype)
#缩放有几种不同的插值（interpolation）方法，在缩小时推荐cv2.INTER_AREA,扩大是推荐cv2.INTER_CUBIC和cv2.INTER_LINEAR。默认都是cv2.INTER_LINEAR
dstImg=cv2.resize(srcImg, dsize=None, fx=0.2, fy=0.2, interpolation=cv2.INTER_AREA)

cv2.imwrite('resizedImage.jpg', dstImg)
