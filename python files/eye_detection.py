import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Define eye landmarks indices
LEFT_EYE = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
RIGHT_EYE = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]

# Initialize webcam
cap = cv2.VideoCapture(0)

def draw_eye_contour(image, landmarks, eye_indices, color=(0, 255, 0)):
    height, width = image.shape[:2]
    points = []
    for idx in eye_indices:
        point = landmarks.landmark[idx]
        x = int(point.x * width)
        y = int(point.y * height)
        points.append((x, y))
    points = np.array(points, dtype=np.int32)
    cv2.polylines(image, [points], True, color, 1)
    return points

def detect_eyes():
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Failed to capture frame")
            continue

        # Flip the image horizontally for a later selfie-view display
        image = cv2.flip(image, 1)
        
        # Convert the BGR image to RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Process the image and detect faces
        results = face_mesh.process(rgb_image)
        
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Draw eye contours
                left_eye = draw_eye_contour(image, face_landmarks, LEFT_EYE, (0, 255, 0))
                right_eye = draw_eye_contour(image, face_landmarks, RIGHT_EYE, (0, 255, 0))
                
                # Calculate eye centers
                left_center = np.mean(left_eye, axis=0).astype(int)
                right_center = np.mean(right_eye, axis=0).astype(int)
                
                # Draw eye centers
                cv2.circle(image, tuple(left_center), 3, (255, 0, 0), -1)
                cv2.circle(image, tuple(right_center), 3, (255, 0, 0), -1)

        # Display the image
        cv2.imshow('Eye Detection', image)
        
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if _name_ == "_main_":
    detect_eyes()