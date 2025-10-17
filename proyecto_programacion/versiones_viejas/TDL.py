import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

from estilos import *

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

class Tdl(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestor de Tareas - Hecho por Bruno González y Martín Baras")
        self.setGeometry(100, 100, 800, 600)
        self.modo_elejido = ""
        self.tema_elejido = ""
        self.tareas_modo_simple = QListWidget()
        self.item = QListWidgetItem()
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

        self.menu_principal()

    def menu_principal(self):
        self.overlay = QWidget(self)
        self.overlay_layout = QVBoxLayout()
        self.overlay_layout.setAlignment(Qt.AlignCenter)

        etiqueta = QLabel("To Do List")
        aplicar_fade_in(etiqueta,1000)
        etiqueta_2 = QLabel("Gestor de tareas")
        aplicar_fade_in(etiqueta_2,1000)

        boton_iniciar = QPushButton("Iniciar")
        if self.modo_elejido == "Simple":
            boton_iniciar.clicked.connect(self.usar_modo_simple)
            boton_iniciar.clicked.connect(self.sonido_click.play)
        elif self.modo_elejido == "Calendario":
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
        
        self.overlay_layout.addWidget(etiqueta,alignment=Qt.AlignCenter | Qt.AlignTop)
        self.overlay_layout.addWidget(etiqueta_2,alignment=Qt.AlignCenter | Qt.AlignTop)
        self.overlay_layout.addWidget(boton_iniciar)
        self.overlay_layout.addWidget(boton_informacion)
        self.overlay_layout.addWidget(boton_opciones)
        self.overlay_layout.addWidget(boton_salir)

        self.overlay.setLayout(self.overlay_layout)
        self.setCentralWidget(self.overlay)
        return self.overlay
    
    def menu_informacion(self):
        self.overlay = QWidget(self)
        self.overlay_layout = QVBoxLayout()

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

        self.overlay_layout.addWidget(informacion,alignment=Qt.AlignCenter)
        self.overlay_layout.addWidget(boton_volver_al_menu_principal,alignment=Qt.AlignLeft)
        self.overlay.setLayout(self.overlay_layout)
        self.setCentralWidget(self.overlay)
        return self.overlay
    
    def menu_modos(self):
        self.overlay = QWidget(self)
        self.overlay_layout_principal = QVBoxLayout()
        self.overlay.setLayout(self.overlay_layout_principal)

        self.overlay_modos = QWidget(self)
        self.overlay_modos_layout = QVBoxLayout()
        self.overlay_modos_layout.setAlignment(Qt.AlignCenter)
        self.overlay_modos.setLayout(self.overlay_modos_layout)

        self.overlay_boton_volver = QWidget(self)
        self.overlay_layout_boton_volver= QVBoxLayout()

        etiqueta_modo = QLabel("Elije el modo que quieras usar:")
        aplicar_fade_in(etiqueta_modo,1000)

        boton_modo_simple = QPushButton("Simple")
        boton_modo_simple.clicked.connect(self.usar_modo_simple)
        boton_modo_simple.clicked.connect(self.sonido_click.play)
        aplicar_fade_in(boton_modo_simple,1000)
        boton_modo_calendario = QPushButton("Calendario")
        boton_modo_calendario.clicked.connect(self.usar_modo_calendario)
        boton_modo_calendario.clicked.connect(self.sonido_click.play)
        aplicar_fade_in(boton_modo_calendario,1000)

        boton_volver_al_menu_principal = QPushButton("Volver")
        aplicar_fade_in(boton_volver_al_menu_principal,1000)
        boton_volver_al_menu_principal.clicked.connect(self.menu_principal)
        boton_volver_al_menu_principal.clicked.connect(self.sonido_click_2.play)

        self.overlay_modos_layout.addWidget(etiqueta_modo,alignment=Qt.AlignCenter)
        self.overlay_modos_layout.addWidget(boton_modo_simple)
        self.overlay_modos_layout.addWidget(boton_modo_calendario)

        self.overlay_layout_boton_volver.addWidget(boton_volver_al_menu_principal)
        self.overlay_boton_volver.setLayout(self.overlay_layout_boton_volver)

        self.overlay_layout_principal.addStretch()
        self.overlay_layout_principal.addWidget(self.overlay_modos)
        self.overlay_layout_principal.addStretch()
        self.overlay_layout_principal.addWidget(self.overlay_boton_volver,alignment=Qt.AlignLeft)
        self.setCentralWidget(self.overlay)
        return self.overlay
    
    def usar_modo_simple(self):
        self.modo_elejido = "Simple"
        self.overlay_ingresar_tarea = QWidget(self)
        self.overlay_lista_tareas = QWidget(self)

        self.overlay_ingresar_tarea_layout = QVBoxLayout()
        self.overlay_lista_tareas_layout = QVBoxLayout()

        self.overlay_ingresar_tarea.setLayout(self.overlay_ingresar_tarea_layout)
        self.overlay_lista_tareas.setLayout(self.overlay_lista_tareas_layout)

        self.tareas_modo_simple = QListWidget()
        self.item = QListWidgetItem()

        etiqueta_acciones = QLabel("Acciones")

        self.boton_ingresar_tarea = QPushButton("Ingresar")
        self.boton_ingresar_tarea.clicked.connect(self.ingresar_tarea)
        self.boton_ingresar_tarea.clicked.connect(self.sonido_click.play)

        self.boton_buscar_tarea = QPushButton("Buscar")
        self.boton_buscar_tarea.clicked.connect(self.buscar_tarea)
        self.boton_buscar_tarea.clicked.connect(self.sonido_click.play)

        self.boton_modificar_tarea = QPushButton("Modificar")
        self.boton_modificar_tarea.clicked.connect(self.modificar_tarea)
        self.boton_modificar_tarea.clicked.connect(self.sonido_click.play)

        self.boton_eliminar_tarea = QPushButton("Eliminar")
        self.boton_eliminar_tarea.clicked.connect(self.eliminar_tarea)
        self.boton_eliminar_tarea.clicked.connect(self.sonido_click.play)

        boton_volver_al_menu_principal = QPushButton("Volver")
        boton_volver_al_menu_principal.clicked.connect(self.menu_principal)
        boton_volver_al_menu_principal.clicked.connect(self.sonido_click_2.play)

        self.overlay_ingresar_tarea_layout.addStretch()
        self.overlay_ingresar_tarea_layout.addWidget(etiqueta_acciones,alignment=Qt.AlignTop | Qt.AlignCenter)
        self.overlay_ingresar_tarea_layout.addStretch()
        self.overlay_ingresar_tarea_layout.addWidget(self.boton_ingresar_tarea,alignment=Qt.AlignCenter)
        self.overlay_ingresar_tarea_layout.addStretch()
        self.overlay_ingresar_tarea_layout.addWidget(self.boton_buscar_tarea,alignment=Qt.AlignCenter)
        self.overlay_ingresar_tarea_layout.addStretch()
        self.overlay_ingresar_tarea_layout.addWidget(self.boton_modificar_tarea,alignment=Qt.AlignCenter)
        self.overlay_ingresar_tarea_layout.addStretch()
        self.overlay_ingresar_tarea_layout.addWidget(self.boton_eliminar_tarea,alignment=Qt.AlignCenter)
        self.overlay_ingresar_tarea_layout.addStretch()
        self.overlay_ingresar_tarea_layout.addWidget(boton_volver_al_menu_principal,alignment=Qt.AlignRight)
        self.overlay_ingresar_tarea_layout.addStretch()
        
        self.overlay_lista_tareas_layout.addWidget(self.tareas_modo_simple)

        self.splitter = QSplitter(Qt.Horizontal)
        aplicar_fade_in(self.splitter,1000)

        self.splitter.addWidget(self.overlay_lista_tareas)
        self.splitter.addWidget(self.overlay_ingresar_tarea)

        self.splitter.setSizes([1000,100])
        self.splitter.handle(1).setEnabled(False)
        self.setCentralWidget(self.splitter)
        return self.splitter,self.modo_elejido
    
    def ingresar_tarea(self):
        pass

    def buscar_tarea(self):
        pass

    def modificar_tarea(self):
        pass

    def eliminar_tarea(self):
        pass
    
    def usar_modo_calendario(self):
        print("Has elejido el modo calendario")
        self.modo_elejido = "Calendario"
        return self.modo_elejido
    
    def opciones(self):
        self.overlay = QWidget(self)
        self.overlay_layout_principal = QVBoxLayout()
        self.overlay.setLayout(self.overlay_layout_principal)

        self.overlay_etiqueta_opciones = QWidget(self)
        self.overlay_etiqueta_opciones_layout = QVBoxLayout()
        self.overlay_etiqueta_opciones.setLayout(self.overlay_etiqueta_opciones_layout)

        self.overlay_opciones = QWidget(self)
        self.overlay_opciones_layout = QGridLayout()
        self.overlay_opciones.setLayout(self.overlay_opciones_layout)

        etiqueta = QLabel("Opciones")
        aplicar_fade_in(etiqueta,1000)

        etiqueta_tema = QLabel("Tema:")
        aplicar_fade_in(etiqueta_tema,1000)

        etiqueta_modo = QLabel("Modo:")
        aplicar_fade_in(etiqueta_modo,1000)

        self.combobox_modos = QComboBox()
        aplicar_fade_in(self.combobox_modos,1000)
        self.combobox_modos.addItems(['Simple','Calendario'])
        self.combobox_modos.setFixedSize(200,50)
        self.combobox_modos.setCurrentText(self.modo_elejido)

        self.combobox_temas = QComboBox()
        aplicar_fade_in(self.combobox_temas,1000)
        self.combobox_temas.addItems(['Claro','Oscuro'])
        self.combobox_temas.setFixedSize(200,50)
        self.combobox_temas.setCurrentText(self.tema_elejido)

        boton_volver_al_menu_principal = QPushButton("Volver")
        aplicar_fade_in(boton_volver_al_menu_principal,1000)
        boton_volver_al_menu_principal.clicked.connect(self.menu_principal)
        boton_volver_al_menu_principal.clicked.connect(self.sonido_click_2.play)

        boton_aplicar_cambios = QPushButton("Aplicar Cambios")
        aplicar_fade_in(boton_aplicar_cambios,1000)
        boton_aplicar_cambios.clicked.connect(self.aplicar_cambios)
        boton_aplicar_cambios.clicked.connect(self.sonido_click_3.play)

        self.overlay_etiqueta_opciones_layout.addWidget(etiqueta,alignment=Qt.AlignCenter)

        self.overlay_opciones_layout.addWidget(etiqueta_tema,1,0,alignment=Qt.AlignTop | Qt.AlignCenter)
        self.overlay_opciones_layout.addWidget(self.combobox_temas,1,1,alignment=Qt.AlignTop | Qt.AlignCenter)
        if self.modo_elejido != "":
            self.overlay_opciones_layout.addWidget(etiqueta_modo,2,0,alignment=Qt.AlignTop | Qt.AlignCenter)
            self.overlay_opciones_layout.addWidget(self.combobox_modos,2,1,alignment=Qt.AlignTop | Qt.AlignCenter)
        else:
            pass
        self.overlay_opciones_layout.addWidget(boton_volver_al_menu_principal,3,0,alignment=Qt.AlignLeft)
        self.overlay_opciones_layout.addWidget(boton_aplicar_cambios,3,0,1,2,alignment=Qt.AlignCenter)
        
        self.overlay_layout_principal.addWidget(self.overlay_etiqueta_opciones)
        self.overlay_layout_principal.addWidget(self.overlay_opciones)
        self.setCentralWidget(self.overlay)
        return self.overlay
    
    def aplicar_cambios(self):
        if self.modo_elejido:
            self.modo_elejido = self.combobox_modos.currentText()
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
    gestor_de_tareas.showMaximized()
    sys.exit(app.exec_())
