import streamlit as st
import cv2
import mediapipe as mp
from PIL import Image
import numpy as np

# Mediapipe setup for both pose and face detection
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mp_face_detection = mp.solutions.face_detection

# Streamlit app function
def pose_and_face_estimation_app():
    st.title("Pose and Face Detection App")

    if 'image' not in st.session_state:
    st.session_state.image = None
    st.session_state.annotated_image = None
    
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        image = np.array(image)

        st.session_state.image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        st.session_state.annotated_image = st.session_state.image.copy()

    def process_and_annotate_image(image):
    # (Processing logic here)
    return annotated_image

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

#reset button
    if st.button("Reset Annotations"):
       if st.session_state.image is not None:
           st.session_state.annotated_image = process_and_annotate_image(st.session_state.image)

    if st.session_state.image is not None and st.session_state.annotated_image is None:
    st.session_state.annotated_image = process_and_annotate_image(st.session_state.image)

        # Convert the processed image to PIL format to display in Streamlit
    if st.session_state.annotated_image is not None:
       st.image(annotated_image, caption='Processed Image', use_column_width=True)
    else:
        st.write("Please upload an image to detect pose and faces.")

# To run the app, uncomment the following line
pose_and_face_estimation_app()
