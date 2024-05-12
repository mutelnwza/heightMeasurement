import cv2
import numpy as np

def getContour(img,cThr=[100,100],showCanny=False, minArea=1000,filter=0,draw=False):
    imgGrey = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGrey,(5,5),1)
    imgCanny = cv2.Canny(imgBlur,cThr[0],cThr[1])
    kernel = np.ones((5,5))
    imgDial = cv2.dilate(imgCanny, kernel,iterations=3)
    imgThre = cv2.erode(imgDial,kernel,iterations=2)
    if showCanny:cv2.imshow('Canny',imgThre)    

    contours, hiearchy = cv2.findContours(imgThre,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    finalcontours=[]
    
    for i in contours:
        area = cv2.contourArea(i)
        if area > minArea:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i,0.02*peri,True)
            bbox = cv2.boundingRect(approx)
            if filter > 0:
                if len(approx)==filter:
                    finalcontours.append(len(approx),area,approx,bbox,i)
            else:
                finalcontours.append(len(approx),area,approx,bbox,i)

    finalcontours = sorted(finalcontours,key=lambda x:x[1],reverse=True)

    if draw:
        for con in finalcontours:
            cv2.drawContours(img,con[4],-1,(0,0,225),3)
    
    return img, finalcontours

