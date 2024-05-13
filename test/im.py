import cv2
import math
import mediapipe as mp
from PIL import Image
import numpy as np

# Mediapipe setup for both pose and face detection
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mp_face_detection = mp.solutions.face_detection

def posecheck():
    imgname = "depositphotos_194974120-stock-photo-casual-man-full-body-in.jpg"
    imgsit="woman-doing-sit-to-stand-exercise.png"
    path = "D:\\heightMeasurement\\test\\test_img\\"+imgsit
    img = Image.open(r""+path)
    img = np.array(img)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    with mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5) as pose:
            pose_results = pose.process(img)

        # Initialize face detection
    with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detector:
        face_results = face_detector.process(img)

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

    postoget= [poselandmark[mp_pose.PoseLandmark.LEFT_SHOULDER], poselandmark[mp_pose.PoseLandmark.LEFT_HIP],poselandmark[mp_pose.PoseLandmark.LEFT_KNEE],poselandmark[mp_pose.PoseLandmark.LEFT_ANKLE],poselandmark[mp_pose.PoseLandmark.LEFT_HEEL],poselandmark[mp_pose.PoseLandmark.RIGHT_SHOULDER], poselandmark[mp_pose.PoseLandmark.RIGHT_HIP],poselandmark[mp_pose.PoseLandmark.RIGHT_KNEE],poselandmark[mp_pose.PoseLandmark.RIGHT_ANKLE],poselandmark[mp_pose.PoseLandmark.RIGHT_HEEL]]

    # convert normalized position to pixel then draw circle on the poselandmark
    for i in range(len(postoget)):
         if postoget[i].x and postoget[i].y <= 1:
            pos=pixel(postoget[i].x,postoget[i].y,imgwidth,imgheight)
            rawimg = cv2.circle(rawimg,(round(pos[1]),round(pos[0])),radius=10,color=(0,0,255),thickness=-1)


    print(img.shape)
    # img size

    drawposshow = Image.fromarray(rawimg, "RGB")
    drawposshow.show()

def pixel(x,y,wid,hi):
     return y*wid, x*hi


def distanceget(pos1, pos2):
    return math.dist(pos1,pos2)

posecheck()
# ยังไม่ได้เช็คตำแหน่งบนสุดของหัว
