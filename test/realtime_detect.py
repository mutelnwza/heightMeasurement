import streamlit as st
import cv2
import mediapipe as mp
import numpy as np

# Mediapipe setup for pose, face detection, and face mesh (landmarks)
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mp_face_detection = mp.solutions.face_detection
mp_face_mesh = mp.solutions.face_mesh

def main():
    st.title("Real-Time Pose, Face Detection, and Face Landmarks")
    run = st.checkbox('Run')
    FRAME_WINDOW = st.image([])

    cap = cv2.VideoCapture(0)  # Initialize the webcam capture

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose, \
         mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detector, \
         mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5) as face_mesh:
        
        while run:
            ret, frame = cap.read()
            if not ret:
                continue

            # Convert the BGR image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process the image for pose detection, face detection, and face landmarks
            pose_results = pose.process(image)
            face_results = face_detector.process(image)
            face_mesh_results = face_mesh.process(image)

            # Draw the pose and face detections and face landmarks on the image
            if pose_results.pose_landmarks:
                mp_drawing.draw_landmarks(
                    image, 
                    pose_results.pose_landmarks, 
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2),
                    connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)
                )

            if face_results.detections:
                for detection in face_results.detections:
                    mp_drawing.draw_detection(image, detection)

            if face_mesh_results.multi_face_landmarks:
                for face_landmarks in face_mesh_results.multi_face_landmarks:
                    mp_drawing.draw_landmarks(
                        image,
                        face_landmarks,
                        mp_face_mesh.FACEMESH_CONTOURS,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1)
                    )

            # Display the processed image in Streamlit
            FRAME_WINDOW.image(image, use_column_width=True)

        cap.release()

if __name__ == '__main__':
    main()
