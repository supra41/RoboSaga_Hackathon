import cv2
import mediapipe as mp
import numpy as np
import time

# Initialize MediaPipe FaceMesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Define eye landmark indices (MediaPipe)
LEFT_EYE = [33, 133]
RIGHT_EYE = [362, 263]
LEFT_EYE_VERTICAL = [159, 145]
RIGHT_EYE_VERTICAL = [386, 374]

# EAR threshold for detecting open/closed eyes
EAR_THRESHOLD = 0.25

# Initialize OpenCV capture
cap = cv2.VideoCapture(0)

# Initialize eye state counters and timers
eyes_open = 0
eyes_closed = 0
eyes_not_detected = 0
open_time = 0
closed_time = 0
away_time = 0
last_state = None
state_start_time = time.time()

def calculate_ear(landmarks, eye_indices, vertical_indices):
    """Calculate the Eye Aspect Ratio (EAR)."""
    p1, p2 = eye_indices
    p3, p4 = vertical_indices

    # Get landmark positions
    eye_width = np.linalg.norm(np.array([landmarks[p1].x, landmarks[p1].y]) -
                               np.array([landmarks[p2].x, landmarks[p2].y]))

    eye_height = np.linalg.norm(np.array([landmarks[p3].x, landmarks[p3].y]) -
                                np.array([landmarks[p4].x, landmarks[p4].y]))

    # Avoid division by zero
    if eye_width == 0:
        return 0

    ear = eye_height / eye_width
    return ear

def update_state_time(current_state):
    """Update time spent in each state."""
    global last_state, state_start_time, open_time, closed_time, away_time

    current_time = time.time()
    if last_state != current_state:
        elapsed = current_time - state_start_time
        if last_state == "open":
            open_time += elapsed
        elif last_state == "closed":
            closed_time += elapsed
        elif last_state == "away":
            away_time += elapsed

        last_state = current_state
        state_start_time = current_time

def draw_eye_state(image, landmarks, eye_indices, vertical_indices, is_left=True):
    """Detect and draw eye state on the image."""
    global eyes_open, eyes_closed

    ear = calculate_ear(landmarks, eye_indices, vertical_indices)

    # Determine eye state
    if ear >= EAR_THRESHOLD:
        eye_state = "open"
        eyes_open += 1
    else:
        eye_state = "closed"
        eyes_closed += 1

    update_state_time(eye_state)

    # Draw eye state
    eye_position = (50, 50) if is_left else (300, 50)
    cv2.putText(image, f"{eye_state.upper()}", eye_position, 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0) if eye_state == "open" else (0, 0, 255), 2)

def detect_eyes():
    """Main function to capture video and detect eye states."""
    global eyes_not_detected, last_state

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Failed to capture frame")
            continue

        image = cv2.flip(image, 1)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_image)

        if not results.multi_face_landmarks:
            cv2.putText(image, "No face detected", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            eyes_not_detected += 2
            update_state_time("away")
        else:
            for face_landmarks in results.multi_face_landmarks:
                draw_eye_state(image, face_landmarks.landmark, LEFT_EYE, LEFT_EYE_VERTICAL, is_left=True)
                draw_eye_state(image, face_landmarks.landmark, RIGHT_EYE, RIGHT_EYE_VERTICAL, is_left=False)

        # Display real-time statistics
        stats_text = (
            f"\rEyes Open: {eyes_open} ({open_time:.1f}s) | "
            f"Eyes Closed: {eyes_closed} ({closed_time:.1f}s) | "
            f"Away: {eyes_not_detected} ({away_time:.1f}s)"
        )
        print(stats_text, end="")

        # Display stats on image
        y_pos = 90
        for text in stats_text.split("|"):
            cv2.putText(image, text.strip(), (10, y_pos), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            y_pos += 30

        cv2.imshow('Eye State Detection', image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            update_state_time(last_state)
            break

    # Print final statistics
    print("\n\nFinal Statistics:")
    print(f"Total Eyes Open: {eyes_open} frames ({open_time:.1f} seconds)")
    print(f"Total Eyes Closed: {eyes_closed} frames ({closed_time:.1f} seconds)")
    print(f"Total Away Time: {eyes_not_detected} frames ({away_time:.1f} seconds)")
    
    

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
  detect_eyes()
