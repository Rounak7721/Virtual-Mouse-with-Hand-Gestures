# Modules
import cv2
import numpy as np
import HandOperationModule
import pyautogui as pag
from pynput.mouse import Button, Controller
import time
import datetime as dt
import os

# Turn off PyAutoGUI's failsafe
pag.FAILSAFE = False

# Virtual Mouse Class
class VirtualMouse():
    def __init__(self, win_w, win_h, screen_w, screen_h):
        
        # ========== Variables ==========
        # Screen,window width and height
        self.win_w, self.win_h = win_w, win_h 
        self.screen_w, self.screen_h = screen_w, screen_h

        # Previous pointer location
        self.static_plocX, self.static_plocY = 0, 0  # Previous pointer locations

        # Check clicks
        self.click_performed = False  # Flag to prevent double clicks
        self.click_wait_time = 0.3 # Time to wait before another click

        # Check Action
        self.last_action_time = 0
        self.action_duration = 0.2  # Time in seconds to keep action state
    
        # Screen shot flag
        self.screenshot_taken = False  # to ensure only one screenshot is taken per fist close
        self.fist_open = False  # Flag to detect fist open state

        # Check dragging
        self.dragging = False

        # Default Action
        self.action_lbl = 'None'
        # Default text color
        self.txt_color = (0, 0, 0)

        # Scroll Lines
        self.numLines = 100

        # Circle radius
        self.radius = 5

        # ========== Objects =========
        # HandOperationModule object
        self.handOp = HandOperationModule.HandOperations(max_hands=1, detectConf=0.7, trackConf=0.7)

        # Mouse controller object
        self.mouseCon = Controller()

    # Function MovePointer: calculates and moves pointer on screen
    def MovePointer(self, lmList, frame, upList):

        # Screen boundary reduction value
        boundR = 120

        # Smoothing Factor
        smoothFact = 1  
        deadZone = 10  # Minimum movement required to move pointer

        # Check if landmark List is not empty
        if len(lmList) != 0:
            # Get tip of index finger
            x1, y1 = lmList[8][1:]

            # Create screen boundary
            cv2.rectangle(frame, (boundR, boundR), (self.win_w - boundR, self.win_h - boundR), (0, 255, 255), 2)

            # If index finger is up -> Move mode
            if upList[1] == 1:
                # Convert coordinates
                xCord = np.interp(x1, (boundR, self.win_w - boundR), (0, self.screen_w))
                yCord = np.interp(y1, (boundR, self.win_h - boundR), (0, self.screen_h))

                # Calculate smoothened movement
                clocX = self.static_plocX + (xCord - self.static_plocX) * smoothFact
                clocY = self.static_plocY + (yCord - self.static_plocY) * smoothFact

                # Ensure coordinates are within screen bounds
                clocX = min(max(clocX, 0), self.screen_w - 1)
                clocY = min(max(clocY, 0), self.screen_h - 1)

                # Check if the movement is beyond the dead zone
                if abs(clocX - self.static_plocX) > deadZone or abs(clocY - self.static_plocY) > deadZone:
                    # Move the cursor
                    pag.moveTo(clocX, clocY)

                    # Update static previous location values
                    self.static_plocX, self.static_plocY = clocX, clocY
                
    # Function LeftClick: triggers left click
    def leftClick(self):
        self.mouseCon.press(Button.left)
        self.mouseCon.release(Button.left)
        return "Left Click", (0, 0, 255)

    # Function RightClick: triggers right click
    def rightClick(self):
        self.mouseCon.press(Button.right)
        self.mouseCon.release(Button.right)
        return "Right Click", (0, 0, 255)

    # Function Scroll: handles scrolling
    def scroll(self, upList, lmList, numLines):
        action_lbl = "None"
        txt_color = (0, 0, 0)
        if len(lmList) != 0:
            # Scroll if both index and middle fingers are up
            if upList[1] == 1 and upList[2] == 0:
                pag.scroll(numLines)  # Scroll up
                action_lbl = "Scroll Up" 
                txt_color = (255, 0, 0)

            elif upList[1] == 0 and upList[2] == 1:
                pag.scroll(-numLines)  # Scroll down
                action_lbl = "Scroll Down" 
                txt_color = (255, 0, 0)
        return action_lbl, txt_color

    # Function ScreenShot: Takes Screenshot of screen
    def screenShot(self, frame):
        ssImg = pag.screenshot()
        tStamp = dt.datetime.now()
        label = tStamp.strftime("%d%m%Y_%H%M%S")
        dir_path = os.path.dirname(os.path.realpath(__file__))
        # Create Screenshots directory if it doesn't exist
        screenshots_dir = os.path.join(dir_path, "Screenshots")
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)
        ssImg.save(f"{dir_path}\Screenshots\screenshot_{label}.png")

    # Function dragDrop: Enables dragging and dropping of objects
    def dragDrop(self, lmList, frame, upList, index_mid_tip_dist):
        # Start dragging if tips of index and middle fingers are close
        if index_mid_tip_dist < 27 and not self.dragging:
            self.mouseCon.press(Button.left)  # Press and hold left mouse button
            self.dragging = True  # Set dragging flag

        # Continue moving pointer while dragging
        if self.dragging:
            self.MovePointer(self.lmList, frame, self.upList) 
            self.action_lbl = "Drag and Drop"
            self.txt_color = (0,0,255)
            cv2.putText(frame, self.action_lbl, (20, 20), cv2.FONT_HERSHEY_COMPLEX, 0.5, self.txt_color, 1)
                

            # Stop dragging when distance between index and middle fingers tips increases
            if index_mid_tip_dist >= 27:
                self.mouseCon.release(Button.left)  # Release mouse button
                self.dragging = False  # Reset dragging flag

    # Function drawMarks: Draws Landmarks on action popints
    def drawMarks(self, frame):
        # Detect hand and landmarks
        frame = self.handOp.findHands(frame, draw=False)
        self.lmList, bbox = self.handOp.findPosition(frame, draw=False)

        # Draw markers on gesture points
        if len(self.lmList) != 0:
            thumb_tip, index_pip, index_tip, middle_tip, ring_tip, pinky_tip = (self.lmList[4][1],self.lmList[4][2]), (self.lmList[6][1],self.lmList[6][2]), (self.lmList[8][1],self.lmList[8][2]), (self.lmList[12][1],self.lmList[12][2]), (self.lmList[16][1],self.lmList[16][2]), (self.lmList[20][1],self.lmList[20][2])

            # Move Points
            cv2.circle(frame, thumb_tip, self.radius, (0,255,0),cv2.FILLED)
            cv2.circle(frame, index_pip, self.radius, (0,255,0),cv2.FILLED)

            # Click Points
            cv2.circle(frame, index_tip, self.radius, (0,0,255),cv2.FILLED)
            cv2.circle(frame, middle_tip, self.radius, (0,0,255),cv2.FILLED)

            # Scroll Point
            cv2.circle(frame, ring_tip, self.radius, (255,0,0),cv2.FILLED)

            # Screenshot Point
            cv2.circle(frame, pinky_tip, self.radius, (255,0,255),cv2.FILLED)
    
    # Funtion action: Performs main gesture actions
    def action(self, frame):
        # Check which fingers are up
        self.upList = self.handOp.fingersUp()

        # Get distance between thumb tip and index base
        thumb_index_pip_dist, f, c = self.handOp.findDistance(4, 6, frame, draw=False)

        # Get distance between thumb tip and index index tip
        index_mid_tip_dist, f, c = self.handOp.findDistance(8, 12, frame, draw=False) 

        # Check if thumb index tip and index mid tip dist in not Null
        if thumb_index_pip_dist is not None and index_mid_tip_dist is not None:
            thumb_index_pip_dist = int(thumb_index_pip_dist)
            index_mid_tip_dist = int(index_mid_tip_dist)

            
            # Action: Drag and Drop
            if self.upList[4] != 0:
                self.dragDrop(self.lmList, frame, self.upList, index_mid_tip_dist)

            # Action: Move Pointer
            if thumb_index_pip_dist < 30 and not self.click_performed:
                self.action_lbl = "Move Pointer"
                self.txt_color = (0,255,0)
                self.MovePointer(self.lmList, frame, self.upList)                
                self.last_action_time = time.time()  # Update last action time
                self.click_performed = False  # Reset click flag
            
            # Check if in click mode and click performed flag
            elif thumb_index_pip_dist > 30 and not self.click_performed:
                # Action: Left click
                if self.upList[1] == 0 and self.upList[3] == 1 and self.upList[4] != 0:
                    self.action_lbl, self.txt_color = self.leftClick()
                    self.click_performed = True  # Set click flag
                    self.last_action_time = time.time()  # Update last action time

                # Action: Right Click
                elif self.upList[2] == 0 and self.upList[3] == 1 and self.upList[4] != 0:
                    self.action_lbl, self.txt_color = self.rightClick()
                    self.click_performed = True  # Set click flag
                    self.last_action_time = time.time()  # Update last action time

                # Action: Scroll 
                elif self.upList[3] == 0 and self.upList[4] != 0:  # Both index and middle fingers up
                    self.action_lbl, self.txt_color = self.scroll(self.upList, self.lmList, self.numLines)
                    self.last_action_time = time.time()  # Update last action time
                    self.click_performed = False  # Reset the click flag

                # Action: Screenshot
                elif self.upList == [0, 0, 0, 0, 0] and not self.screenshot_taken:
                    self.txt_color = (255,0,255)
                    self.screenShot(frame)
                    self.screenshot_taken = True  # Set Screenshot taken flag
                    self.fist_open = False  # fist open flag is reset

                # Reset screenshot_taken when fist is opened again
                elif self.upList != [0, 0, 0, 0, 0]:
                    self.fist_open = True

        # Ensure enough time passed before resetting flags
        if self.fist_open and self.screenshot_taken:
            self.screenshot_taken = False

        # Reset click_performed flag
        if self.click_performed and time.time() - self.last_action_time > self.click_wait_time:
            self.click_performed = False

        # Check if action state needs to be reset
        if time.time() - self.last_action_time > self.action_duration:
            self.action_lbl = 'None'
            self.txt_color = (0, 0, 0)
        
        # Display action on frame
        if not self.dragging:
            cv2.putText(frame, self.action_lbl, (20, 20), cv2.FONT_HERSHEY_COMPLEX, 0.5, self.txt_color, 1)

# Function: Main
def main():
    # ========== Variables ==========
    # Setup window dimensions
    win_w, win_h = 640, 512  # mouse->640, 512
    # Get screen dimensions
    screen_w, screen_h = pag.size()

    # ========== Objects ========== 
    # Virtual Mouse Class object
    vmouse = VirtualMouse(win_w, win_h, screen_w,screen_h)

    # Video Object
    cam = cv2.VideoCapture(0)

    # Setup window width and height
    cam.set(3, win_w)  # width
    cam.set(4, win_h)  # height

    # Main Loop
    while True:
        if not cam.isOpened():
            print("Error: Camera not opened.")
            break

        # Read cam input
        ret, frame = cam.read()
        if not ret:
            print("Failed to capture image")
            continue

        # Flip frame
        frame = cv2.flip(frame, 1)

        # Draw marks on action Points
        vmouse.drawMarks(frame)

        # Perform actions
        vmouse.action(frame)

        # Display frame
        cv2.imshow("Virtual Mouse", frame)

        # Exit Condition
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Clean Up
    cam.release()
    cv2.destroyAllWindows()

# Run main function
if __name__ == "__main__":
    main()