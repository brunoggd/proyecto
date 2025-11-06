from estilos import *
from funciones_y_extras import *

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

class Config:
    def __init__(self):
        super().__init__()
        self.tema_elegido = "Claro"
        self.volumen = 50
        self.pantalla_completa=0

        self.limite_paginas = 10
        self.indice_pagina = 1
        self.paginas_salteadas = 0
        self.flag=True
        
        self.script_dir = os.path.dirname(os.path.abspath(__file__))

        self.sonido_click=QSoundEffect()
        ruta_click = os.path.join(self.script_dir, "./recursos/sonidos/click.wav")
        self.sonido_click.setSource(QUrl.fromLocalFile(ruta_click))
        self.sonido_click.setVolume(1.0)

        self.sonido_click_2=QSoundEffect()
        ruta_click_2 = os.path.join(self.script_dir, "./recursos/sonidos/click_2.wav")
        self.sonido_click_2.setSource(QUrl.fromLocalFile(ruta_click_2))
        self.sonido_click_2.setVolume(0.05)

        self.sonido_click_3=QSoundEffect()
        ruta_click_3 = os.path.join(self.script_dir, "./recursos/sonidos/click_3.wav")
        self.sonido_click_3.setSource(QUrl.fromLocalFile(ruta_click_3))
        self.sonido_click_3.setVolume(0.25)
        
    def aplicar_cambios(self):
        self.configurar_tema()

    def _actualizar_resaltado_fechas(self):
        for fecha_str, tareas in self.diccionario_tareas_modo_calendario.items():
            prioridades = []
            fecha_en_qdate = QDate.fromString(fecha_str, "yyyy-MM-dd")
            for tarea in tareas:
                prioridades.append(tarea["prioridad"])

                formato = QTextCharFormat()

                if "Alta" in prioridades:
                    formato = self.resaltado_segun_prioridad("Alta")
                elif "Media" in prioridades:
                    formato = self.resaltado_segun_prioridad("Media")
                else: 
                    formato = self.resaltado_segun_prioridad("Baja")

            self.calendario.setDateTextFormat(fecha_en_qdate,formato)
        self.calendario.update()

    def _configurar_tema(self):
        if self.tema_elegido == "Oscuro":
                self.setStyleSheet(estilo_tema_oscuro)
                self.aplicar_gradiente(self,"#000000","#113A96")
        elif self.tema_elegido == "Claro":
            self.setStyleSheet(estilo)
            self.aplicar_gradiente(self,"#004EFF","#3876FF")

    def aplicar_gradiente(self,widget,color_1,color_2):
        gradiente = QLinearGradient(0,0,0,widget.height())
        gradiente.setColorAt(0.0,QColor(color_1))
        gradiente.setColorAt(1.0,QColor(color_2))

        paleta = widget.palette()
        paleta.setBrush(widget.backgroundRole(),QBrush(gradiente))
        widget.setPalette(paleta)
        widget.setAutoFillBackground(True)
        aplicar_fade_in(widget,2000)

    def resaltado_segun_prioridad(self,prioridad):
        formato = QTextCharFormat()
        if prioridad == "Alta":
            formato.setBackground(QColor("#FF5C5C"))
        if prioridad == "Media":
            formato.setBackground(QColor("#FFF45C"))
        if prioridad == "Baja":
            formato.setBackground(QColor("#7AFF5C"))
        return formato

    def configurar_tema(self):
        self.tema_elegido = self.combobox_temas.currentText()
        if self.tema_elegido == "Oscuro":
            self.setStyleSheet(estilo_tema_oscuro)
            self.aplicar_gradiente(self,"#000000","#113A96")
        elif self.tema_elegido == "Claro":
            self.setStyleSheet(estilo)
            self.aplicar_gradiente(self,"#004EFF","#3876FF")

    def cargar_pantalla_completa(self):
        if self.pantalla_completa==0:
            self.boton_pantalla_completa.setText("NO")
            self.showNormal()
            print("Minimizado")
        elif self.pantalla_completa==1:
            self.boton_pantalla_completa.setText("SI")
            self.showFullScreen()
            print("Maximizado")

    def configurar_pantalla_completa(self):
        if self.pantalla_completa==1:
            self.boton_pantalla_completa.setText("NO")
            self.pantalla_completa=0
            self.showNormal()
        else:
            self.boton_pantalla_completa.setText("SI")
            self.pantalla_completa=1
            self.showFullScreen()

    def actualizar_volumen(self, valor): 
        limpiar_consola()
        print(f"Volumen: {valor}")
        self.volumen=valor
        valor_adaptado = valor / 100
        self.sonido_click.setVolume(valor_adaptado)
        self.sonido_click_2.setVolume(valor_adaptado * 0.2) 
        self.sonido_click_3.setVolume(valor_adaptado)
        if valor < 10:
            self.etiqueta_slider_volumen.setText(f"Volumen: {valor}%")
        else:
            self.etiqueta_slider_volumen.setText(f"Volumen: {valor}%")
        self.etiqueta_slider_volumen.setStyleSheet("background:transparent;")

    def guardar_y_salir(self):
        respuesta = QMessageBox.question(self,"Guardar y Salir","Realizaste cambios en la configuración, ¿Deseas guardar los cambios?",QMessageBox.Yes | QMessageBox.No)
        if respuesta == QMessageBox.Yes:
            self.guardar_config_mysql()
            self.close()
        else:
            self.close()

    def centrar_ventana(self):
        pantalla = QApplication.primaryScreen().availableGeometry()
        ventana = self.frameGeometry()
        ventana.moveCenter(pantalla.center())
        self.move(ventana.topLeft())