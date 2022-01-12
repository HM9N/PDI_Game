import screenManager
import handManager

screenManager = screenManager.ScreenManager(150,160,[780,450],100)

handManager = handManager.HandManager(screenManager)

handManager.start()