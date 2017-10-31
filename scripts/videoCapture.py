
# coding: utf-8

# In[4]:

import cv2


# In[52]:

def videoCapture():
    # 可以从摄像头读取视频流，也可以从本地视频文件中读取
    videoCapture=cv2.VideoCapture(0)

    if not videoCapture.isOpened():
        print('video open failed..')
        return;
    
    # 从摄像头读取视频流时，无法获得fps。可以自己设置。
    videoCapture.set(cv2.CAP_PROP_FPS, 20)
    fps = videoCapture.get(cv2.CAP_PROP_FPS)
    size = (int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)), 
            int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print ('fps={} (width,height)={}'.format(fps, size))
    
    # 保存为新的视频文件
    '''
    OpenCV写视频, 需要指定视频的格式, 可以从原视频中获取; 使用VideoWriter类和write()函数
    VideoWriter类写入视频时, 需要提供视频名, 编码格式, 码率(fps), 帧的尺寸等参数;
    视频格式包括: 
    I420(适合处理大文件) -> .avi;
    PIMI -> .avi;
    MJPG -> .avi & .mp4
    THEO -> .ogv;
    FLV1(flash video, 流媒体视频) -> .flv
    '''
    videoWriter=cv2.VideoWriter('video.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), fps, size)
    
    cv2.namedWindow('video')
    success, frame=videoCapture.read()
    while success:
        cv2.imshow('video', frame)
        if cv2.waitKey(10)==27:
            break
        # 写入视频文件
        videoWriter.write(frame)
        success, frame=videoCapture.read()
    videoCapture.release()
    cv2.destroyWindow('video')


# In[53]:

videoCapture()


# In[ ]:



