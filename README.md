# Virtual Mouse — Gesture-Controlled HCI System

## Description
**Virtual Mouse — Gesture-Controlled HCI System** is a computer vision and human-computer interaction (HCI) project that enables hands-free mouse control using real-time hand gesture recognition. Using webcam input, the system interprets finger movements and gestures to control cursor movement, clicks, scrolling, drag-and-drop, and screenshots.

Built with OpenCV, MediaPipe, PyAutoGUI, and Pynput, the project demonstrates practical applications of real-time vision-based interaction systems.

## Features

### 1. Cursor Movement
Control the mouse pointer by bringing the thumb tip (4) and index finger PIP (6) closer together.  
When separated, the system switches to click interaction mode.

### 2. Left Click
Trigger a left click by lowering and raising the index finger, mimicking a button press.

### 3. Right Click
Trigger a right click by lowering and raising the middle finger.

### 4. Scrolling
- **Scroll Up:** Close the ring finger while keeping the index finger raised and pinky extended.
- **Scroll Down:** Close the ring finger while keeping the middle finger raised and pinky extended.

### 5. Drag and Drop
Bring the index tip (8) and middle tip (12) together to enter drag mode.  
Move objects while fingers remain close, and release when separated.

### 6. Screenshot Capture
Take screenshots by making a closed fist (all fingers down) and reopening the hand.

---

## Hand Landmarks
The following image shows the landmarks used for gesture recognition:

![Hand Landmarks](hand_landmarks.png)

---

## Installation

### Clone the Repository
```bash
git clone https://github.com/Rounak7721/Virtual-Mouse-with-Hand-Gestures.git
cd Virtual-Mouse-with-Hand-Gestures
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run the Project
```bash
python VirtualMouse.py
```

---

## Project Structure
```text
Virtual-Mouse-with-Hand-Gestures/
│
├── requirements.txt
├── HandOperationModule.py     # Gesture recognition and landmark processing
├── VirtualMouse.py            # Main application logic
└── README.md
```

---

## Core Modules

### HandOperationModule.py
Handles:
- Hand landmark detection
- Finger state recognition
- Distance and gesture calculations
- Gesture interpretation logic

This serves as the perception and control module of the system.

### VirtualMouse.py
Responsible for:
- Camera stream processing
- Gesture-to-action mapping
- Cursor control
- Mouse event execution

This acts as the interaction layer of the project.

---

## Technologies Used
- OpenCV — Real-time computer vision processing  
- MediaPipe — Hand tracking and landmark detection  
- PyAutoGUI — Cursor movement and mouse actions  
- Pynput — Advanced mouse control  
- NumPy — Numerical operations  
- Math — Distance calculations  
- Time — Timing and gesture state management

---

## Applications
- Touchless human-computer interaction
- Accessibility-focused interfaces
- Gesture-based control systems
- Computer vision HCI experimentation
- Foundation for robotics and vision-based interaction research

---

## Future Improvements
- Gesture customization and user-defined controls  
- Improved pointer smoothing and stability  
- Gesture-based keyboard shortcuts  
- Multi-hand interaction support  
- Depth-aware interaction using stereo or RGB-D cameras  
- Integration with AI-based gesture recognition models

---

## Highlights
- Real-time gesture-based mouse control  
- Landmark-driven interaction logic  
- Practical HCI + Computer Vision project  
- Modular and extensible architecture
