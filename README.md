# Finger Piano 🎹🖐️

An interactive, computer-vision-based virtual piano that lets you play musical notes simply by moving your fingers in front of your webcam. 

This project uses **MediaPipe** for real-time hand and finger tracking, **OpenCV** for webcam video capture, and **PyGame** to handle the audio playback and graphical display.

## How It Works

The script captures your webcam feed and maps the landmarks of your hand. It constantly checks the state of your fingers (open or closed) by comparing the position of your fingertips to your knuckles. When a finger transitions from a "closed" state to an "open" state, PyGame triggers a specific piano note associated with that finger.

* **Thumb:** Plays note 1 (b6)
* **Index Finger:** Plays note 2 (c6)
* **Middle Finger:** Plays note 3 (e6)
* **Ring Finger:** Plays note 4 (f6)
* **Pinky Finger:** Plays note 5 (g6)

## Prerequisites

You will need Python 3.x installed on your machine. To install the required libraries, run the following command in your terminal or command prompt:

```bash
pip install opencv-python mediapipe pygame numpy
```

## Setup Instructions

For this code to run successfully without throwing a sound-loading warning, you must set up your audio files exactly as the code expects. 

1. Go to your computer's **Desktop**.
2. Create a new folder and name it exactly **`c_note.wav`** *(Note: Even though it has a `.wav` extension, the code treats this as a folder directory).*
3. Place your `.mp3` sound files inside this new folder. They must be named exactly as follows:
   * `b6-82017.mp3` (for the thumb)
   * `c6-102822.mp3` (for the index finger)
   * `e6-82016.mp3` (for the middle finger)
   * `f6-102819.mp3` (for the ring finger)
   * `g6-82013.mp3` (for the pinky finger)

## Usage

1. Ensure your webcam is connected and accessible.
2. Run the Python script:
   ```bash
   python finger_piano.py
   ```
   *(Replace `finger_piano.py` with whatever you named your Python file).*
3. A PyGame window titled "Finger Piano" will open showing your webcam feed. 
4. Hold your hand up to the camera. Close your hand into a fist, and then flick your fingers open one by one to play the notes!
5. To exit the application, click the close (X) button on the PyGame window.
