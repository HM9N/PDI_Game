import numpy as np
import cv2
import mediapipe as mp
import pyautogui


class HandManager:
    def __init__(self, screenManager):
        self.screenManager = screenManager
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands

    def calculate_distance(self, x1, y1, x2, y2):
        p1 = np.array([x1, y1])
        p2 = np.array([x2, y2])
        return np.linalg.norm(p1 - p2)

    def detect_finger_down(self, hand_landmarks, width, height, output):
        finger_down = False
        color_base = (255, 0, 112)
        color_index = (255, 198, 82)

        x_base1 = int(hand_landmarks.landmark[0].x * width)
        y_base1 = int(hand_landmarks.landmark[0].y * height)

        x_base2 = int(hand_landmarks.landmark[9].x * width)
        y_base2 = int(hand_landmarks.landmark[9].y * height)

        x_index = int(hand_landmarks.landmark[8].x * width)
        y_index = int(hand_landmarks.landmark[8].y * height)

        d_base = self.calculate_distance(x_base1, y_base1, x_base2, y_base2)
        d_base_index = self.calculate_distance(
            x_base1, y_base1, x_index, y_index)

        if d_base_index < d_base:
            finger_down = True
            color_base = (255, 0, 255)
            color_index = (255, 0, 255)

        cv2.circle(output, (x_base1, y_base1), 5, color_base, 2)
        cv2.circle(output, (x_index, y_index), 5, color_index, 2)
        cv2.line(output, (x_base1, y_base1), (x_base2, y_base2), color_base, 3)
        cv2.line(output, (x_base1, y_base1),
                 (x_index, y_index), color_index, 3)

        return finger_down

    def start(self):
        cap = self.screenManager.beginVideoCapture()
        aspect_ratio_screen = self.screenManager.getAspectRatioScreen()
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
                area_width = width - X_Y_INI * 2
                area_height = int(area_width / aspect_ratio_screen)
                aux_image = np.zeros(frame.shape, np.uint8)
                aux_image = cv2.rectangle(aux_image, (X_Y_INI, X_Y_INI), (
                    X_Y_INI + area_width, X_Y_INI + area_height), (255, 0, 0), -1)
                output = cv2.addWeighted(frame, 1, aux_image, 0.7, 0)

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                results = hands.process(frame_rgb)

                if results.multi_hand_landmarks is not None:
                    for hand_landmarks in results.multi_hand_landmarks:
                        x = int(hand_landmarks.landmark[9].x * width)
                        y = int(hand_landmarks.landmark[9].y * height)
                        xm = np.interp(
                            x, (X_Y_INI, X_Y_INI + area_width), (X_INI, X_FIN))
                        ym = np.interp(
                            y, (X_Y_INI, X_Y_INI + area_height), (Y_INI, Y_FIN))
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
