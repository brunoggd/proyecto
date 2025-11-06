import mysql.connector
from mysql.connector import Error

from translate import Translator

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

from estilos import *
from texto_informativo import *
from funciones_y_extras import *
from configuraciones import Config
from base_de_datos import Db
from menus import Menu

class Tdl(QMainWindow, Config, Db,Menu):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestor de Tareas - Hecho por Bruno González y Martín Baras")
        self.setGeometry(100, 100, 800, 600)
        self.centrar_ventana()
        self.setStyleSheet(estilo)

        self.calendario = QCalendarWidget()
        self.calendario.setFixedSize(400,400)
        self.calendario.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.calendario.setMinimumDate(QDate(anio_actual,1,1))
        self.calendario.setMaximumDate(QDate(anio_actual,12,31))

        self.boton_pantalla_completa = QPushButton()
        self.boton_pantalla_completa.clicked.connect(self.sonido_click.play)
        self.boton_pantalla_completa.clicked.connect(self.configurar_pantalla_completa)
        self.boton_pantalla_completa.setFixedSize(200,55)
        if self.pantalla_completa == 0:
            self.boton_pantalla_completa.setText("NO")
        else:
            self.boton_pantalla_completa.setText("SI")

        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        self.contenedor_menu_principal = QWidget()
        self.contenedor_menu_informacion = QWidget()
        self.contenedor_menu_modos = QWidget()
        self.contenedor_modo_calendario = QWidget()
        self.contenedor_opciones = QWidget()

        self.stacked_widget.addWidget(self.contenedor_menu_principal)
        self.stacked_widget.addWidget(self.contenedor_menu_informacion)
        self.stacked_widget.addWidget(self.contenedor_menu_modos)
        self.stacked_widget.addWidget(self.contenedor_modo_calendario)
        self.stacked_widget.addWidget(self.contenedor_opciones)

        self.lista_tareas = QListWidget()
        self.lista_tareas.itemSelectionChanged.connect(self.mostrar_datos_tarea_actual_modo_calendario)
        self.lista_tareas.currentItemChanged.connect(self.mostrar_datos_tarea_actual_modo_calendario)

        self.diccionario_tareas_modo_calendario = {}
        
        self.ingreso_de_tarea_modo_calendario = self.ingresar_tarea_modo_calendario()
        self.busqueda_de_tarea_modo_calendario = self.buscar_tarea_modo_calendario()
        self.modificacion_de_tarea_modo_calendario = self.modificar_tarea_modo_calendario()
        self.visualizacion_de_tarea_modo_calendario = self.visualizar_tarea_modo_calendario()

        self.menu_principal()

        self.conexion = self.conectar_mysql()
        
        self.cargar_config()
        self.cargar_tareas()
        self._actualizar_resaltado_fechas()
        self.mostrar_tareas_por_fecha()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gestor_de_tareas = Tdl()
    gestor_de_tareas.show()
    sys.exit(app.exec_())
