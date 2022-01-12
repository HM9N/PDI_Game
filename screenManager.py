import cv2

class ScreenManager:
    def __init__(self, xIni,yIni, screenPortionSize, margin):
        self.xIni=xIni
        self.yIni=yIni
        self.xFin=xIni + screenPortionSize[0]
        self.yFin=yIni + screenPortionSize[1]
        self.screenPortionSize = screenPortionSize
        self.margin = margin

    def getXIni(self):
        return self.xIni

    def getYIni(self):
        return self.yIni

    def getScreenPortionSize(self):
        return self.screenPortionSize

    def setAspectRatioScreen(self):
        return (self.xFin - self.xIni)/(self.yFin - self.Ini)

    def beginVideoCapture(self):
        return cv2.VideoCapture(0, cv2.CAP_DSHOW)

    

    

    

    