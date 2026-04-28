import cv2
import mediapipe as mp
import pygame
import numpy as np
import os

# Initialize pygame
pygame.init()
pygame.mixer.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Finger Piano")

# Get the path to the user's Desktop
desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')

# The folder containing your sound files, based on your file name
# It must be this exact folder name on your desktop
sound_folder_path = os.path.join(desktop_path, 'c_note.wav')

# Load piano sounds from the specified folder, using the correct .mp3 extension
try:
    sounds = {
        'thumb': pygame.mixer.Sound(os.path.join(sound_folder_path, 'b6-82017.mp3')),
        'index': pygame.mixer.Sound(os.path.join(sound_folder_path, 'c6-102822.mp3')),
        'middle': pygame.mixer.Sound(os.path.join(sound_folder_path, 'e6-82016.mp3')),
        'ring': pygame.mixer.Sound(os.path.join(sound_folder_path, 'f6-102819.mp3')),
        'pinky': pygame.mixer.Sound(os.path.join(sound_folder_path, 'g6-82013.mp3'))
    }
except pygame.error as e:
    print(f"Warning: A sound file could not be loaded. Please ensure the folder and the correct .mp3 files exist. Error: {e}")
    sounds = {}

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Open webcam
cap = cv2.VideoCapture(0)

# A dictionary to keep track of the playing state of each finger
finger_states = {
    'thumb': False,
    'index': False,
    'middle': False,
    'ring': False,
    'pinky': False
}

def get_finger_status(hand_landmarks):
    """Checks if each finger is open or closed based on landmark positions."""
    finger_tips = {
        'thumb': mp_hands.HandLandmark.THUMB_TIP,
        'index': mp_hands.HandLandmark.INDEX_FINGER_TIP,
        'middle': mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
        'ring': mp_hands.HandLandmark.RING_FINGER_TIP,
        'pinky': mp_hands.HandLandmark.PINKY_TIP
    }

    finger_knuckles = {
        'index': mp_hands.HandLandmark.INDEX_FINGER_PIP,
        'middle': mp_hands.HandLandmark.MIDDLE_FINGER_PIP,
        'ring': mp_hands.HandLandmark.RING_FINGER_PIP,
        'pinky': mp_hands.HandLandmark.PINKY_PIP
    }

    current_status = {}

    # Logic for non-thumb fingers (Index, Middle, Ring, Pinky)
    for finger in ['index', 'middle', 'ring', 'pinky']:
        tip_y = hand_landmarks.landmark[finger_tips[finger]].y
        knuckle_y = hand_landmarks.landmark[finger_knuckles[finger]].y
        current_status[finger] = tip_y < knuckle_y

    # Logic for the Thumb
    thumb_tip_x = hand_landmarks.landmark[finger_tips['thumb']].x
    thumb_base_x = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].x
    current_status['thumb'] = abs(thumb_tip_x - thumb_base_x) > 0.05

    return current_status

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            current_finger_status = get_finger_status(hand_landmarks)

            for finger, is_open in current_finger_status.items():
                if is_open and not finger_states[finger]:
                    if finger in sounds:
                        sounds[finger].play()

                finger_states[finger] = is_open

    else:
        for finger in finger_states:
            finger_states[finger] = False

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = np.rot90(frame)
    frame_surface = pygame.surfarray.make_surface(frame)

    screen.blit(frame_surface, (0, 0))
    pygame.display.update()

# Cleanup
cap.release()
pygame.quit()