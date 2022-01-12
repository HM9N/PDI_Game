import cv2


class ScreenManager:
    def __init__(self, xIni, yIni, screenPortionSize, margin):
        self.xIni = xIni
        self.yIni = yIni
        self.xFin = xIni + screenPortionSize[0]
        self.yFin = yIni + screenPortionSize[1]
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

    def getScreenPortionSize(self):
        return self.screenPortionSize

    def getAspectRatioScreen(self):
        return (self.xFin - self.xIni)/(self.yFin - self.xIni)

    def getMargin(self):
        return self.margin

    def getColorMousePointer(self):
        return self.colorMousePointer

    def beginVideoCapture(self):
        return cv2.VideoCapture(0, cv2.CAP_DSHOW)
