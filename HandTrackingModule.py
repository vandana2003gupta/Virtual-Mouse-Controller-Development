import cv2
import mediapipe as mp

class handDetector:
    def __init__(self, mode=False, maxHands=2, detectionCon=0.7, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=self.mode,
                                        max_num_hands=self.maxHands,
                                        min_detection_confidence=self.detectionCon,
                                        min_tracking_confidence=self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0):
        lmList = []
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(hand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append((id, cx, cy))
        return lmList, img

    def fingersUp(self):
        fingers = []
        if not self.results.multi_hand_landmarks:
            return fingers
        hand = self.results.multi_hand_landmarks[0]
        landmarks = hand.landmark
        # Thumb
        fingers.append(landmarks[4].x < landmarks[3].x)
        # Fingers
        for tip in [8, 12, 16, 20]:
            fingers.append(landmarks[tip].y < landmarks[tip - 2].y)
        return fingers

    def findDistance(self, p1, p2, img, draw=True):
        lmList, _ = self.findPosition(img)
        if not lmList:
            return 0, img, None
        x1, y1 = lmList[p1][1:]
        x2, y2 = lmList[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 2)
            cv2.circle(img, (x1, y1), 10, (255, 0, 255), -1)
            cv2.circle(img, (x2, y2), 10, (255, 0, 255), -1)
            cv2.circle(img, (cx, cy), 10, (0, 0, 255), -1)
        return length, img, (x1, y1, x2, y2, cx, cy)
