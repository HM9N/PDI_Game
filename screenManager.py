import cv2


class ScreenManager:
    def __init__(self, xIni, yIni, screenPortionSize, margin):
        self.xIni = xIni # Coordenada en X del punto inicial
        self.yIni = yIni # Coordenada en Y del punto inicial
        self.xFin = xIni + screenPortionSize[0] # Se le suma el ancho del recuadro al punto inicial
        self.yFin = yIni + screenPortionSize[1] # Se le suma el alto del recuadro al punto inicial
        self.screenPortionSize = screenPortionSize
        self.margin = margin
        self.colorMousePointer = (255, 0, 255)

    def getXIni(self):
        return self.xIni

    def getYIni(self):
        return self.yIni

    def getXFin(self):
        return self.xFin

    def getYFin(self):
        return self.yFin

    #Se obtiene las dimensiones del recuadro
    def getScreenPortionSize(self):
        return self.screenPortionSize 

    #Se obtiene la relación de aspecto para dibujar un recuadro que tenga la misma relación de aspecto que nuestra pantalla
    def getAspectRatioScreen(self):
        return (self.xFin - self.xIni)/(self.yFin - self.xIni) 

    def getMargin(self):
        return self.margin

    def getColorMousePointer(self):
        return self.colorMousePointer

    # Se usa openCV para usar la cámara para vídeo
    def beginVideoCapture(self):
        return cv2.VideoCapture(0, cv2.CAP_DSHOW)
