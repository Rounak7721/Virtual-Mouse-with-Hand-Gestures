# Modules
import cv2
import mediapipe as mp
import time as t
import math

# HandOperations calss
class HandOperations():

    def __init__(self, mode=False, max_hands=2, detectConf=0.5, trackConf=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.detectConf = float(detectConf)
        self.trackConf = float(trackConf)

        # Hand Object
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.max_hands,
            min_detection_confidence=self.detectConf,
            min_tracking_confidence=self.trackConf
        )
        # Drawing Utility Object
        self.mpDraw = mp.solutions.drawing_utils

        # Specs for landmarks and connection lines
        self.lmSpec = self.mpDraw.DrawingSpec(color=(0,0,255), thickness=2, circle_radius=2)
        self.conSpec = self.mpDraw.DrawingSpec(color=(0,255,0), thickness=2)


    # Function findHands: detects hands and draws landmarks & connection lines
    def findHands(self, frame, draw=True):
        
        # Convert frame from BGR to RGB
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process frame
        self.results = self.hands.process(frameRGB)

        # Extract landmarks and draw for multiple hands
        if self.results.multi_hand_landmarks:
            for hlmarks in self.results.multi_hand_landmarks:
                # Check if draw is True
                if draw:
                    # Draw landmarks with connections
                    self.mpDraw.draw_landmarks(frame, hlmarks, 
                                               self.mpHands.HAND_CONNECTIONS,
                                               landmark_drawing_spec = self.lmSpec,
                                               connection_drawing_spec= self.conSpec)
        return frame
    

    # Function findPosition: Finds position of all 21 landmarks and stores in a list
    def findPosition(self, frame, numHands=0, draw=True):
        x = [] # X coordinate list
        y = [] # Y coordinate list
        bbox = [] # box coordinates

        # Landmark List
        self.lmList = []

        # Check for multiple hands
        if self.results.multi_hand_landmarks:
            # track mentioned number of hands
            myHand = self.results.multi_hand_landmarks[numHands]
            

            # Get id and landmarks from selected hand
            for id, lmark in enumerate(myHand.landmark):

                # Get height and width of frame
                frame_h, frame_w, c = frame.shape

                # Calculate center x and y coordinates
                cx, cy = int(lmark.x * frame_w), int(lmark.y * frame_h)

                # Store coordinates in lists
                x.append(cx)
                y.append(cy)

                # Store hand id and center coordinates of x and y in  landmark list
                self.lmList.append([id,cx,cy])

                # Check if draw True
                if draw:
                    cv2.circle(frame, (cx,cy), 3, (0,255,255), 2)

            # Calculate min and max from x and y list and store in bbox list
            xmin, xmax = min(x), max(x)
            ymin, ymax = min(y), max(y)
            bbox = xmin, ymin, xmax, ymax

            # Check if draw True 
            if draw:
                boxLen = 20
                cv2.rectangle(frame, (xmin-boxLen, ymin-boxLen),(xmax+boxLen, ymax+boxLen), (0,0,255),2)
        
        return self.lmList, bbox
        
    # Function fingersUp: checks which tip landmarks are pointed upwards and returs a list
    def fingersUp(self):

        # tip landmark list
        self.tipLmarks = [4,8,12,16,20]

        # finger up list
        upList = []

        # return empty list if no landmarks
        if not self.lmList:
            return upList 
        
        # For thumb
        # Thumb
        if self.lmList[self.tipLmarks[0]][1] < self.lmList[self.tipLmarks[0] - 1][1]:
            upList.append(1)
        else:
            upList.append(0)

        # For Other Fingers
        # check z coordinates of fingers-> which is closer to camera
        for idx in range(1,5):
            if self.lmList[self.tipLmarks[idx]][2] < self.lmList[self.tipLmarks[idx] - 2][2]:
                upList.append(1)
            else:
                upList.append(0)
        
        return upList
    
    # Function findDistance: calculates disatance between 2 landmarks
    def findDistance(self, p1, p2, frame, draw=True, radius=5, thkns=3):
        # Check if landmarks are available
        if not self.lmList or len(self.lmList) <= max(p1, p2):
            return None, frame, []
        
        # extracts  x and y coordinates of the landmarks (p1 and p2).
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]

        # Calculate Midpoint
        cx, cy = (x1 + x2)//2, (y1 + y2)//2

        # Calculate Euclidean distance
        dist = math.hypot(x2-x1, y2-y1)
        
        # Check if draw true
        if draw:
            cv2.line(frame, (x1, y1), (x2,y2), (0,0,255), thkns)
            cv2.circle(frame, (x1,y1), radius, (255,0,255), cv2.FILLED)
            cv2.circle(frame, (x2,y2), radius, (255,0,255), cv2.FILLED)
            cv2.circle(frame, (cx,cy), radius, (255,255,255), cv2.FILLED)

        return dist, frame, [x1, y1, x2, y2, cx, cy]
    

# Main Function
def main():
    # Video Object
    cam = cv2.VideoCapture(0)

    # HandOperation object
    handOp = HandOperations()

    # Loop
    while True:
        # get frame
        _, frame = cam.read()
        frame = cv2.flip(frame,1)

        # call findHands function
        frame = handOp.findHands(frame)

        # call findPosition function
        lmList, bbox = handOp.findPosition(frame)
        if len(lmList) != 0:
            # print(lmList)
            pass

        # call fingersUp function
        upList = handOp.fingersUp()
        print(upList)

        # call findDistance function
        dist, frame, cordList = handOp.findDistance(p1=4, p2=8, frame=frame)
        # print(dist)
        # display frame
        cv2.imshow("Virtual Mouse and Keyboard", frame)

        # Exit condidtion
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cam.release()
            cv2.destroyAllWindows()
            break

# Main
if __name__ == "__main__":
    main()