import cv2
import math
import mediapipe as mp
from PIL import Image
import time
import numpy as np

start=time.time()

# Mediapipe setup for both pose and face detection
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mp_face_detection = mp.solutions.face_detection

def posecheck():
    imgname = "depositphotos_194974120-stock-photo-casual-man-full-body-in.jpg"
    imgsit="woman-doing-sit-to-stand-exercise.png"
    half = "half.jpg"
    a = "276025.jpg"
    path = "D:\\heightMeasurement\\test\\test_img\\"+a
    img = Image.open(r""+path)
    img = np.array(img)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # cv2.circle(img,(human[0][0],human[1][3]),radius=10,color=(0,0,255),thickness=-1)

    with mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5) as pose:
            pose_results = pose.process(img)    

    # Draw pose and face landmarks on the image
    annotated_image = img.copy()
    if pose_results.pose_landmarks:
        mp_drawing.draw_landmarks(
            annotated_image, 
            pose_results.pose_landmarks, 
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2),
            connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)
        )


    rawimg = annotated_image
    annotated_image = Image.fromarray(annotated_image,'RGB')
    # annotated_image.show()
    imgwidth, imgheight, _ = img.shape
    poselandmark = pose_results.pose_landmarks.landmark


# find distance between shoulder and hip

    if poselandmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x and poselandmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y and poselandmark[mp_pose.PoseLandmark.LEFT_HIP].x and poselandmark[mp_pose.PoseLandmark.LEFT_HIP].y <= 1:
        pos1=pixel([poselandmark[mp_pose.PoseLandmark.LEFT_SHOULDER]],imgwidth,imgheight)
        pos2=pixel([poselandmark[mp_pose.PoseLandmark.LEFT_HIP]],imgwidth,imgheight)
        dist = abs(pos1[1]-pos2[1])
        print(dist)

    elif poselandmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x and poselandmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y and poselandmark[mp_pose.PoseLandmark.RIGHT_HIP].x and poselandmark[mp_pose.PoseLandmark.RIGHT_HIP].y <= 1:
        pos1=pixel([poselandmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]],imgwidth,imgheight)
        pos2=pixel([poselandmark[mp_pose.PoseLandmark.RIGHT_HIP]],imgwidth,imgheight)
        dist = abs(pos1[1]-pos2[1])

    else:
         print("shoulder and hip not found")
         quit()

    posleft=[
            poselandmark[mp_pose.PoseLandmark.LEFT_HIP],
            poselandmark[mp_pose.PoseLandmark.LEFT_KNEE],
            poselandmark[mp_pose.PoseLandmark.LEFT_ANKLE],
            poselandmark[mp_pose.PoseLandmark.LEFT_HEEL]
            ]

    posright=[
            poselandmark[mp_pose.PoseLandmark.RIGHT_HIP],
            poselandmark[mp_pose.PoseLandmark.RIGHT_KNEE],
            poselandmark[mp_pose.PoseLandmark.RIGHT_ANKLE],
            poselandmark[mp_pose.PoseLandmark.RIGHT_HEEL]
            ]

    availableleft,availableright,pixelleft,pixelright=[],[],[],[]

    checkpos(posleft,availableleft)
    checkpos(posright,availableright)

    cvt(availableleft,pixelleft,imgwidth,imgheight,rawimg)
    cvt(availableright,pixelright,imgwidth,imgheight,rawimg)

    print(pixelleft)
    print(pixelright)

    print("shape",img.shape)
    # img size

    drawposshow = Image.fromarray(rawimg, "RGB")
    drawposshow.show()


def pixel(pos,wid,hi,):
    for i in range(len(pos)):
        return pos[i].x*hi,pos[i].y*wid


def cvt(pos,listtoadd,wid,hi,img):
    for i in range(len(pos)):
        position=pos[i].x*hi,pos[i].y*wid
        print("pos",position)
        listtoadd.append(position)
        cv2.circle(img,(round(position[0]),round(position[1])),radius=0,color=(0,0,255),thickness=20)


def distanceget(pos1, pos2):
    return math.dist(pos1,pos2)


def checkpos(listofpos,listtoadd):
    for i in range(len(listofpos)):
        if listofpos[i].x and listofpos[i].y <= 1:
                listtoadd.append(listofpos[i])

print(posecheck())
end=time.time()
print(end-start)
# ยังไม่ได้เช็คตำแหน่งบนสุดของหัว
