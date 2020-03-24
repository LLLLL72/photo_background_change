import cv2
import  numpy as np




def change_bg(img):
#缩放
    rows,cols,channels = img.shape
    # img=cv2.resize(img,None,fx=0.5,fy=0.5)
    rows,cols,channels = img.shape
    # cv2.imshow('img',img)
    #转换hsv
    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    lower_blue=np.array([78,43,46])
    upper_blue=np.array([110,255,255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    # cv2.imshow('Mask', mask)

    #腐蚀膨胀
    erode=cv2.erode(mask,None,iterations=15)
    # cv2.imshow('erode',erode)
    dilate=cv2.dilate(erode,None,iterations=23)
    # cv2.imshow('dilate',dilate)
    # cv2.fill
    #遍历替换
    for i in range(rows):
        for j in range(cols):
            if dilate[i,j]==255:
                img[i,j]=(0,0,255)#此处替换颜色，为BGR通道

    return img