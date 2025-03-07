import cv2
import mediapipe as mp
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
# Vertical eye landmarks
LEFT_EYE_VERTICAL = [386, 374]  # Top and bottom landmarks
RIGHT_EYE_VERTICAL = [159, 145]  # Top and bottom landmarks

# Initialize webcam
cap = cv2.VideoCapture(0)

def calculate_ear(landmarks, eye_indices, vertical_indices):
    """Calculate Eye Aspect Ratio (EAR)"""
    points = []
    for idx in eye_indices:
        point = landmarks.landmark[idx]
        points.append([point.x, point.y])
    points = np.array(points)
    
    # Get vertical points
    v_top = landmarks.landmark[vertical_indices[0]]
    v_bottom = landmarks.landmark[vertical_indices[1]]
    vertical_distance = abs(v_top.y - v_bottom.y)
    
    # EAR threshold can be adjusted based on your needs
    return vertical_distance

def draw_eye_state(image, landmarks, eye_indices, vertical_indices, is_left=True):
    height, width = image.shape[:2]
    points = []
    
    # Calculate EAR
    ear = calculate_ear(landmarks, eye_indices, vertical_indices)
    
    # Threshold for eye state - adjust these values based on testing
    EAR_THRESHOLD = 0.022
    
    # Determine eye state
    if ear < EAR_THRESHOLD:
        state = "Closed"
        color = (0, 0, 255)  # Red
    else:
        state = "Open"
        color = (0, 255, 0)  # Green
    
    # Draw eye contour
    for idx in eye_indices:
        point = landmarks.landmark[idx]
        x = int(point.x * width)
        y = int(point.y * height)
        points.append((x, y))
    
    points = np.array(points, dtype=np.int32)
    cv2.polylines(image, [points], True, color, 1)
    
    # Add text for eye state
    eye_text = "Left" if is_left else "Right"
   
    
    return points

def detect_eyes():
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Failed to capture frame")
            continue

        image = cv2.flip(image, 1)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_image)
        
        # Add text for when no face is detected
        if not results.multi_face_landmarks:
            cv2.putText(image, "No face detected", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        else:
            for face_landmarks in results.multi_face_landmarks:
                # Draw eye contours and state
                left_eye = draw_eye_state(image, face_landmarks, LEFT_EYE, 
                                        LEFT_EYE_VERTICAL, is_left=True)
                right_eye = draw_eye_state(image, face_landmarks, RIGHT_EYE, 
                                         RIGHT_EYE_VERTICAL, is_left=False)

        cv2.imshow('Eye State Detection', image)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if _name_ == "_main_":
    detect_eyes()