import sys
import os
import requests
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

from estilos import *

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
    #Crear el efecto de opacidad
    efecto = QGraphicsOpacityEffect()
    widget.setGraphicsEffect(efecto)
    #Crear la animación
    animacion = QPropertyAnimation(efecto, b"opacity")
    animacion.setDuration(duracion)
    animacion.setStartValue(0)
    animacion.setEndValue(1)
    animacion.start()    
    #Guardar la animación para que no se destruya
    widget.animacion_opacidad = animacion

def limpiar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')

class Tdl(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestor de Tareas - Hecho por Bruno González y Martín Baras")
        self.setGeometry(100, 100, 800, 600)
        self.modo_elegido = ""
        self.tema_elejido = ""
        self.volumen = 50
        self.pantalla_completa=False
        self.centrar_ventana()
        self.setStyleSheet(estilo)

        self.nombre_video="./recursos/videos/portada.mp4"
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.ruta_video = os.path.join(self.script_dir, self.nombre_video)

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

        # Escena gráfica
        self.scene = QGraphicsScene() #es como un lienzo donde podés poner elementos visuales (video, botones, imágenes).
        self.view = QGraphicsView(self.scene, self)#muestra esa escena en la ventana principal.
        self.view.setSceneRect(0, 0, self.width(), self.height())#se fija la escena al tamaño de la ventana para que al acceder a menús que se pueden desplazar no se rompa el video de fondo
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setFrameShape(QFrame.NoFrame)

         # Video como fondo
        self.video_item = QGraphicsVideoItem()#es el componente que reproduce el video dentro de la escena.
        self.video_item.setAspectRatioMode(Qt.KeepAspectRatioByExpanding)#asegura que el video se escale manteniendo proporciones.
        self.video_item.setSize(QSizeF(self.size()))#ajusta el tamaño del video al tamaño de la ventana.
        self.scene.addItem(self.video_item)#lo agrega a la escena para que se vea.

        self.playlist = QMediaPlaylist()#permite reproducir uno o más videos.
        self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(self.ruta_video)))#carga el video desde el archivo local.
        self.playlist.setPlaybackMode(QMediaPlaylist.Loop)#hace que el video se repita infinitamente.

        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        """es el motor que reproduce el video. None significa que el reproductor no tiene un widget padre.
           VideoSurface: el video se va a renderizar en una superficie personalizada, como QGraphicsVideoItem, QVideoWidget, etc.
           Es necesario para que el video se pueda mostrar en objetos gráficos."""
        self.media_player.setPlaylist(self.playlist)#le asigna la lista de reproducción.
        self.media_player.setVideoOutput(self.video_item)#le dice que muestre el video en video_item.
        self.media_player.setVolume(50)
        self.media_player.play()#comienza la reproducción.

        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        self.overlay_menu_principal = QWidget()
        self.overlay_menu_informacion = QWidget()
        self.overlay_menu_modos = QWidget()
        self.overlay_modo_simple = QWidget()
        self.overlay_modo_calendario = QWidget()
        self.overlay_opciones = QWidget()

        self.stacked_widget.addWidget(self.overlay_menu_principal)
        self.stacked_widget.addWidget(self.overlay_menu_informacion)
        self.stacked_widget.addWidget(self.overlay_menu_modos)
        self.stacked_widget.addWidget(self.overlay_modo_simple)
        self.stacked_widget.addWidget(self.overlay_modo_calendario)
        self.stacked_widget.addWidget(self.overlay_opciones)

        self.tareas_modo_simple = QListWidget()
        self.tareas_modo_simple.itemSelectionChanged.connect(self.mostrar_datos_tarea_actual)
        self.tareas_modo_simple.currentItemChanged.connect(self.mostrar_datos_tarea_actual)
        if self.modo_elegido == "Calendario":
            self.tareas_modo_simple.itemSelectionChanged.connect(self.mostrar_datos_tarea_actual_modo_calendario)
            self.tareas_modo_simple.currentItemChanged.connect(self.mostrar_datos_tarea_actual_modo_calendario)

        self.diccionario_tareas_modo_calendario = {}

        self.indice_tarea = self.tareas_modo_simple.count() + 1

        self.ingreso_de_tarea = self.ingresar_tarea()
        self.busqueda_de_tarea = self.buscar_tarea()
        self.modificacion_de_tarea = self.modificar_tarea()
        self.visualizacion_de_tarea = self.visualizar_tarea()
        
        self.ingreso_de_tarea_modo_calendario = self.ingresar_tarea_modo_calendario()
        self.busqueda_de_tarea_modo_calendario = self.buscar_tarea_modo_calendario()
        self.modificacion_de_tarea_modo_calendario = self.modificar_tarea_modo_calendario()
        self.visualizacion_de_tarea_modo_calendario = self.visualizar_tarea_modo_calendario()

        self.menu_principal()

    def menu_principal(self):
        if self.overlay_menu_principal.layout() is None:
            layout = QVBoxLayout()
            layout.setAlignment(Qt.AlignCenter)
            self.overlay_menu_principal.setLayout(layout)
        else:
            layout = self.overlay_menu_principal.layout()
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()

        etiqueta = QLabel("To Do List")
        aplicar_fade_in(etiqueta,1000)
        etiqueta_2 = QLabel("Gestor de tareas")
        aplicar_fade_in(etiqueta_2,1000)

        boton_iniciar = QPushButton("Iniciar")
        if self.modo_elegido == "Simple":
            boton_iniciar.clicked.connect(self.usar_modo_simple)
            boton_iniciar.clicked.connect(self.sonido_click.play)
        elif self.modo_elegido == "Calendario":
            boton_iniciar.clicked.connect(self.usar_modo_calendario)
            boton_iniciar.clicked.connect(self.sonido_click.play)
        else:
            boton_iniciar.clicked.connect(self.menu_modos)
            boton_iniciar.clicked.connect(self.sonido_click.play)
        boton_informacion = QPushButton("Información")
        boton_informacion.clicked.connect(self.menu_informacion)
        boton_informacion.clicked.connect(self.sonido_click.play)

        boton_opciones = QPushButton("Opciones")
        aplicar_fade_in(boton_opciones,1000)
        boton_opciones.clicked.connect(self.opciones)
        boton_opciones.clicked.connect(self.sonido_click.play)
        
        boton_salir = QPushButton("Salir")
        boton_salir.clicked.connect(self.close)
        boton_salir.clicked.connect(self.sonido_click.play)

        aplicar_fade_in(boton_iniciar,1000)
        aplicar_fade_in(boton_informacion,1000)
        aplicar_fade_in(boton_salir,1000)
        
        layout.addWidget(etiqueta,alignment=Qt.AlignCenter | Qt.AlignTop)
        layout.addWidget(etiqueta_2,alignment=Qt.AlignCenter | Qt.AlignTop)
        layout.addWidget(boton_iniciar)
        layout.addWidget(boton_informacion)
        layout.addWidget(boton_opciones)
        layout.addWidget(boton_salir)

        self.stacked_widget.setCurrentWidget(self.overlay_menu_principal)
    
    def menu_informacion(self):
        if self.overlay_menu_informacion.layout() is None:
            layout = QVBoxLayout()
            self.overlay_menu_informacion.setLayout(layout)
        else:
            layout = self.overlay_menu_informacion.layout()
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()

        boton_volver_al_menu_principal = QPushButton("Volver")
        aplicar_fade_in(boton_volver_al_menu_principal,1000)
        boton_volver_al_menu_principal.clicked.connect(self.menu_principal)
        boton_volver_al_menu_principal.clicked.connect(self.sonido_click_2.play)

        informacion = QTextEdit()
        aplicar_fade_in(informacion,1000)
        informacion.setReadOnly(True)
        informacion.setFixedSize(900,550)
        texto_informativo="""
                                                Modos:

Modo Simple: Permite ingresar tareas y ordenarlas en una interfaz clara y sencilla. Es recomendable usar este modo para tareas simples o cotidianas.

Modo Calendario: Permite ingresar tareas y ordenarlas en una interfaz con calendario para una mejor organización.

Puedes cambiar los modos a tu gusto aunque hayas elejido uno u otro al principio en el apartado de "Opciones".

Recomendaciones:
1) Elegir el modo que mejor se ajuste a tus necesidades.
2) Ingresar tus tareas de forma clara y entendible.
3) Realizar un seguimiento regular de tus tareas."""
        informacion.setText(texto_informativo)

        layout.addWidget(informacion,alignment=Qt.AlignCenter)
        layout.addWidget(boton_volver_al_menu_principal,alignment=Qt.AlignLeft)

        self.stacked_widget.setCurrentWidget(self.overlay_menu_informacion)
    
    def menu_modos(self):
        if self.overlay_menu_modos.layout() is None:
            layout = QVBoxLayout()
            self.overlay_menu_modos.setLayout(layout)
        else:
            layout = self.overlay_menu_modos.layout()
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()

        contenedor_modos = QWidget()
        contenedor_boton_volver = QWidget()

        layout_modos = QVBoxLayout()
        layout_boton_volver = QVBoxLayout()
        
        contenedor_modos.setLayout(layout_modos)
        contenedor_boton_volver.setLayout(layout_boton_volver)

        etiqueta_modo = QLabel("Elije el modo que quieras usar:")
        aplicar_fade_in(etiqueta_modo,1000)

        boton_modo_simple = QPushButton("Simple")
        boton_modo_simple.clicked.connect(self.usar_modo_simple)
        boton_modo_simple.clicked.connect(self.sonido_click.play)
        aplicar_fade_in(boton_modo_simple,1000)
        boton_modo_simple.setFixedSize(200,55)

        boton_modo_calendario = QPushButton("Calendario")
        boton_modo_calendario.clicked.connect(self.usar_modo_calendario)
        boton_modo_calendario.clicked.connect(self.sonido_click.play)
        aplicar_fade_in(boton_modo_calendario,1000)
        boton_modo_calendario.setFixedSize(200,55)

        boton_volver_al_menu_principal = QPushButton("Volver")
        aplicar_fade_in(boton_volver_al_menu_principal,1000)
        boton_volver_al_menu_principal.clicked.connect(self.menu_principal)
        boton_volver_al_menu_principal.clicked.connect(self.sonido_click_2.play)

        layout_modos.addWidget(etiqueta_modo,alignment=Qt.AlignCenter)
        layout_modos.addWidget(boton_modo_simple,alignment=Qt.AlignCenter)
        layout_modos.addWidget(boton_modo_calendario,alignment=Qt.AlignCenter)

        layout_boton_volver.addWidget(boton_volver_al_menu_principal)

        layout.addStretch()
        layout.addWidget(contenedor_modos)
        layout.addStretch()
        layout.addWidget(contenedor_boton_volver,alignment=Qt.AlignLeft)

        self.stacked_widget.setCurrentWidget(self.overlay_menu_modos)
    
    def usar_modo_simple(self):
        if self.overlay_modo_simple.layout() is None:
            layout = QHBoxLayout()
            self.overlay_modo_simple.setLayout(layout)
            self.modo_elegido = "Simple"
            if self.modo_elegido == "Simple":
                self.tareas_modo_simple.setFixedSize(800,550)

            contenedor_lista_tareas = QWidget()
            self.contenedor_acciones = QWidget()
            self.contenedor_acciones.setFixedSize(400,600)
            contenedor_botones = QWidget()

            layout_lista_tareas = QVBoxLayout()
            self.layout_acciones = QStackedLayout()
            layout_botones = QVBoxLayout()

            contenedor_lista_tareas.setLayout(layout_lista_tareas)
            self.contenedor_acciones.setLayout(self.layout_acciones)
            contenedor_botones.setLayout(layout_botones)

            etiqueta_mis_tareas = QLabel("Mis tareas ⤵")
            aplicar_fade_in(etiqueta_mis_tareas,1000)

            etiqueta_acciones = QLabel("Acciones")
            aplicar_fade_in(etiqueta_acciones,1000)

            self.boton_ingresar_tarea = QPushButton("Ingresar")
            self.boton_ingresar_tarea.clicked.connect(lambda: self.layout_acciones.setCurrentIndex(1))
            self.boton_ingresar_tarea.clicked.connect(self.sonido_click.play)
            aplicar_fade_in(self.boton_ingresar_tarea,1000)
            self.boton_ingresar_tarea.setFixedSize(200,55)

            self.boton_buscar_tarea = QPushButton("Buscar")
            self.boton_buscar_tarea.clicked.connect(lambda: self.layout_acciones.setCurrentIndex(2))
            self.boton_buscar_tarea.clicked.connect(self.sonido_click.play)
            aplicar_fade_in(self.boton_buscar_tarea,1000)
            self.boton_buscar_tarea.setFixedSize(200,55)

            self.boton_modificar_tarea = QPushButton("Modificar")
            self.boton_modificar_tarea.clicked.connect(lambda: self.layout_acciones.setCurrentIndex(3))
            self.boton_modificar_tarea.clicked.connect(self.sonido_click.play)
            aplicar_fade_in(self.boton_modificar_tarea,1000)
            self.boton_modificar_tarea.setFixedSize(200,55)

            self.boton_ver_tarea = QPushButton("Visualizar")
            self.boton_ver_tarea.clicked.connect(lambda: self.layout_acciones.setCurrentIndex(4))
            self.boton_ver_tarea.clicked.connect(self.sonido_click.play)
            aplicar_fade_in(self.boton_ver_tarea,1000)
            self.boton_ver_tarea.setFixedSize(200,55)

            self.boton_eliminar_tarea = QPushButton("Eliminar")
            self.boton_eliminar_tarea.clicked.connect(self.eliminar_tarea)
            self.boton_eliminar_tarea.clicked.connect(self.sonido_click.play)
            aplicar_fade_in(self.boton_eliminar_tarea,1000)
            self.boton_eliminar_tarea.setFixedSize(200,55)

            boton_volver_al_menu_principal = QPushButton("Volver")
            aplicar_fade_in(boton_volver_al_menu_principal,1000)
            boton_volver_al_menu_principal.clicked.connect(self.menu_principal)
            boton_volver_al_menu_principal.clicked.connect(self.sonido_click_2.play)
            
            layout_lista_tareas.addWidget(etiqueta_mis_tareas,alignment=Qt.AlignCenter)
            layout_lista_tareas.addWidget(self.tareas_modo_simple)

            layout_botones.addStretch()
            layout_botones.addWidget(etiqueta_acciones,alignment=Qt.AlignTop | Qt.AlignCenter)
            layout_botones.addStretch()
            layout_botones.addWidget(self.boton_ingresar_tarea,alignment=Qt.AlignCenter)
            layout_botones.addStretch()
            layout_botones.addWidget(self.boton_buscar_tarea,alignment=Qt.AlignCenter)
            layout_botones.addStretch()
            layout_botones.addWidget(self.boton_modificar_tarea,alignment=Qt.AlignCenter)
            layout_botones.addStretch()
            layout_botones.addWidget(self.boton_ver_tarea,alignment=Qt.AlignCenter)
            layout_botones.addStretch()
            layout_botones.addWidget(self.boton_eliminar_tarea,alignment=Qt.AlignCenter)
            layout_botones.addStretch()
            layout_botones.addWidget(boton_volver_al_menu_principal,alignment=Qt.AlignRight)
            layout_botones.addStretch()

            layout.addWidget(contenedor_lista_tareas)
            layout.addWidget(self.contenedor_acciones)

            self.layout_acciones.addWidget(contenedor_botones)
            self.layout_acciones.addWidget(self.ingreso_de_tarea)
            self.layout_acciones.addWidget(self.busqueda_de_tarea)
            self.layout_acciones.addWidget(self.modificacion_de_tarea)
            self.layout_acciones.addWidget(self.visualizacion_de_tarea)

        self.layout_acciones.setCurrentIndex(0)
        self.stacked_widget.setCurrentWidget(self.overlay_modo_simple)
    
    def ingresar_tarea(self):
        contenedor = QWidget()
        layout = QGridLayout()
        contenedor.setLayout(layout)

        grupo_botones = QGroupBox()
        layout_grupo_botones = QVBoxLayout()
        grupo_botones.setLayout(layout_grupo_botones)

        self.combobox_categoria = QComboBox()
        self.combobox_categoria.addItems(["Estudio","Trabajo","Hogar","Personal","Otro"])
        aplicar_fade_in(self.combobox_categoria,1000)

        etiqueta_nombre = QLabel("Nombre:")
        aplicar_fade_in(etiqueta_nombre,1000)

        etiqueta_descripcion = QLabel("Descripción:")
        aplicar_fade_in(etiqueta_descripcion,1000)

        etiqueta_categoria = QLabel("Categoría:")
        aplicar_fade_in(etiqueta_categoria,1000)

        etiqueta_prioridad = QLabel("Prioridad:")
        aplicar_fade_in(etiqueta_prioridad,1000)

        self.nombre_tarea = QLineEdit()
        self.nombre_tarea.setPlaceholderText("Ingrese el nombre de la tarea aquí")
        aplicar_fade_in(self.nombre_tarea,1000)

        self.descripcion_tarea = QLineEdit()
        self.descripcion_tarea.setPlaceholderText("Ingrese la descripcion de la tarea aquí")
        aplicar_fade_in(self.descripcion_tarea,1000)

        self.boton_prioridad_alta = QRadioButton("Alta")
        self.boton_prioridad_alta.setChecked(True)
        self.boton_prioridad_alta.clicked.connect(self.sonido_click.play)
        aplicar_fade_in(self.boton_prioridad_alta,1000)

        self.boton_prioridad_media = QRadioButton("Media")
        self.boton_prioridad_media.clicked.connect(self.sonido_click.play)
        aplicar_fade_in(self.boton_prioridad_media,1000)

        self.boton_prioridad_baja = QRadioButton("Baja")
        self.boton_prioridad_baja.clicked.connect(self.sonido_click.play)
        aplicar_fade_in(self.boton_prioridad_baja,1000)

        layout_grupo_botones.addWidget(self.boton_prioridad_alta,alignment=Qt.AlignCenter)
        layout_grupo_botones.addWidget(self.boton_prioridad_media,alignment=Qt.AlignCenter)
        layout_grupo_botones.addWidget(self.boton_prioridad_baja,alignment=Qt.AlignCenter)

        boton_confirmar_ingresar_tarea = QPushButton("Confirmar")
        aplicar_fade_in(boton_confirmar_ingresar_tarea,1000)
        boton_confirmar_ingresar_tarea.setFixedSize(200,55)
        boton_confirmar_ingresar_tarea.clicked.connect(self.sonido_click.play)
        boton_confirmar_ingresar_tarea.clicked.connect(self.confirmar_ingresar_tarea)

        boton_cancelar_ingresar_tarea = QPushButton("Cancelar")
        aplicar_fade_in(boton_cancelar_ingresar_tarea,1000)
        boton_cancelar_ingresar_tarea.setFixedSize(200,55)
        boton_cancelar_ingresar_tarea.clicked.connect(self.sonido_click.play)
        boton_cancelar_ingresar_tarea.clicked.connect(lambda: self.layout_acciones.setCurrentIndex(0))

        layout.addWidget(etiqueta_nombre,0,0,1,3,alignment=Qt.AlignCenter)
        layout.addWidget(self.nombre_tarea,1,0,1,3)
        layout.addWidget(etiqueta_descripcion,2,0,1,3,alignment=Qt.AlignCenter)
        layout.addWidget(self.descripcion_tarea,3,0,1,3)
        layout.addWidget(etiqueta_categoria,4,0,1,2,alignment=Qt.AlignLeft)
        layout.addWidget(self.combobox_categoria,4,1,1,2)
        layout.addWidget(etiqueta_prioridad,5,0,1,2,alignment=Qt.AlignLeft)
        layout.addWidget(grupo_botones,5,1,1,2)
        layout.addWidget(boton_confirmar_ingresar_tarea,6,0,1,3,alignment=Qt.AlignCenter)
        layout.addWidget(boton_cancelar_ingresar_tarea,7,0,1,3,alignment=Qt.AlignCenter)

        return contenedor
    
    def confirmar_ingresar_tarea(self):
        nombre_tarea = self.nombre_tarea.text().strip()
        descripcion_tarea = self.descripcion_tarea.text().strip()
        categoria_elejida = self.combobox_categoria.currentText()
        prioridad_asignada = ""
        if self.boton_prioridad_alta.isChecked():
            prioridad_asignada = "Alta"
        if self.boton_prioridad_media.isChecked():
            prioridad_asignada = "Media"
        if self.boton_prioridad_baja.isChecked():
            prioridad_asignada = "Baja"
        if nombre_tarea and descripcion_tarea:
            tarea = f"{self.indice_tarea}) {nombre_tarea}"
            respuesta = QMessageBox.question(self,"Confirmar tarea","¿Desea ingresar la tarea?",QMessageBox.Yes | QMessageBox.No)
            if respuesta == QMessageBox.Yes:
                if self.buscar_tareas_duplicadas(nombre_tarea,descripcion_tarea):
                    return
                else:
                    item = QListWidgetItem(tarea)
                    item.setData(Qt.UserRole, nombre_tarea)
                    item.setData(Qt.UserRole + 1, descripcion_tarea)
                    item.setData(Qt.UserRole + 2, categoria_elejida)
                    item.setData(Qt.UserRole + 3, prioridad_asignada)
                    item.setData(Qt.UserRole + 4,self.indice_tarea)
                    self.tareas_modo_simple.addItem(item)
                    self.ordenar_indice_tareas()
                    self.layout_acciones.setCurrentIndex(0)
                    self.nombre_tarea.clear()
                    self.descripcion_tarea.clear()
                    self.combobox_categoria.setCurrentIndex(0)
                    self.boton_prioridad_alta.setChecked(True)
                    self.boton_prioridad_media.setChecked(False)
                    self.boton_prioridad_baja.setChecked(False)
            else:
                pass
        else:
            QMessageBox.warning(self,"Error","Los campos no pueden estar vacíos.")

    def ingresar_tarea_modo_calendario(self):
        contenedor = QWidget()
        layout = QGridLayout()
        contenedor.setLayout(layout)

        grupo_botones = QGroupBox()
        layout_grupo_botones = QVBoxLayout()
        grupo_botones.setLayout(layout_grupo_botones)

        self.combobox_categoria_modo_calendario = QComboBox()
        self.combobox_categoria_modo_calendario.addItems(["Estudio","Trabajo","Hogar","Personal","Otro"])
        aplicar_fade_in(self.combobox_categoria_modo_calendario,1000)

        etiqueta_nombre = QLabel("Nombre:")
        aplicar_fade_in(etiqueta_nombre,1000)

        etiqueta_descripcion = QLabel("Descripción:")
        aplicar_fade_in(etiqueta_descripcion,1000)

        etiqueta_categoria = QLabel("Categoría:")
        aplicar_fade_in(etiqueta_categoria,1000)

        etiqueta_prioridad = QLabel("Prioridad:")
        aplicar_fade_in(etiqueta_prioridad,1000)

        etiqueta_fecha_seleccionada = QLabel("Fecha:")
        aplicar_fade_in(etiqueta_fecha_seleccionada,1000)

        self.etiqueta_fecha_seleccionada = QLabel("Ninguna")
        self.etiqueta_fecha_seleccionada.setStyleSheet(estilo_etiqueta_fecha)
        self.etiqueta_fecha_seleccionada.setFixedSize(230,50)
        aplicar_fade_in(self.etiqueta_fecha_seleccionada,1000)

        self.nombre_tarea_modo_calendario = QLineEdit()
        self.nombre_tarea_modo_calendario.setPlaceholderText("Ingrese el nombre de la tarea aquí")
        aplicar_fade_in(self.nombre_tarea_modo_calendario,1000)

        self.descripcion_tarea_modo_calendario = QLineEdit()
        self.descripcion_tarea_modo_calendario.setPlaceholderText("Ingrese la descripcion de la tarea aquí")
        aplicar_fade_in(self.descripcion_tarea_modo_calendario,1000)

        self.boton_prioridad_alta_modo_calendario = QRadioButton("Alta")
        self.boton_prioridad_alta_modo_calendario.setChecked(True)
        self.boton_prioridad_alta_modo_calendario.clicked.connect(self.sonido_click.play)
        aplicar_fade_in(self.boton_prioridad_alta_modo_calendario,1000)

        self.boton_prioridad_media_modo_calendario = QRadioButton("Media")
        self.boton_prioridad_media_modo_calendario.clicked.connect(self.sonido_click.play)
        aplicar_fade_in(self.boton_prioridad_media_modo_calendario,1000)

        self.boton_prioridad_baja_modo_calendario = QRadioButton("Baja")
        self.boton_prioridad_baja_modo_calendario.clicked.connect(self.sonido_click.play)
        aplicar_fade_in(self.boton_prioridad_baja_modo_calendario,1000)

        layout_grupo_botones.addWidget(self.boton_prioridad_alta_modo_calendario,alignment=Qt.AlignCenter)
        layout_grupo_botones.addWidget(self.boton_prioridad_media_modo_calendario,alignment=Qt.AlignCenter)
        layout_grupo_botones.addWidget(self.boton_prioridad_baja_modo_calendario,alignment=Qt.AlignCenter)

        boton_confirmar_ingresar_tarea = QPushButton("Confirmar")
        aplicar_fade_in(boton_confirmar_ingresar_tarea,1000)
        boton_confirmar_ingresar_tarea.setFixedSize(200,55)
        boton_confirmar_ingresar_tarea.clicked.connect(self.sonido_click.play)
        boton_confirmar_ingresar_tarea.clicked.connect(self.confirmar_ingresar_tarea_modo_calendario)

        boton_cancelar_ingresar_tarea = QPushButton("Cancelar")
        aplicar_fade_in(boton_cancelar_ingresar_tarea,1000)
        boton_cancelar_ingresar_tarea.setFixedSize(200,55)
        boton_cancelar_ingresar_tarea.clicked.connect(self.sonido_click.play)
        boton_cancelar_ingresar_tarea.clicked.connect(lambda: self.layout_acciones_modo_calendario.setCurrentIndex(0))

        layout.addWidget(etiqueta_nombre,0,0,1,3,alignment=Qt.AlignCenter)
        layout.addWidget(self.nombre_tarea_modo_calendario,1,0,1,3)
        layout.addWidget(etiqueta_descripcion,2,0,1,3,alignment=Qt.AlignCenter)
        layout.addWidget(self.descripcion_tarea_modo_calendario,3,0,1,3)
        layout.addWidget(etiqueta_categoria,4,0,1,2,alignment=Qt.AlignLeft)
        layout.addWidget(self.combobox_categoria_modo_calendario,4,1,1,2)
        layout.addWidget(etiqueta_prioridad,5,0,1,2,alignment=Qt.AlignLeft)
        layout.addWidget(grupo_botones,5,1,1,2)
        layout.addWidget(etiqueta_fecha_seleccionada,6,0,1,3,alignment=Qt.AlignLeft)
        layout.addWidget(self.etiqueta_fecha_seleccionada,6,1,1,2,alignment=Qt.AlignCenter)
        layout.addWidget(boton_confirmar_ingresar_tarea,7,0,1,3,alignment=Qt.AlignCenter)
        layout.addWidget(boton_cancelar_ingresar_tarea,8,0,1,3,alignment=Qt.AlignCenter)

        return contenedor

    def confirmar_ingresar_tarea_modo_calendario(self):
        nombre_tarea = self.nombre_tarea_modo_calendario.text().strip()
        descripcion_tarea = self.descripcion_tarea_modo_calendario.text().strip()
        categoria_elejida = self.combobox_categoria_modo_calendario.currentText()
        prioridad_asignada = ""
        fecha_tarea = self.etiqueta_fecha_seleccionada.text()
        if self.boton_prioridad_alta_modo_calendario.isChecked():
            prioridad_asignada = "Alta"
        if self.boton_prioridad_media_modo_calendario.isChecked():
            prioridad_asignada = "Media"
        if self.boton_prioridad_baja_modo_calendario.isChecked():
            prioridad_asignada = "Baja"
        if nombre_tarea and descripcion_tarea:
            if fecha_tarea == "Ninguna":
                QMessageBox.warning(self,"Error","Debes seleccionar una fecha.")
                return
            tarea = f"{self.indice_tarea}) {nombre_tarea}"
            respuesta = QMessageBox.question(self,"Confirmar tarea","¿Desea ingresar la tarea?",QMessageBox.Yes | QMessageBox.No)
            if respuesta == QMessageBox.Yes:
                if self.buscar_tareas_duplicadas(nombre_tarea,descripcion_tarea):
                    return
                else:
                    item = QListWidgetItem(tarea)
                    item.setData(Qt.UserRole, nombre_tarea)
                    item.setData(Qt.UserRole + 1, descripcion_tarea)
                    item.setData(Qt.UserRole + 2, categoria_elejida)
                    item.setData(Qt.UserRole + 3, prioridad_asignada)
                    item.setData(Qt.UserRole + 4, self.indice_tarea)
                    item.setData(Qt.UserRole + 5, fecha_tarea)
                    self.tareas_modo_simple.addItem(item)
                    self.ordenar_indice_tareas()
                    self.layout_acciones_modo_calendario.setCurrentIndex(0)
                    self.nombre_tarea_modo_calendario.clear()
                    self.descripcion_tarea_modo_calendario.clear()
                    self.combobox_categoria_modo_calendario.setCurrentIndex(0)
                    self.boton_prioridad_alta_modo_calendario.setChecked(True)
                    self.boton_prioridad_media_modo_calendario.setChecked(False)
                    self.boton_prioridad_baja_modo_calendario.setChecked(False)
            else:
                pass
        else:
            QMessageBox.warning(self,"Error","Los campos no pueden estar vacíos.")

    def buscar_tareas_duplicadas(self,nombre_tarea,descripcion_tarea):
        for i in range(self.tareas_modo_simple.count()):
            tarea_duplicada = self.tareas_modo_simple.item(i)
            if tarea_duplicada.data(Qt.UserRole) == nombre_tarea:
                QMessageBox.warning(self,"Error","Ya existe una tarea con ese nombre.")
                return True
            if tarea_duplicada.data(Qt.UserRole + 1) == descripcion_tarea:
                QMessageBox.warning(self,"Error","Ya existe una tarea con esa descripción.")
                return True
        return False

    def buscar_tarea(self):
        contenedor = QWidget()
        layout = QVBoxLayout()
        contenedor.setLayout(layout)

        etiqueta_buscar_tarea = QLabel("Ingrese el nombre de la tarea a buscar aquí ⤵")
        etiqueta_buscar_tarea.setWordWrap(True)

        self.ingresar_tarea_a_buscar = QLineEdit()
        self.ingresar_tarea_a_buscar.setPlaceholderText("Ingrese el nombre de la tarea aquí")
        aplicar_fade_in(self.ingresar_tarea_a_buscar,1000)

        boton_buscar_tarea = QPushButton("Buscar")
        boton_buscar_tarea.clicked.connect(self.sonido_click.play)
        boton_buscar_tarea.clicked.connect(self.encontrar_tarea)
        boton_buscar_tarea.setFixedSize(200,55)
        aplicar_fade_in(boton_buscar_tarea,1000)

        boton_cancelar_buscar_tarea = QPushButton("Cancelar")
        aplicar_fade_in(boton_cancelar_buscar_tarea,1000)
        boton_cancelar_buscar_tarea.setFixedSize(200,55)
        boton_cancelar_buscar_tarea.clicked.connect(self.sonido_click.play)
        boton_cancelar_buscar_tarea.clicked.connect(lambda: self.layout_acciones.setCurrentIndex(0))

        layout.addStretch()
        layout.addWidget(etiqueta_buscar_tarea)
        layout.addStretch()
        layout.addWidget(self.ingresar_tarea_a_buscar)
        layout.addStretch()
        layout.addWidget(boton_buscar_tarea,alignment=Qt.AlignCenter)
        layout.addStretch()
        layout.addWidget(boton_cancelar_buscar_tarea,alignment=Qt.AlignCenter)
        layout.addStretch()
        return contenedor
    
    def buscar_tarea_modo_calendario(self):
        contenedor = QWidget()
        layout = QVBoxLayout()
        contenedor.setLayout(layout)

        etiqueta_buscar_tarea = QLabel("Ingrese el nombre de la tarea a buscar aquí ⤵")
        etiqueta_buscar_tarea.setWordWrap(True)

        self.ingresar_tarea_a_buscar_modo_calendario = QLineEdit()
        self.ingresar_tarea_a_buscar_modo_calendario.setPlaceholderText("Ingrese el nombre de la tarea aquí")
        aplicar_fade_in(self.ingresar_tarea_a_buscar_modo_calendario,1000)

        boton_buscar_tarea = QPushButton("Buscar")
        boton_buscar_tarea.clicked.connect(self.sonido_click.play)
        boton_buscar_tarea.clicked.connect(self.encontrar_tarea)
        boton_buscar_tarea.setFixedSize(200,55)
        aplicar_fade_in(boton_buscar_tarea,1000)

        boton_cancelar_buscar_tarea = QPushButton("Cancelar")
        aplicar_fade_in(boton_cancelar_buscar_tarea,1000)
        boton_cancelar_buscar_tarea.setFixedSize(200,55)
        boton_cancelar_buscar_tarea.clicked.connect(self.sonido_click.play)
        boton_cancelar_buscar_tarea.clicked.connect(lambda: self.layout_acciones_modo_calendario.setCurrentIndex(0))

        layout.addStretch()
        layout.addWidget(etiqueta_buscar_tarea)
        layout.addStretch()
        layout.addWidget(self.ingresar_tarea_a_buscar_modo_calendario)
        layout.addStretch()
        layout.addWidget(boton_buscar_tarea,alignment=Qt.AlignCenter)
        layout.addStretch()
        layout.addWidget(boton_cancelar_buscar_tarea,alignment=Qt.AlignCenter)
        layout.addStretch()
        return contenedor
    
    def encontrar_tarea(self):
        if self.tareas_modo_simple.count() == 0:
            QMessageBox.warning(self,"Error","No hay tareas ingresadas, prueba ingresando algo que tengas que hacer :)")
            return
        nombre_tarea_a_buscar = self.ingresar_tarea_a_buscar.text().strip()
        if not nombre_tarea_a_buscar:
            QMessageBox.warning(self,"Error","El campo de búsqueda está vacío.")
            return 
        for i in range(self.tareas_modo_simple.count()):
            item = self.tareas_modo_simple.item(i)
            datos = item.data(Qt.UserRole)
            if datos.lower() == nombre_tarea_a_buscar.lower():
                self.tareas_modo_simple.setCurrentItem(item)
                self.ingresar_tarea_a_buscar.clear()   
                return
        QMessageBox.information(self,"Tarea no encontrada","No hay tareas con el nombre que ingresaste.")
        self.ingresar_tarea_a_buscar.clear()            

    def modificar_tarea(self):
        contenedor = QWidget()
        layout = QGridLayout()
        contenedor.setLayout(layout)

        grupo_botones = QGroupBox()
        layout_grupo_botones = QVBoxLayout()
        grupo_botones.setLayout(layout_grupo_botones)

        self.combobox_categoria_modificada = QComboBox()
        self.combobox_categoria_modificada.addItems(["Estudio","Trabajo","Hogar","Personal","Otro"])
        aplicar_fade_in(self.combobox_categoria_modificada,1000)

        etiqueta_modificacion_tarea = QLabel("Modificación de tarea ⤵")
        aplicar_fade_in(etiqueta_modificacion_tarea,1000)

        etiqueta_nombre = QLabel("Nombre:")
        aplicar_fade_in(etiqueta_nombre,1000)

        etiqueta_descripcion = QLabel("Descripción:")
        aplicar_fade_in(etiqueta_descripcion,1000)

        etiqueta_categoria = QLabel("Categoría:")
        aplicar_fade_in(etiqueta_categoria,1000)

        etiqueta_prioridad = QLabel("Prioridad:")
        aplicar_fade_in(etiqueta_prioridad,1000)

        self.nombre_tarea_modificada = QLineEdit()
        self.nombre_tarea_modificada.setPlaceholderText("Ingrese el nuevo nombre aquí")
        aplicar_fade_in(self.nombre_tarea_modificada,1000)

        self.descripcion_tarea_modificada = QLineEdit()
        self.descripcion_tarea_modificada.setPlaceholderText("Ingrese la nueva descripcion aquí")
        aplicar_fade_in(self.descripcion_tarea_modificada,1000)

        self.boton_prioridad_alta_modificada = QRadioButton("Alta")
        self.boton_prioridad_alta_modificada.setChecked(True)
        self.boton_prioridad_alta_modificada.clicked.connect(self.sonido_click.play)
        aplicar_fade_in(self.boton_prioridad_alta_modificada,1000)

        self.boton_prioridad_media_modificada = QRadioButton("Media")
        self.boton_prioridad_media_modificada.clicked.connect(self.sonido_click.play)
        aplicar_fade_in(self.boton_prioridad_media_modificada,1000)

        self.boton_prioridad_baja_modificada = QRadioButton("Baja")
        self.boton_prioridad_baja_modificada.clicked.connect(self.sonido_click.play)
        aplicar_fade_in(self.boton_prioridad_baja_modificada,1000)

        layout_grupo_botones.addWidget(self.boton_prioridad_alta_modificada,alignment=Qt.AlignCenter)
        layout_grupo_botones.addWidget(self.boton_prioridad_media_modificada,alignment=Qt.AlignCenter)
        layout_grupo_botones.addWidget(self.boton_prioridad_baja_modificada,alignment=Qt.AlignCenter)

        boton_modificar_tarea = QPushButton("Modificar")
        aplicar_fade_in(boton_modificar_tarea,1000)
        boton_modificar_tarea.setFixedSize(200,55)
        boton_modificar_tarea.clicked.connect(self.sonido_click.play)
        boton_modificar_tarea.clicked.connect(self.modificar_tarea_seleccionada)

        boton_cancelar = QPushButton("Cancelar")
        aplicar_fade_in(boton_cancelar,1000)
        boton_cancelar.setFixedSize(200,55)
        boton_cancelar.clicked.connect(self.sonido_click.play)
        boton_cancelar.clicked.connect(lambda: self.layout_acciones.setCurrentIndex(0))
        boton_cancelar.clicked.connect(self.cancelar_modificacion_tarea)

        layout.addWidget(etiqueta_modificacion_tarea,0,0,1,3,alignment=Qt.AlignCenter)
        layout.addWidget(etiqueta_nombre,1,0,1,3,alignment=Qt.AlignCenter)
        layout.addWidget(self.nombre_tarea_modificada,2,0,1,3)
        layout.addWidget(etiqueta_descripcion,3,0,1,3,alignment=Qt.AlignCenter)
        layout.addWidget(self.descripcion_tarea_modificada,4,0,1,3)
        layout.addWidget(etiqueta_categoria,5,0,1,2,alignment=Qt.AlignLeft)
        layout.addWidget(self.combobox_categoria_modificada,5,1,1,2)
        layout.addWidget(etiqueta_prioridad,6,0,1,2,alignment=Qt.AlignLeft)
        layout.addWidget(grupo_botones,6,1,1,2)
        layout.addWidget(boton_modificar_tarea,7,0,1,3,alignment=Qt.AlignCenter)
        layout.addWidget(boton_cancelar,8,0,1,3,alignment=Qt.AlignCenter)

        return contenedor
    
    def modificar_tarea_modo_calendario(self):
        contenedor = QWidget()
        layout = QGridLayout()
        contenedor.setLayout(layout)

        grupo_botones = QGroupBox()
        layout_grupo_botones = QVBoxLayout()
        grupo_botones.setLayout(layout_grupo_botones)

        self.combobox_categoria_modificada_modo_calendario = QComboBox()
        self.combobox_categoria_modificada_modo_calendario.addItems(["Estudio","Trabajo","Hogar","Personal","Otro"])
        aplicar_fade_in(self.combobox_categoria_modificada_modo_calendario,1000)

        etiqueta_modificacion_tarea = QLabel("Modificación de tarea ⤵")
        aplicar_fade_in(etiqueta_modificacion_tarea,1000)

        etiqueta_nombre = QLabel("Nombre:")
        aplicar_fade_in(etiqueta_nombre,1000)

        etiqueta_descripcion = QLabel("Descripción:")
        aplicar_fade_in(etiqueta_descripcion,1000)

        etiqueta_categoria = QLabel("Categoría:")
        aplicar_fade_in(etiqueta_categoria,1000)

        etiqueta_prioridad = QLabel("Prioridad:")
        aplicar_fade_in(etiqueta_prioridad,1000)

        etiqueta_fecha_modificada = QLabel("Fecha:")
        aplicar_fade_in(etiqueta_fecha_modificada,1000)

        self.etiqueta_fecha_modificada_modo_calendario = QLabel("Ninguna")
        self.etiqueta_fecha_modificada_modo_calendario.setStyleSheet(estilo_etiqueta_fecha)
        self.etiqueta_fecha_modificada_modo_calendario.setFixedSize(230,50)
        aplicar_fade_in(self.etiqueta_fecha_modificada_modo_calendario,1000)

        self.nombre_tarea_modificada_modo_calendario = QLineEdit()
        self.nombre_tarea_modificada_modo_calendario.setPlaceholderText("Ingrese el nuevo nombre aquí")
        aplicar_fade_in(self.nombre_tarea_modificada_modo_calendario,1000)

        self.descripcion_tarea_modificada_modo_calendario = QLineEdit()
        self.descripcion_tarea_modificada_modo_calendario.setPlaceholderText("Ingrese la nueva descripcion aquí")
        aplicar_fade_in(self.descripcion_tarea_modificada_modo_calendario,1000)

        self.boton_prioridad_alta_modificada_modo_calendario = QRadioButton("Alta")
        self.boton_prioridad_alta_modificada_modo_calendario.setChecked(True)
        self.boton_prioridad_alta_modificada_modo_calendario.clicked.connect(self.sonido_click.play)
        aplicar_fade_in(self.boton_prioridad_alta_modificada_modo_calendario,1000)

        self.boton_prioridad_media_modificada_modo_calendario = QRadioButton("Media")
        self.boton_prioridad_media_modificada_modo_calendario.clicked.connect(self.sonido_click.play)
        aplicar_fade_in(self.boton_prioridad_media_modificada_modo_calendario,1000)

        self.boton_prioridad_baja_modificada_modo_calendario = QRadioButton("Baja")
        self.boton_prioridad_baja_modificada_modo_calendario.clicked.connect(self.sonido_click.play)
        aplicar_fade_in(self.boton_prioridad_baja_modificada_modo_calendario,1000)

        layout_grupo_botones.addWidget(self.boton_prioridad_alta_modificada_modo_calendario,alignment=Qt.AlignCenter)
        layout_grupo_botones.addWidget(self.boton_prioridad_media_modificada_modo_calendario,alignment=Qt.AlignCenter)
        layout_grupo_botones.addWidget(self.boton_prioridad_baja_modificada_modo_calendario,alignment=Qt.AlignCenter)

        boton_modificar_tarea = QPushButton("Modificar")
        aplicar_fade_in(boton_modificar_tarea,1000)
        boton_modificar_tarea.setFixedSize(200,55)
        boton_modificar_tarea.clicked.connect(self.sonido_click.play)
        boton_modificar_tarea.clicked.connect(self.modificar_tarea_seleccionada_modo_calendario)

        boton_cancelar = QPushButton("Cancelar")
        aplicar_fade_in(boton_cancelar,1000)
        boton_cancelar.setFixedSize(200,55)
        boton_cancelar.clicked.connect(self.sonido_click.play)
        boton_cancelar.clicked.connect(lambda: self.layout_acciones_modo_calendario.setCurrentIndex(0))
        boton_cancelar.clicked.connect(self.cancelar_modificacion_tarea)

        layout.addWidget(etiqueta_modificacion_tarea,0,0,1,3,alignment=Qt.AlignCenter)
        layout.addWidget(etiqueta_nombre,1,0,1,3,alignment=Qt.AlignCenter)
        layout.addWidget(self.nombre_tarea_modificada_modo_calendario,2,0,1,3)
        layout.addWidget(etiqueta_descripcion,3,0,1,3,alignment=Qt.AlignCenter)
        layout.addWidget(self.descripcion_tarea_modificada_modo_calendario,4,0,1,3)
        layout.addWidget(etiqueta_categoria,5,0,1,2,alignment=Qt.AlignLeft)
        layout.addWidget(self.combobox_categoria_modificada_modo_calendario,5,1,1,2)
        layout.addWidget(etiqueta_prioridad,6,0,1,2,alignment=Qt.AlignLeft)
        layout.addWidget(grupo_botones,6,1,1,2)
        layout.addWidget(etiqueta_fecha_modificada,7,0,1,3,alignment=Qt.AlignLeft)
        layout.addWidget(self.etiqueta_fecha_modificada_modo_calendario,7,1,1,2,alignment=Qt.AlignCenter)
        layout.addWidget(boton_modificar_tarea,8,0,1,3,alignment=Qt.AlignCenter)
        layout.addWidget(boton_cancelar,9,0,1,3,alignment=Qt.AlignCenter)

        return contenedor
        
    def modificar_tarea_seleccionada(self):
        if self.tareas_modo_simple.count() == 0:
            QMessageBox.warning(self,"Error","No hay tareas ingresadas, prueba ingresando algo que tengas que hacer :)")
            return
        
        tarea_seleccionada = self.tareas_modo_simple.currentItem()      
        if not tarea_seleccionada:
            QMessageBox.warning(self,"Error","Seleccione la tarea que desea modificar.")
            return
        
        nuevo_nombre_tarea = self.nombre_tarea_modificada.text().strip()
        nueva_descripcion_tarea = self.descripcion_tarea_modificada.text()
        nueva_categoria = self.combobox_categoria_modificada.currentText()
        nueva_prioridad = ''

        if self.boton_prioridad_alta_modificada.isChecked():
            nueva_prioridad = "Alta"
        elif self.boton_prioridad_media_modificada.isChecked():
            nueva_prioridad = "Media"
        else:
            nueva_prioridad = "Baja"

        if not nuevo_nombre_tarea or not nueva_descripcion_tarea:
            QMessageBox.warning(self,"Error","Los campos no pueden estar vacíos.")
            return
        
        indice = tarea_seleccionada.data(Qt.UserRole + 4)

        tarea_seleccionada.setText(f"{indice}) {nuevo_nombre_tarea}")
        tarea_seleccionada.setData(Qt.UserRole, nuevo_nombre_tarea)
        tarea_seleccionada.setData(Qt.UserRole + 1,nueva_descripcion_tarea)
        tarea_seleccionada.setData(Qt.UserRole + 2, nueva_categoria)
        tarea_seleccionada.setData(Qt.UserRole + 3, nueva_prioridad)

        self.nombre_tarea_modificada.clear()
        self.descripcion_tarea_modificada.clear()
        self.combobox_categoria_modificada.setCurrentIndex(0)
        self.boton_prioridad_alta_modificada.setChecked(True)
        self.boton_prioridad_media_modificada.setChecked(False)
        self.boton_prioridad_baja_modificada.setChecked(False)

    def modificar_tarea_seleccionada_modo_calendario(self):
        if self.tareas_modo_simple.count() == 0:
            QMessageBox.warning(self,"Error","No hay tareas ingresadas, prueba ingresando algo que tengas que hacer :)")
            return
        
        tarea_seleccionada = self.tareas_modo_simple.currentItem()      
        if not tarea_seleccionada:
            QMessageBox.warning(self,"Error","Seleccione la tarea que desea modificar.")
            return
        
        nuevo_nombre_tarea = self.nombre_tarea_modificada_modo_calendario.text().strip()
        nueva_descripcion_tarea = self.descripcion_tarea_modificada_modo_calendario.text()
        nueva_categoria = self.combobox_categoria_modificada_modo_calendario.currentText()
        nueva_fecha = self.etiqueta_fecha_modificada_modo_calendario.text()
        nueva_prioridad = ''

        if self.boton_prioridad_baja_modificada_modo_calendario.isChecked():
            nueva_prioridad = "Alta"
        elif self.boton_prioridad_baja_modificada_modo_calendario.isChecked():
            nueva_prioridad = "Media"
        else:
            nueva_prioridad = "Baja"

        if not nuevo_nombre_tarea or not nueva_descripcion_tarea:
            QMessageBox.warning(self,"Error","Los campos no pueden estar vacíos.")
            return
        
        indice = tarea_seleccionada.data(Qt.UserRole + 4)

        tarea_seleccionada.setText(f"{indice}) {nuevo_nombre_tarea}")
        tarea_seleccionada.setData(Qt.UserRole, nuevo_nombre_tarea)
        tarea_seleccionada.setData(Qt.UserRole + 1,nueva_descripcion_tarea)
        tarea_seleccionada.setData(Qt.UserRole + 2, nueva_categoria)
        tarea_seleccionada.setData(Qt.UserRole + 3, nueva_prioridad)
        tarea_seleccionada.setData(Qt.UserRole + 5, nueva_fecha)

        self.nombre_tarea_modificada.clear()
        self.descripcion_tarea_modificada.clear()
        self.etiqueta_fecha_modificada_modo_calendario.setText("Ninguna")
        self.combobox_categoria_modificada.setCurrentIndex(0)
        self.boton_prioridad_alta_modificada.setChecked(True)
        self.boton_prioridad_media_modificada.setChecked(False)
        self.boton_prioridad_baja_modificada.setChecked(False)

    def mostrar_datos_tarea_actual(self):
        tarea_seleccionada = self.tareas_modo_simple.currentItem()
        if not tarea_seleccionada:
            return
        
        nombre_tarea_seleccionada = tarea_seleccionada.data(Qt.UserRole)
        descripcion_tarea_seleccionada = tarea_seleccionada.data(Qt.UserRole + 1)
        categoria_tarea_seleccionada = tarea_seleccionada.data(Qt.UserRole + 2)
        prioridad_tarea_seleccionada = tarea_seleccionada.data(Qt.UserRole + 3)

        self.nombre_tarea_modificada.setText(nombre_tarea_seleccionada)
        self.descripcion_tarea_modificada.setText(descripcion_tarea_seleccionada)
        self.combobox_categoria_modificada.setCurrentText(categoria_tarea_seleccionada)
        
        if prioridad_tarea_seleccionada == "Alta":
            self.boton_prioridad_alta_modificada.setChecked(True)
        elif prioridad_tarea_seleccionada == "Media":
            self.boton_prioridad_media_modificada.setChecked(True)
        else:
            self.boton_prioridad_baja_modificada.setChecked(True)

    def mostrar_datos_tarea_actual_modo_calendario(self):
        tarea_seleccionada = self.tareas_modo_simple.currentItem()
        if not tarea_seleccionada:
            return
        
        nombre_tarea_seleccionada = tarea_seleccionada.data(Qt.UserRole)
        descripcion_tarea_seleccionada = tarea_seleccionada.data(Qt.UserRole + 1)
        categoria_tarea_seleccionada = tarea_seleccionada.data(Qt.UserRole + 2)
        prioridad_tarea_seleccionada = tarea_seleccionada.data(Qt.UserRole + 3)
        fecha_tarea_seleccionada = tarea_seleccionada.data(Qt.UserRole + 5)

        self.nombre_tarea_modificada_modo_calendario.setText(nombre_tarea_seleccionada)
        self.descripcion_tarea_modificada_modo_calendario.setText(descripcion_tarea_seleccionada)
        self.combobox_categoria_modificada_modo_calendario.setCurrentText(categoria_tarea_seleccionada)
        self.etiqueta_fecha_modificada_modo_calendario.setText(fecha_tarea_seleccionada)
        
        if prioridad_tarea_seleccionada == "Alta":
            self.boton_prioridad_alta_modificada_modo_calendario.setChecked(True)
        elif prioridad_tarea_seleccionada == "Media":
            self.boton_prioridad_media_modificada_modo_calendario.setChecked(True)
        else:
            self.boton_prioridad_baja_modificada_modo_calendario.setChecked(True)

    def cancelar_modificacion_tarea(self):
        self.nombre_tarea_modificada.clear()
        self.descripcion_tarea_modificada.clear()
        self.etiqueta_fecha_modificada_modo_calendario.setText("Ninguna")
        self.combobox_categoria_modificada.setCurrentIndex(0)
        self.boton_prioridad_alta_modificada.setChecked(True)
        self.boton_prioridad_media_modificada.setChecked(False)
        self.boton_prioridad_baja_modificada.setChecked(False)

    def eliminar_tarea(self):
        if self.tareas_modo_simple.count() == 0:
            QMessageBox.warning(self,"Error","No hay tareas ingresadas, prueba ingresando algo que tengas que hacer :)")
            return
        
        tarea_seleccionada = self.tareas_modo_simple.currentItem()
        if not tarea_seleccionada:
            QMessageBox.warning(self,"Error","Seleccione una tarea para eliminarla.")
            return
        
        respuesta = QMessageBox.question(self,"Eliminar tarea","¿Desea eliminar la tarea seleccionada?",QMessageBox.Yes | QMessageBox.No)
    
        if respuesta == QMessageBox.Yes:
            fila_de_la_tarea_seleccionada = self.tareas_modo_simple.row(tarea_seleccionada)
            self.tareas_modo_simple.takeItem(fila_de_la_tarea_seleccionada)
            self.ordenar_indice_tareas()

    def ordenar_indice_tareas(self):
        for i in range(self.tareas_modo_simple.count()):
            item = self.tareas_modo_simple.item(i)
            item.setData(Qt.UserRole + 4, i + 1)
            nombre_tarea = item.data(Qt.UserRole)
            item.setText(f"{i + 1}) {nombre_tarea}")

    def visualizar_tarea(self):
        contenedor = QWidget()
        layout = QVBoxLayout()
        contenedor.setLayout(layout)

        self.lienso = QTextEdit()
        self.lienso.setPlaceholderText("Aquí se pueden ver los datos de la tarea que selecciones.")
        aplicar_fade_in(self.lienso,1000)
        self.lienso.setReadOnly(True)

        boton_ver = QPushButton("Ver tarea")
        aplicar_fade_in(boton_ver,1000)
        boton_ver.clicked.connect(self.sonido_click.play)
        boton_ver.clicked.connect(self.ver_datos_tarea)
        boton_ver.setFixedSize(200,55)

        boton_volver = QPushButton("Volver")
        aplicar_fade_in(boton_volver,1000)
        boton_volver.clicked.connect(self.sonido_click.play)
        boton_volver.clicked.connect(lambda: self.layout_acciones.setCurrentIndex(0))
        boton_volver.clicked.connect(self.lienso.clear)
        boton_volver.setFixedSize(200,55)

        layout.addWidget(self.lienso)
        layout.addWidget(boton_ver,alignment=Qt.AlignCenter)
        layout.addWidget(boton_volver,alignment=Qt.AlignCenter)

        return contenedor
    
    def visualizar_tarea_modo_calendario(self):
        contenedor = QWidget()
        layout = QVBoxLayout()
        contenedor.setLayout(layout)

        self.lienso_modo_calendario = QTextEdit()
        self.lienso_modo_calendario.setPlaceholderText("Aquí se pueden ver los datos de la tarea que selecciones.")
        aplicar_fade_in(self.lienso_modo_calendario,1000)
        self.lienso_modo_calendario.setReadOnly(True)

        boton_ver = QPushButton("Ver tarea")
        aplicar_fade_in(boton_ver,1000)
        boton_ver.clicked.connect(self.sonido_click.play)
        boton_ver.clicked.connect(self.ver_datos_tarea_modo_calendario)
        boton_ver.setFixedSize(200,55)

        boton_volver = QPushButton("Volver")
        aplicar_fade_in(boton_volver,1000)
        boton_volver.clicked.connect(self.sonido_click.play)
        boton_volver.clicked.connect(lambda: self.layout_acciones_modo_calendario.setCurrentIndex(0))
        boton_volver.clicked.connect(self.lienso_modo_calendario.clear)
        boton_volver.setFixedSize(200,55)

        layout.addWidget(self.lienso_modo_calendario)
        layout.addWidget(boton_ver,alignment=Qt.AlignCenter)
        layout.addWidget(boton_volver,alignment=Qt.AlignCenter)

        return contenedor
    
    def ver_datos_tarea(self):
        if self.tareas_modo_simple.count() == 0:
            QMessageBox.warning(self,"Error","No hay tareas ingresadas, prueba ingresando algo que tengas que hacer :)")
            return
        
        tarea_seleccionada = self.tareas_modo_simple.currentItem()
        if not tarea_seleccionada:
            QMessageBox.warning(self,"Error","Seleccione una tarea para visualizar.")
            return
        
        nombre_tarea = tarea_seleccionada.data(Qt.UserRole)
        descripcion_tarea = tarea_seleccionada.data(Qt.UserRole + 1)
        categoria_tarea = tarea_seleccionada.data(Qt.UserRole + 2)
        prioridad_tarea = tarea_seleccionada.data(Qt.UserRole + 3)
        indice_tarea = tarea_seleccionada.data(Qt.UserRole + 4)

        datos_tarea = f"""
<b>Tarea N°:</b>    {indice_tarea}<br>
<b>Nombre:</b>  {nombre_tarea}<br>
<b>Descripción:</b> {descripcion_tarea}<br>
<b>Categoría:</b>   {categoria_tarea}<br>
<b>Prioridad:</b>   {prioridad_tarea}
"""
        self.lienso.setText(datos_tarea)

    def ver_datos_tarea_modo_calendario(self):
        if self.tareas_modo_simple.count() == 0:
            QMessageBox.warning(self,"Error","No hay tareas ingresadas, prueba ingresando algo que tengas que hacer :)")
            return
        
        tarea_seleccionada = self.tareas_modo_simple.currentItem()
        if not tarea_seleccionada:
            QMessageBox.warning(self,"Error","Seleccione una tarea para visualizar.")
            return
        
        nombre_tarea = tarea_seleccionada.data(Qt.UserRole)
        descripcion_tarea = tarea_seleccionada.data(Qt.UserRole + 1)
        categoria_tarea = tarea_seleccionada.data(Qt.UserRole + 2)
        prioridad_tarea = tarea_seleccionada.data(Qt.UserRole + 3)
        indice_tarea = tarea_seleccionada.data(Qt.UserRole + 4)
        fecha_tarea = tarea_seleccionada.data(Qt.UserRole + 5)

        datos_tarea = f"""
<b>Tarea N°:</b>    {indice_tarea}<br>
<b>Nombre:</b>  {nombre_tarea}<br>
<b>Descripción:</b> {descripcion_tarea}<br>
<b>Categoría:</b>   {categoria_tarea}<br>
<b>Prioridad:</b>   {prioridad_tarea}<br>
<b>Fecha:</b>    {fecha_tarea}
"""
        self.lienso_modo_calendario.setText(datos_tarea)
    
    def usar_modo_calendario(self):
        if self.overlay_modo_calendario.layout() is None:
            layout = QHBoxLayout()
            self.modo_elegido = "Calendario"
            if self.modo_elegido == "Calendario":
                self.tareas_modo_simple.setFixedSize(465,400)
                self.tareas_modo_simple.itemSelectionChanged.connect(self.mostrar_datos_tarea_actual_modo_calendario)
                self.tareas_modo_simple.currentItemChanged.connect(self.mostrar_datos_tarea_actual_modo_calendario)
            self.overlay_modo_calendario.setLayout(layout)

            contenedor_calendario = QWidget()
            layout_calendario = QGridLayout()
            contenedor_calendario.setLayout(layout_calendario)

            contenedor_botones = QWidget()
            layout_botones = QVBoxLayout()
            contenedor_botones.setLayout(layout_botones)

            self.contenedor_acciones_modo_calendario = QWidget()
            self.layout_acciones_modo_calendario = QStackedLayout()
            self.contenedor_acciones_modo_calendario.setLayout(self.layout_acciones_modo_calendario)

            self.calendario = QCalendarWidget()
            self.calendario.setFixedSize(400,400)
            #self.calendario.setNavigationBarVisible(False)
            self.calendario.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
            self.calendario.setSelectedDate(QDate.currentDate())
            self.calendario.setMinimumDate(QDate(anio_actual,1,1))
            self.calendario.setMaximumDate(QDate(anio_actual,12,31))
            aplicar_fade_in(self.calendario,1000)

            self.combobox_meses = QComboBox()
            aplicar_fade_in(self.combobox_meses,1000)
            self.meses=[]
            for mes in meses_diccionario:
                self.meses.append(mes)
            mes_elegido = self.meses[mes_actual - 1]
            print(mes_elegido)
            self.combobox_meses.addItems(self.meses)
            self.combobox_meses.setCurrentText(mes_elegido)
            self.combobox_meses.currentTextChanged.connect(self.actualizar_fechas)

            """self.combobox_anios = QComboBox()
            aplicar_fade_in(self.combobox_anios,1000)
            años=["2025","2026"]
            self.combobox_anios.addItems(años)
            self.combobox_anios.currentTextChanged.connect(self.actualizar_fechas)
            self.combobox_anios.currentTextChanged.connect(self.obtener_feriados)
            #self.combobox_anios.currentTextChanged.connect(self.marcar_feriados)
            self.combobox_anios.setCurrentText(str(anio_actual))"""

            self.label = QLabel()
            aplicar_fade_in(self.label,1000)
            self.label.setStyleSheet("font-size: 16px;")
            self.label.setFixedSize(400,100)
            self.label.setWordWrap(True)
            aplicar_fade_in(self.label,1000)

            etiqueta_acciones = QLabel("Acciones")
            aplicar_fade_in(etiqueta_acciones,1000)

            etiqueta_mes = QLabel("Mes:")
            aplicar_fade_in(etiqueta_mes,1000)

            etiqueta_año_complemento_1 = QLabel("Año:")
            aplicar_fade_in(etiqueta_año_complemento_1,1000)

            etiqueta_año_complemento_2 = QLabel(f"{anio_actual}")
            etiqueta_año_complemento_2.setStyleSheet(estilo_etiqueta_año)
            aplicar_fade_in(etiqueta_año_complemento_2,1000)

            etiqueta_mis_tareas = QLabel("Mis tareas ⤵")
            aplicar_fade_in(etiqueta_mis_tareas,1000)

            self.boton_ingresar_tarea_modo_calendario = QPushButton("Ingresar")
            self.boton_ingresar_tarea_modo_calendario.clicked.connect(lambda: self.layout_acciones_modo_calendario.setCurrentIndex(1))
            self.boton_ingresar_tarea_modo_calendario.clicked.connect(self.sonido_click.play)
            aplicar_fade_in(self.boton_ingresar_tarea_modo_calendario,1000)
            self.boton_ingresar_tarea_modo_calendario.setFixedSize(200,55)

            self.boton_buscar_tarea_modo_calendario = QPushButton("Buscar")
            self.boton_buscar_tarea_modo_calendario.clicked.connect(lambda: self.layout_acciones_modo_calendario.setCurrentIndex(2))
            self.boton_buscar_tarea_modo_calendario.clicked.connect(self.sonido_click.play)
            aplicar_fade_in(self.boton_buscar_tarea_modo_calendario,1000)
            self.boton_buscar_tarea_modo_calendario.setFixedSize(200,55)

            self.boton_modificar_tarea_modo_calendario = QPushButton("Modificar")
            self.boton_modificar_tarea_modo_calendario.clicked.connect(lambda: self.layout_acciones_modo_calendario.setCurrentIndex(3))
            self.boton_modificar_tarea_modo_calendario.clicked.connect(self.sonido_click.play)
            aplicar_fade_in(self.boton_modificar_tarea_modo_calendario,1000)
            self.boton_modificar_tarea_modo_calendario.setFixedSize(200,55)

            self.boton_ver_tarea_modo_calendario = QPushButton("Visualizar")
            self.boton_ver_tarea_modo_calendario.clicked.connect(lambda: self.layout_acciones_modo_calendario.setCurrentIndex(4))
            self.boton_ver_tarea_modo_calendario.clicked.connect(self.sonido_click.play)
            aplicar_fade_in(self.boton_ver_tarea_modo_calendario,1000)
            self.boton_ver_tarea_modo_calendario.setFixedSize(200,55)

            self.boton_eliminar_tarea_modo_calendario = QPushButton("Eliminar")
            self.boton_eliminar_tarea_modo_calendario.clicked.connect(self.eliminar_tarea)
            self.boton_eliminar_tarea_modo_calendario.clicked.connect(self.sonido_click.play)
            aplicar_fade_in(self.boton_eliminar_tarea_modo_calendario,1000)
            self.boton_eliminar_tarea_modo_calendario.setFixedSize(200,55)

            boton_volver_al_menu_principal = QPushButton("Volver")
            aplicar_fade_in(boton_volver_al_menu_principal,1000)
            boton_volver_al_menu_principal.clicked.connect(self.menu_principal)
            boton_volver_al_menu_principal.clicked.connect(self.sonido_click_2.play)

            boton_avanzar_mes = QPushButton(">>>")
            aplicar_fade_in(boton_avanzar_mes,1000)
            boton_avanzar_mes.clicked.connect(self.sonido_click.play)
            boton_avanzar_mes.setFixedSize(200,55)

            boton_retroceder_mes = QPushButton("<<<")
            aplicar_fade_in(boton_retroceder_mes,1000)
            boton_retroceder_mes.clicked.connect(self.sonido_click.play)
            boton_retroceder_mes.setFixedSize(200,55)

            #layout_calendario.addWidget(etiqueta_año_complemento_1,1,0)
            #layout_calendario.addWidget(etiqueta_año_complemento_2,1,1)
            #layout_calendario.addWidget(etiqueta_mes,1,2)
            #layout_calendario.addWidget(self.combobox_meses,1,3)
            layout_calendario.addWidget(etiqueta_mis_tareas,1,4,1,4,alignment=Qt.AlignCenter)
            layout_calendario.addWidget(self.calendario,2,0,1,4,alignment=Qt.AlignCenter)
            layout_calendario.addWidget(self.tareas_modo_simple,2,4,1,4,alignment=Qt.AlignRight)
            layout_calendario.addWidget(self.label,3,0,1,4,alignment=Qt.AlignCenter)

            layout_botones.addWidget(etiqueta_acciones,alignment=Qt.AlignTop | Qt.AlignCenter)
            layout_botones.addWidget(self.boton_ingresar_tarea_modo_calendario,alignment=Qt.AlignCenter)
            layout_botones.addWidget(self.boton_buscar_tarea_modo_calendario,alignment=Qt.AlignCenter)
            layout_botones.addWidget(self.boton_modificar_tarea_modo_calendario,alignment=Qt.AlignCenter)
            layout_botones.addWidget(self.boton_ver_tarea_modo_calendario,alignment=Qt.AlignCenter)
            layout_botones.addWidget(self.boton_eliminar_tarea_modo_calendario,alignment=Qt.AlignCenter)
            layout_botones.addWidget(boton_volver_al_menu_principal,alignment=Qt.AlignRight)

            #self.feriados = self.obtener_feriados()
            #self.marcar_feriados()
            #self.calendario.clicked.connect(self.mostrar_fecha)
            self.calendario.clicked.connect(self.mostrar_fecha_seleccionada)

            layout.addWidget(contenedor_calendario)
            layout.addWidget(self.contenedor_acciones_modo_calendario)

            self.layout_acciones_modo_calendario.addWidget(contenedor_botones)
            self.layout_acciones_modo_calendario.addWidget(self.ingreso_de_tarea_modo_calendario)
            self.layout_acciones_modo_calendario.addWidget(self.busqueda_de_tarea_modo_calendario)
            self.layout_acciones_modo_calendario.addWidget(self.modificacion_de_tarea_modo_calendario)
            self.layout_acciones_modo_calendario.addWidget(self.visualizacion_de_tarea_modo_calendario)

        self.layout_acciones_modo_calendario.setCurrentIndex(0)
        self.stacked_widget.setCurrentWidget(self.overlay_modo_calendario)

    def obtener_feriados(self):
        url = 'https://calendarific.com/api/v2/holidays'
        parametros = {
            "api_key": api_key,
            "country": pais,
            "year": anio_actual
        }

        response = requests.get(url, params=parametros)
        data = response.json()

        feriados = []
        
        for feriado in data['response']['holidays']:
            fecha = feriado['date']['datetime']
            razon = feriado['description'] #obtener descripcion de los dias feriados
            feriados.append((fecha['year'], fecha['month'], fecha['day'], razon)) #agregar a la lista feriados cada feriado con; año,mes,dia,descripcion

        return feriados
    
    def marcar_feriados(self):
        formato = QTextCharFormat()
        formato.setBackground(QBrush(QColor("lightcoral"))) #Color de los dias marcados como feriado en el calendario

        for year, month, day, _ in self.feriados:
            fecha = QDate(year, month, day)
            self.calendario.setDateTextFormat(fecha, formato)

    def mostrar_fecha(self, date):
        festividad = ""

        for year, month, day, razon in self.feriados:
            if year == date.year() and month == date.month() and day == date.day():
                festividad = f"Festividad: {razon}"
                break

        self.label.setText(f"Fecha seleccionada: {date.toString()}\n{festividad}")

    def mostrar_fecha_seleccionada(self,date):
        self.etiqueta_fecha_seleccionada.setText(f"{date.toString()}")
        self.etiqueta_fecha_modificada_modo_calendario.setText(f"{date.toString()}")

    def actualizar_fechas(self):
        mes_actual=meses_diccionario[self.combobox_meses.currentText()]
        self.calendario.setCurrentPage(anio_actual,mes_actual)
    
    def opciones(self):
        if self.overlay_opciones.layout() is None:
            layout = QVBoxLayout()
            self.overlay_opciones.setLayout(layout)
        else:
            layout = self.overlay_opciones.layout()
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()

        contenedor_opciones = QWidget()

        layout_opciones = QGridLayout()

        contenedor_opciones.setLayout(layout_opciones)

        etiqueta_opciones = QLabel("Opciones")
        aplicar_fade_in(etiqueta_opciones,1000)

        etiqueta_tema = QLabel("Tema:")
        aplicar_fade_in(etiqueta_tema,1000)

        etiqueta_modo = QLabel("Modo:")
        aplicar_fade_in(etiqueta_modo,1000)

        etiqueta_pantalla_completa = QLabel("Pantalla Completa:")
        aplicar_fade_in(etiqueta_pantalla_completa,1000)

        self.slider_volumen = QSlider(Qt.Horizontal)
        self.slider_volumen.setRange(0, 100)
        self.slider_volumen.setValue(self.volumen)
        self.slider_volumen.setFixedWidth(300)
        aplicar_fade_in(self.slider_volumen,1000)

        self.etiqueta_slider_volumen = QLabel(f"Volumen: {self.volumen}%")
        aplicar_fade_in(self.etiqueta_slider_volumen,1000)
        self.slider_volumen.valueChanged.connect(self.actualizar_volumen)

        self.combobox_modos = QComboBox()
        aplicar_fade_in(self.combobox_modos,1000)
        self.combobox_modos.addItems(['Simple','Calendario'])
        self.combobox_modos.setFixedSize(200,50)
        self.combobox_modos.setCurrentText(self.modo_elegido)

        self.combobox_temas = QComboBox()
        aplicar_fade_in(self.combobox_temas,1000)
        self.combobox_temas.addItems(['Claro','Oscuro'])
        self.combobox_temas.setFixedSize(200,50)
        self.combobox_temas.setCurrentText(self.tema_elejido)

        self.boton_pantalla_completa = QPushButton()
        self.boton_pantalla_completa.clicked.connect(self.sonido_click.play)
        self.boton_pantalla_completa.clicked.connect(self.configurar_pantalla_completa)
        aplicar_fade_in(self.boton_pantalla_completa,1000)
        self.boton_pantalla_completa.setFixedSize(200,55)
        if self.pantalla_completa == False:
            self.boton_pantalla_completa.setText("NO")
        else:
            self.boton_pantalla_completa.setText("SI")

        boton_volver_al_menu_principal = QPushButton("Volver")
        aplicar_fade_in(boton_volver_al_menu_principal,1000)
        boton_volver_al_menu_principal.clicked.connect(self.menu_principal)
        boton_volver_al_menu_principal.clicked.connect(self.sonido_click_2.play)

        boton_aplicar_cambios = QPushButton("Aplicar Cambios")
        aplicar_fade_in(boton_aplicar_cambios,1000)
        boton_aplicar_cambios.clicked.connect(self.aplicar_cambios)
        boton_aplicar_cambios.clicked.connect(self.sonido_click_3.play)

        layout_opciones.addWidget(etiqueta_opciones,1,0,1,2,alignment=Qt.AlignTop | Qt.AlignCenter)
        layout_opciones.addWidget(etiqueta_tema,2,0,alignment=Qt.AlignTop | Qt.AlignCenter)
        layout_opciones.addWidget(self.combobox_temas,2,1,alignment=Qt.AlignTop | Qt.AlignCenter)
        if self.modo_elegido != "":
            layout_opciones.addWidget(etiqueta_modo,3,0,alignment=Qt.AlignTop | Qt.AlignCenter)
            layout_opciones.addWidget(self.combobox_modos,3,1,alignment=Qt.AlignTop | Qt.AlignCenter)
        else:
            pass
        layout_opciones.addWidget(etiqueta_pantalla_completa,4,0,alignment=Qt.AlignTop | Qt.AlignCenter)
        layout_opciones.addWidget(self.boton_pantalla_completa,4,1,alignment=Qt.AlignTop | Qt.AlignCenter)
        layout_opciones.addWidget(self.etiqueta_slider_volumen,5,0,alignment=Qt.AlignTop | Qt.AlignCenter)
        layout_opciones.addWidget(self.slider_volumen,5,1,alignment=Qt.AlignTop | Qt.AlignCenter)
        layout_opciones.addWidget(boton_volver_al_menu_principal,6,0,alignment=Qt.AlignLeft)
        layout_opciones.addWidget(boton_aplicar_cambios,6,0,1,2,alignment=Qt.AlignCenter)
        
        layout.addWidget(contenedor_opciones)

        self.stacked_widget.setCurrentWidget(self.overlay_opciones)
    
    def aplicar_cambios(self):
        if self.modo_elegido:
            self.modo_elegido = self.combobox_modos.currentText()
        else:
            pass
        self.tema_elejido = self.combobox_temas.currentText()

        if self.tema_elejido == "Oscuro":
            self.setStyleSheet(estilo_tema_oscuro)
            ruta_nueva = os.path.join(self.script_dir, "./recursos/videos/portada_tema_oscuro.mp4")
            self.media_player.stop()
            self.playlist.clear()
            self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(ruta_nueva)))
            self.playlist.setCurrentIndex(0)
            self.media_player.setPlaylist(self.playlist)
            self.media_player.setVideoOutput(self.video_item)
            self.media_player.setVolume(0)
            self.media_player.play()
        else:
            self.setStyleSheet(estilo)
            ruta_nueva = os.path.join(self.script_dir, "./recursos/videos/portada.mp4")
            self.media_player.stop()
            self.playlist.clear()
            self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(ruta_nueva)))
            self.playlist.setCurrentIndex(0)
            self.media_player.setPlaylist(self.playlist)
            self.media_player.setVideoOutput(self.video_item)
            self.media_player.setVolume(0)
            self.media_player.play()

    def configurar_pantalla_completa(self):
        if self.pantalla_completa:
            self.boton_pantalla_completa.setText("NO")
            self.pantalla_completa=False
            self.showMaximized()
        else:
            self.boton_pantalla_completa.setText("SI")
            self.pantalla_completa=True
            self.showFullScreen()

    def actualizar_volumen(self, valor):
        limpiar_consola()
        print(f"Volumen: {valor}")
        self.volumen=valor
        valor_adaptado = valor / 100
        self.sonido_click.setVolume(valor_adaptado)
        self.sonido_click_2.setVolume(valor_adaptado * 0.2) #para que no se escuche tan alto (es medio molesto este sonido cuando el volumen es alto)
        self.sonido_click_3.setVolume(valor_adaptado)
        self.media_player.setVolume(valor)
        if valor < 10:
            self.etiqueta_slider_volumen.setText(f"Volumen:  {valor}%")
        else:
            self.etiqueta_slider_volumen.setText(f"Volumen: {valor}%")
        self.etiqueta_slider_volumen.setStyleSheet("background:transparent;")

    def centrar_ventana(self):
        pantalla = QApplication.primaryScreen().availableGeometry()
        ventana = self.frameGeometry()
        ventana.moveCenter(pantalla.center())
        self.move(ventana.topLeft())

    def resizeEvent(self, event):
        nuevo_tamaño = QSizeF(self.size())
        widget = self.centralWidget()
        self.video_item.setSize(nuevo_tamaño)#Ajustar el tamaño del video
        self.view.setGeometry(0, 0, self.width(), self.height())#Ajustar el tamaño del visor de la escena
        self.view.setSceneRect(0, 0, self.width(), self.height())
        widget.setGeometry(0, 0, self.width(), self.height())

        super().resizeEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gestor_de_tareas = Tdl()
    gestor_de_tareas.show()
    sys.exit(app.exec_())
