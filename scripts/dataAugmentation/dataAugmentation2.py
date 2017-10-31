#!-*-coding: utf-8-*-

# In[4]:

#from PIL import Image
#from PIL import ImageEnhance  
import numpy as np
import os
import cv2


# In[5]:

print cv2.__version__


# In[6]:

########################################################################
# 平移
def offset(image, xoff, yoff):
    rows,cols = image.shape[:2]
    H = np.float32([[1,0,xoff],[0,1,yoff]])
    #需要图像、变换矩阵、变换后的大小
    changedImg = cv2.warpAffine(image, H, (cols,rows)) 
    return changedImg
# 旋转
def rotate(image, angle, center=None, scale=1):
    rows,cols = image.shape[:2]
    if center==None:
        center=(cols/2, rows/2)
    #第一个参数旋转中心，第二个参数旋转角度，第三个参数：缩放比例
    M = cv2.getRotationMatrix2D(center, angle, scale)
    #第三个参数：变换后的图像大小
    changedImg= cv2.warpAffine(image, M, (cols, rows))
    return changedImg
# 仿射
# pts1:：原图上的三个点
# pts2：目标图上的三个点
def affine(image, pts1, pts2):
    rows,cols = image.shape[:2]
    # 图像的旋转加上拉升就是图像仿射变换，仿射变化也是需要一个M矩阵就可以，
    # 但是由于仿射变换比较复杂，一般直接找很难找到这个矩阵，opencv提供了根据变换前后三个点的对应关系来自动求解M。
    #pts1 = np.float32([[50,50],[200,50],[50,200]])
    #pts2 = np.float32([[10,100],[200,50],[100,250]])
    M = cv2.getAffineTransform(pts1,pts2)
    #第三个参数：变换后的图像大小
    changedImg = cv2.warpAffine(image, M, (cols,rows))
    return changedImg
# 翻转
def flip(image, flag):
    if flag=='top_bottom':
        changedImg=cv2.flip(image, 0)
    elif flag=='left_right':
        changedImg=cv2.flip(image, 1)
    return changedImg
# 改变图像对比度和明亮度
def contrast_brightness(image, alpha, beta):
    changedImg=image*alpha+beta
    changedImg=np.where(changedImg<=255, changedImg, 255)
    changedImg=np.where(changedImg>=0, changedImg, 0)
    return changedImg
            
##############################################################################


# In[7]:


def objectRecognition(picName):
    image=cv2.imread(picName)
    gray=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('gray', gray)

    gradX = cv2.Sobel(gray, ddepth=cv2.cv.CV_32F, dx=1, dy=0, ksize=-1)
    gradY = cv2.Sobel(gray, ddepth=cv2.cv.CV_32F, dx=0, dy=1, ksize=-1)

    # subtract the y-gradient from the x-gradient
    gradient = cv2.subtract(gradX, gradY)
    gradient = cv2.convertScaleAbs(gradient)

    # blur and threshold the image
    blurred = cv2.blur(gradient, (9, 9))
    (_, thresh) = cv2.threshold(blurred, 90, 255, cv2.THRESH_BINARY)
    #cv2.imshow('thresh', thresh)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 25))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    #cv2.imshow('closed', closed)

    # perform a series of erosions and dilations
    closed1 = cv2.erode(closed, None, iterations=4)
    closed1 = cv2.dilate(closed1, None, iterations=4)
    #cv2.imshow('closed1', closed1)

    (cnts, _) = cv2.findContours(closed1.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #print cnts
    c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
    #print c
    # compute the rotated bounding box of the largest contour
    rect = cv2.minAreaRect(c)
    box = np.int0(cv2.cv.BoxPoints(rect))

    # draw a bounding box arounded the detected barcode and display the image
    #cv2.drawContours(image, [box], -1, (0, 255, 0), 3)

    Xs = [i[0] for i in box]
    Ys = [i[1] for i in box]
    x1 = max(min(Xs), 0)
    x2 = min(max(Xs), image.shape[1])
    y1 = max(min(Ys), 0)
    y2 = min(max(Ys), image.shape[0])
    #box1=np.array([[x1,y1],[x2,y1],[x2,y2],[x1,y2]])
    #cv2.drawContours(image, [box1], -1, (0, 0, 255), 3)
    #location=[[x1,y1], [x2,y2]]
    normalized_loc=[
        [float(x1)/image.shape[1], float(y1)/image.shape[0]],
        [float(x2)/image.shape[1], float(y2)/image.shape[0]]
    ]
    return image, location




# In[10]:

NUM_PER_CLASS=400
# 平移距离
offs=range(-80, 100, 20)
# 放缩比例
probs =[1, 0.9, 0.8, 0.7, 0.6]
#旋转角度在后面每次都随机设置一次
angles=None 
print 'angles:', angles, type(angles)



print 'waiting..'

path='./data/'
fileNames=os.listdir(path)

for file_ in fileNames:
    filePath=os.path.join(path, file_)#原来的文件路径  
    if os.path.isdir(filePath):#如果是文件夹则跳过  
        #print filePath
        continue;   
    fileName, fileType=os.path.splitext(file_)#分离文件名和扩展名  
    print fileName, fileType
    newDir=os.path.join(path, fileName+'/')#新的文件路径  
    print newDir
    os.mkdir(newDir)
    
    srcImg=cv2.imread(filePath)
    print type(srcImg), srcImg.size, srcImg.shape, srcImg.dtype
    
    # 在opencv中，对图像的处理都是先x轴后y轴。图像的横向为x轴，纵向为y轴。
    srcImg=cv2.resize(srcImg, dsize=None, fx=0.1, fy=0.1, interpolation=cv2.INTER_LINEAR)
    #cv2.imshow(fileName, srcImg)
    rows, cols=srcImg.shape[:2]
   
    #print rows, cols
    ''' 
    1.对比度明亮度改变。
    4.左右翻转。
    5.角度旋转（8个角度）
    2.图像位移。
    3.扭曲变形。 
    
    '''
    fd=open(path+fileName+'.txt', 'a')
    c=0
    # 平移
    for off in offs:
        tmp1=offset(srcImg, off, 0)
        # 放缩
        for prob in probs:
            tmp2=cv2.resize(tmp1, None, fx=prob, fy=prob)
            # 旋转
            angles=np.concatenate((np.random.randint(-10, 11, 9), 
                np.array([0])))
            for angle in angles:
                tmp3=rotate(tmp2, angle)
                c+=1
                if c==NUM_PER_CLASS+1:
                    break
                pn=newDir+fileName+str(c)+'.jpeg'
                cv2.imwrite(pn, tmp3, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
                img, loc=objectRecognition(pn)
                #cv2.imwrite(pn, img, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
                #fd=open(path+fileName+'.txt', 'a')
                fd.write(str(c)+' '
		        		+str(loc[0][0])+' '
                        +str(loc[0][1])+' '
			    		+str(loc[1][0])+' '
		            	+str(loc[1][1])+'\n')
			
            if c==NUM_PER_CLASS+1:
                break
        if c==NUM_PER_CLASS+1:
        	break
    

fd.close()   
print 'Done..'
#cv2.waitKey(0)








