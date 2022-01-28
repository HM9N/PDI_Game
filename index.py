#--------------------------------------------------------------------------
#------- PLANTILLA DE CÓDIGO ----------------------------------------------
#------- Juego PDI-------------------------------------------
#------- Por: Jhon Vásquez  y Alejandro -----------------------------------
#-------      CC 1040752210, CC         -----------------------------------
#------- Curso Básico de Procesamiento de Imágenes y Visión Artificial-----
#------- Febrero de 2022--------------------------------------------------
#--------------------------------------------------------------------------

#--------------------------------------------------------------------------
#------- Se hacen las importaciones necesarias ----------------------------
import screenManager
import handManager

#-------  Se configura la sección de la pantalla en la cual se va a jugar
screenManager = screenManager.ScreenManager(150,160,[780,450],100)

#------- Se invoca la clase para el uso de mediaPipe hands
handManager = handManager.HandManager(screenManager)

#------- Se inicia con la ejecución del programa
handManager.start()