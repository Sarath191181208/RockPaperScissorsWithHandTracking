import cv2
import mediapipe as mp
import time


class HandDetector:
    def __init__(self, mode=False, maxHands=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
        self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
    def countFingers(self,lmList,count= False):
        ''' :returns a list containing which fingers are open
            :param lmList ! List containing positon of fingers
                    count = default:false if true return return the number of open fingers
        '''
        fingers = []
        if len(lmList) != 0:

            if lmList[4][1] > lmList[3][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            for n in range(2, 6):
                if lmList[4 * n][2] < lmList[4 * n - 1][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            if count == True:
                openFingers = 0
                for i in fingers:
                    if i == 1 :
                        openFingers += 1
                return openFingers

        return fingers
    
    def findHands(self, img, draw:bool=True):
        ''':return the image of the hand

         '''
        imgRBG = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRBG)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(
                        img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, handNo=0, draw:bool=True):
        ''':returns  an array containing the landmark List of points of hands
                :parameter img = ! Must its an image from ex openCV ,
                handNo = default : 0, index of the  hands if noOfHands > 1
                , draw = default : True if you neeed to draw points on screen
        '''
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for Id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
        return lmList



position = 0
shaked = 0



        


def main():
    previousTime = 0
    currentTime = 0
    cap = cv2.VideoCapture(0)
    detector = HandDetector()
    # detector = Hand.....HandDetector()

    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)

        currentTime = time.time()
        fps = 1 / (currentTime - previousTime)
        previousTime = currentTime
        cv2.putText(img, str(int(fps)), (10, 70),
                    cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 0), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()