import numpy as np
import cv2
import mediapipe as mp
import pyautogui


class HandManager:
    def __init__(self, screenManager):
        self.screenManager = screenManager
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands

    def calculateDistance(self, x1, y1, x2, y2):
        p1 = np.array([x1, y1])
        p2 = np.array([x2, y2])
        return np.linalg.norm(p1 - p2)

    def detect_finger_down(self, handLandmarks, width, height, output):
        fingerDown = False
        colorBase = (255, 0, 112)
        colorIndex = (255, 198, 82)

        xBase1 = int(handLandmarks.landmark[0].x * width)
        yBase1 = int(handLandmarks.landmark[0].y * height)

        xBase2 = int(handLandmarks.landmark[9].x * width)
        yBase2 = int(handLandmarks.landmark[9].y * height)

        xIndex = int(handLandmarks.landmark[8].x * width)
        yIndex = int(handLandmarks.landmark[8].y * height)

        dBase = self.calculateDistance(xBase1, yBase1, xBase2, yBase2)
        dBase_index = self.calculateDistance(
            xBase1, yBase1, xIndex, yIndex)

        if dBase_index < dBase:
            fingerDown = True
            colorBase = (255, 0, 255)
            colorIndex = (255, 0, 255)

        cv2.circle(output, (xBase1, yBase1), 5, colorBase, 2)
        cv2.circle(output, (xIndex, yIndex), 5, colorIndex, 2)
        cv2.line(output, (xBase1, yBase1), (xBase2, yBase2), colorBase, 3)
        cv2.line(output, (xBase1, yBase1),
                 (xIndex, yIndex), colorIndex, 3)

        return fingerDown

    def start(self):
        cap = self.screenManager.beginVideoCapture()
        aspectRatioScreen = self.screenManager.getAspectRatioScreen()
        X_Y_INI = self.screenManager.getMargin()
        X_INI = self.screenManager.getXIni()
        X_FIN = self.screenManager.getXFin()
        Y_INI = self.screenManager.getYIni()
        Y_FIN = self.screenManager.getYFin()
        colorMousePointer = self.screenManager.getColorMousePointer()

        with self.mp_hands.Hands(
                static_image_mode=False,
                max_num_hands=1,
                min_detection_confidence=0.5) as hands:

            while True:
                ret, frame = cap.read()
                if ret == False:
                    break

                height, width, _ = frame.shape
                frame = cv2.flip(frame, 1)

                # Dibujando un área proporcional a la del juego
                areaWidth = width - X_Y_INI * 2
                areaHeight = int(areaWidth / aspectRatioScreen)
                auxImage = np.zeros(frame.shape, np.uint8)
                auxImage = cv2.rectangle(auxImage, (X_Y_INI, X_Y_INI), (
                    X_Y_INI + areaWidth, X_Y_INI + areaHeight), (255, 0, 0), -1)
                output = cv2.addWeighted(frame, 1, auxImage, 0.7, 0)

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                results = hands.process(frame_rgb)

                if results.multi_hand_landmarks is not None:
                    for hand_landmarks in results.multi_hand_landmarks:
                        x = int(hand_landmarks.landmark[9].x * width)
                        y = int(hand_landmarks.landmark[9].y * height)
                        xm = np.interp(
                            x, (X_Y_INI, X_Y_INI + areaWidth), (X_INI, X_FIN))
                        ym = np.interp(
                            y, (X_Y_INI, X_Y_INI + areaHeight), (Y_INI, Y_FIN))
                        pyautogui.moveTo(int(xm), int(ym))
                        if self.detect_finger_down(hand_landmarks, width, height, output):
                            pyautogui.click()
                        cv2.circle(output, (x, y), 10, colorMousePointer, 3)
                        cv2.circle(output, (x, y), 5, colorMousePointer, -1)

                #cv2.imshow('Frame', frame)
                cv2.imshow('output', output)
                if cv2.waitKey(1) & 0xFF == 27:
                    break
        cap.release()
        cv2.destroyAllWindows()
