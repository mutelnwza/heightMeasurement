import streamlit as st
import cv2
import math
from cv2 import imshow
import mediapipe as mp
from PIL import Image
import numpy as np

# Mediapipe setup for both pose and face detection
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mp_face_detection = mp.solutions.face_detection

def posecheck():
    imgname = "depositphotos_194974120-stock-photo-casual-man-full-body-in.jpg"
    path = "D:\\heightMeasurement\\test\\test_img\\"+imgname
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
        print("1")

    # if face_results.detections:
    #     for detection in face_results.detections:
    #         mp_drawing.draw_detection(annotated_image, detection)

    annotated_image = Image.fromarray(annotated_image,'RGB')
    imgwidth, imgheight, _ = img.shape
    Lshoulderpos=[pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y*imgheight,pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x*imgheight]
    Lhippos=[pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].y*imgheight,pose_results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].x*imgheight]
    finddis = math.dist(Lshoulderpos,Lhippos)
    print(finddis)
    annotated_image.show()


# Streamlit app function
def pose_and_face_estimation_app():
    st.title("Pose and Face Detection App")

    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        image = np.array(image)

        # Convert the image from BGR to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Initialize pose detection
        with mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5) as pose:
            pose_results = pose.process(image)

        # Initialize face detection
        with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detector:
            face_results = face_detector.process(image)

        # Draw pose and face landmarks on the image
        annotated_image = image.copy()
        if pose_results.pose_landmarks:
            mp_drawing.draw_landmarks(
                annotated_image, 
                pose_results.pose_landmarks, 
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2),
                connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)
            )

        if face_results.detections:
            for detection in face_results.detections:
                mp_drawing.draw_detection(annotated_image, detection)

        # Convert the processed image to PIL format to display in Streamlit
    #     st.image(annotated_image, caption='Processed Image', use_column_width=True)
    # else:
    #     st.write("Please upload an image to detect pose and faces.")
    

# To run the app, uncomment the following line
# pose_and_face_estimation_app()

posecheck()
