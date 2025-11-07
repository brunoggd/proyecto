import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

api_key = "m8vkw03Vv8kbOmPQ8jtzvWdXXjzpbIKi"
pais = "AR"
anio_actual = QDate.currentDate().year()
mes_actual = QDate.currentDate().month()
meses_diccionario = {
                        "Enero": 1,
                        "Febrero": 2,
                        "Marzo": 3,
                        "Abril": 4,
                        "Mayo": 5,
                        "Junio": 6,
                        "Julio": 7,
                        "Agosto": 8,
                        "Septiembre": 9,
                        "Octubre": 10,
                        "Noviembre": 11,
                        "Diciembre": 12
                        }

def aplicar_fade_in(widget,duracion:int):
    efecto = QGraphicsOpacityEffect()
    widget.setGraphicsEffect(efecto)

    animacion = QPropertyAnimation(efecto, b"opacity")
    animacion.setDuration(duracion)
    animacion.setStartValue(0)
    animacion.setEndValue(1)
    animacion.start()    

    widget.animacion_opacidad = animacion

def limpiar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')