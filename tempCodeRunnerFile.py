import cv2
import mediapipe as mp
import pygame
import numpy as np

# Initialize pygame
pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Finger Detection with Webcam")

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Open webcam
cap = cv2.VideoCapture(0)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ret, frame = cap.read()
    if not ret:
        break

    # Flip for mirror effect
    frame = cv2.flip(frame, 1)

    # Convert to RGB for MediaPipe
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    # Draw landmarks if hand detected
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Example: get fingertip (index finger tip is landmark 8)
            index_tip = hand_landmarks.landmark[8]
            x, y = int(index_tip.x * width), int(index_tip.y * height)

            # Draw a circle on index fingertip
            cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)

    # Convert OpenCV frame → pygame surface
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = np.rot90(frame)
    frame_surface = pygame.surfarray.make_surface(frame)

    # Show in pygame
    screen.blit(frame_surface, (0, 0))
    pygame.display.update()

# Cleanup
cap.release()
pygame.quit()
