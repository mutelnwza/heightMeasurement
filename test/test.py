import cv2 
import math
import time  
  
img = cv2.imread("D:\\heightMeasurement\\test\\test_img\\275968.jpg")
img = cv2.resize(img,(800,800))
  
def draw_circle(event, x, y, flags, param): 
      
    if event == cv2.EVENT_LBUTTONDOWN: 
        print("position added")
        cv2.circle(img, (x, y), 5, (0,0,255), -1) 
        pos.append([x,y])
        print(pos)
        
def getdist(pos1,pos2):
    return math.dist(pos1,pos2)

cv2.namedWindow(winname = "Original Picture") 
cv2.resizeWindow("Original Picture",300,700)
cv2.setMouseCallback("Original Picture", draw_circle)

while True: 
    cv2.imshow("Original Picture", img) 
    pos,heightinpixel = [],[]
    refinpixel=[]
    k = cv2.waitKey(0)

    if cv2.waitKey(0) == ord('a'):
        for i in range(len(pos)-1):
            heightinpixel.append(getdist(pos[i],pos[i+1]))
            # heightinpixel.append(abs(pos[i][1]-pos[i+1][1]))
            img=cv2.line(img, pos[i],pos[i+1],(0,0,255),1)
            print(i)

    cv2.destroyWindow("Original Picture")

    cv2.imshow("heightline", img)
    cv2.setMouseCallback("heightline",draw_circle)
    pos=[]
    if cv2.waitKey(0) == ord('a'):
        for i in range(len(pos)-1):
            refinpixel.append(abs(pos[i+1][1]-pos[i][1]))
            img=cv2.line(img,pos[i],pos[i+1],(0,0,255),1)

    cv2.destroyWindow("heightline")

    cv2.imshow("reference object",img)
    height=float(input("input length of the reference object"))
    if cv2.waitKey(0) == ord('q'):
        print("calculating")
        print(heightinpixel)
        
        pixel_per_cm = height/refinpixel[0]
        print("pixel per cm =",pixel_per_cm)
        cm = heightinpixel[0]*pixel_per_cm
        cv2.putText(img, str(cm), (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),2)
        cv2.destroyWindow("reference object")
        cv2.imshow("final height",img)
        
        
   
cv2.destroyAllWindows() 

# วาดจุดลงบนตำแหน่งที่จะวัด get position แล้วหาระยะห่าง