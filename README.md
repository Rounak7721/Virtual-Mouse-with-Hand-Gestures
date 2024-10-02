# Virtual Mouse with Hand Gestures


## Description
Virtual Mouse with Hand Gestures is a computer vision-based project that utilizes hand gestures to control the mouse pointer, perform clicks, scrolling, screenshots, and drag-and-drop actions. This project employs OpenCV, Mediapipe, PyAutoGUI, and Pynput for gesture recognition and cursor control, providing a hands-free way to interact with your computer.


## Features
1. Move Pointer: Move the pointer by bringing the thumb tip (4) and index finger pip (6) (two green points) closer together. When they are apart, it switches to click mode.
2. Left Click: Perform a left click by putting the index finger (red point) down and up, mimicking the press of a mouse button.
3. Right Click: Perform a right click by putting the middle finger (red point) down and up, similar to pressing the right button on a mouse.
4. Scroll:
   1. Scroll Up: Close the ring finger (blue point) and simultaneously raise the index finger, keeping the pinky finger (pink dot) up.
   2. Scroll Down: Close the ring finger (blue point) and simultaneously raise the middle finger, keeping the pinky finger (pink dot) up.
6. Drag and Drop: Bring the index tip (8) and middle tip (12) (red dots) closer together to initiate drag mode. Move objects while the tips are close, and release to drop the object once the tips separate, keeping the pinky finger (pink dot) up.
7. Screenshot: Take a screenshot by closing the pinky finger (pink dot) and forming a fist (all fingers closed), then opening the fist.


## Installation
### Clone the repository:
git clone https://github.com/Rounak7721/Virtual-Mouse-with-Hand-Gestures.git

### Install the required dependencies: 
Navigate to the project directory and install the necessary Python libraries:
pip install -r requirements.txt

### Run the project: 
Use the following command to start the virtual mouse:
python VirtualMouse.py


## Technologies Used
OpenCV: For video capturing and processing.
Mediapipe: For hand gesture recognition.
PyAutoGUI: For controlling the mouse.
Pynput: For handling advanced mouse controls.


## Future Improvements
Gesture customization for additional functionality.
Enhance pointer stability and reduce shaking.
Add gesture-based keyboard inputs.
