import streamlit as st
import cv2
import numpy as np

def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: 
                    imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        hor = [np.zeros((height, width, 3), np.uint8)] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2: 
                imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        ver = np.hstack(imgArray)
    return ver

def getContours(img, imgContour):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            objCor = len(approx)
            x, y, w, h = cv2.boundingRect(approx)
            objectType = "None"
            if objCor == 3:
                objectType = "Triangle"
            elif objCor == 4:
                aspRatio = w / float(h)
                if aspRatio > 0.98 and aspRatio < 1.03:
                    objectType = "Square"
                else:
                    objectType = "Rectangle"
            elif objCor > 4:
                objectType = "Circle"
            cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(imgContour, objectType, (x + (w // 2) - 10, y + (h // 2) - 10), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 0), 2)

st.title("Image Processing with OpenCV and Streamlit")
path = 'test_img/american-football-isolated-top-view-260nw-646786579.webp'
img = cv2.imread(path)
if img is not None:
    imgContour = img.copy()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)
    canny_threshold1 = st.sidebar.slider("Canny Threshold 1", 10, 100, 50)
    canny_threshold2 = st.sidebar.slider("Canny Threshold 2", 50, 150, 50)
    imgCanny = cv2.Canny(imgBlur, canny_threshold1, canny_threshold2)
    getContours(imgCanny, imgContour)

    imgBlank = np.zeros_like(img)
    scale = st.sidebar.slider("Scale", 0.5, 1.0, 0.8)
    imgStack = stackImages(scale, ([img, imgGray, imgBlur], [imgCanny, imgContour, imgBlank]))
    st.image(imgStack, channels="BGR", caption="Stacked Images")
else:
    st.write("Error: Image not found. Please check the path.")

