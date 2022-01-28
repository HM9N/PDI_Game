import numpy as np
import cv2
import mediapipe as mp
import pyautogui  # - Esta libreria nos sirve para controlar el mouse desde el programa


class HandManager:

    def __init__(self, screenManager):
        # Se le pasa la región de la pantalla donde se va a jugar
        self.screenManager = screenManager
        # Método para dibujar los resultados de las detenciones
        self.mp_drawing = mp.solutions.drawing_utils
        # Métodos para poder usar mediapipe para trabajar con las manos
        self.mp_hands = mp.solutions.hands

    # Se configura la distancia entre el landmark #9 y el landmark #8 para saber cuando se ha cerrado el dedo índice
    def calculateDistance(self, x1, y1, x2, y2):
        p1 = np.array([x1, y1])
        p2 = np.array([x2, y2])
        # Nos devuelva la distancia euclidiana entre los dos puntos (p1 y p2)
        return np.linalg.norm(p1 - p2)

    # Detecta cuando se baja el dedo índice
    def detect_finger_down(self, handLandmarks, width, height, output):
        fingerDown = False
        # El color para línea del landmark 9 a la muñeca
        colorBase = (255, 0, 112)
        # El color desde el dedo índice hasta la muñeca
        colorIndex = (255, 198, 82)

        # Valor x del landmark 0
        xBase1 = int(handLandmarks.landmark[0].x * width)
        # Valor y del landmark 0
        yBase1 = int(handLandmarks.landmark[0].y * height)

        # Valor x del landmark 9
        xBase2 = int(handLandmarks.landmark[9].x * width)
        # Valor y del landmark 9
        yBase2 = int(handLandmarks.landmark[9].y * height)

        # Valor x del landmark 8
        xIndex = int(handLandmarks.landmark[8].x * width)
        # Valor y del landmark 8
        yIndex = int(handLandmarks.landmark[8].y * height)

        # Se calcula la distancia entre los landmarks 0 y 9
        dBase = self.calculateDistance(xBase1, yBase1, xBase2, yBase2)
        # Se calcula la distancia entre los landmarks 0 y 8
        dBase_index = self.calculateDistance(xBase1, yBase1, xIndex, yIndex)

        if dBase_index < dBase:  # Condición para ejecutar el click del mouse
            fingerDown = True
            colorBase = (255, 0, 255)
            colorIndex = (255, 0, 255)

        # Se dibujan las lineas y circulos de los landmarks de interés
        cv2.circle(output, (xBase1, yBase1), 5, colorBase, 2)
        cv2.circle(output, (xIndex, yIndex), 5, colorIndex, 2)
        cv2.line(output, (xBase1, yBase1), (xBase2, yBase2), colorBase, 3)
        cv2.line(output, (xBase1, yBase1), (xIndex, yIndex), colorIndex, 3)

        return fingerDown

    def start(self):
        cap = self.screenManager.beginVideoCapture()
        aspectRatioScreen = self.screenManager.getAspectRatioScreen()
        # Se define el margen que habrá en el recuadro para no usar los bordes
        X_Y_INI = self.screenManager.getMargin()
        X_INI = self.screenManager.getXIni()
        X_FIN = self.screenManager.getXFin()
        Y_INI = self.screenManager.getYIni()
        Y_FIN = self.screenManager.getYFin()
        colorMousePointer = self.screenManager.getColorMousePointer()

        with self.mp_hands.Hands(
                # Opción para que las imagenes sean tratadas como un stream.
                static_image_mode=False,
                max_num_hands=1,  # El número de manos que se van a detectar
                min_detection_confidence=0.5) as hands:  # Valor mímimo de confianza del modelo de la detección de manos

            while True:
                ret, frame = cap.read()  # Se lee la información de proveniente de la cámara
                if ret == False:
                    break

                # Se extraen las dimensiones de la imagen proveniente de la cámara
                height, width, _ = frame.shape
                # Se giran los frames horizontalmente para reflejar la imagen y así la mano pueda ser identificada como derecha o izquierda
                frame = cv2.flip(frame, 1)

                # Dibujando un área proporcional a la del juego
                # Se le resta el margen al ancho del recuadro interno que será usado
                areaWidth = width - X_Y_INI * 2
                # El alto del área del recuadro interno tendrá la misma relación de aspecta que la región dónde está el juego
                areaHeight = int(areaWidth / aspectRatioScreen)
                # Se crea una imagen auxiliar
                auxImage = np.zeros(frame.shape, np.uint8)
                auxImage = cv2.rectangle(auxImage, (X_Y_INI, X_Y_INI), (
                    X_Y_INI + areaWidth, X_Y_INI + areaHeight), (255, 0, 0), -1)  # Se visualiza el rectangulo con los puntos y dimensiones
                # Se suman las imagen proveniente de la cámara con el rectangulo creado
                output = cv2.addWeighted(frame, 1, auxImage, 0.7, 0)

                # Se pasa la imagen a RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                results = hands.process(frame_rgb)

                if results.multi_hand_landmarks is not None:
                    for hand_landmarks in results.multi_hand_landmarks:
                        # Se selecciona el landmark #9
                        x = int(hand_landmarks.landmark[9].x * width)
                        y = int(hand_landmarks.landmark[9].y * height)
                        xm = np.interp(
                            x, (X_Y_INI, X_Y_INI + areaWidth), (X_INI, X_FIN))  # Se hace la interpolación lineal en x para poder llevar el movimiento del mouse desde el recuadro de la imagen al área del juego
                        ym = np.interp(
                            y, (X_Y_INI, X_Y_INI + areaHeight), (Y_INI, Y_FIN))  # Se hace la interpolación lineal en y para poder llevar el movimiento del mouse al área del juego
                        pyautogui.moveTo(int(xm), int(ym)) #Se usa la libreria pyautogui para mover el cursor (pasandole las coordenadas como parametros)
                        if self.detect_finger_down(hand_landmarks, width, height, output): #Si la distancia entre la punta dedo indice y la muñeca cumple el requisito para hacer clic se usa pyautogui para dar el clic
                            pyautogui.click() # Se hace clic
                        cv2.circle(output, (x, y), 10, colorMousePointer, 3)
                        cv2.circle(output, (x, y), 5, colorMousePointer, -1)

                #cv2.imshow('Frame', frame)
                cv2.imshow('output', output)
                if cv2.waitKey(1) & 0xFF == 27:
                    break
        cap.release()
        cv2.destroyAllWindows()
