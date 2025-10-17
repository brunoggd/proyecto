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

def limpiar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')

class Tdl(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestor de Tareas - Hecho por Bruno González y Martín Baras")
        self.setGeometry(100, 100, 800, 600)
        self.modo_elejido = ""
        self.tema_elejido = ""
        self.indice_tarea = 0
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

        self.ingreso_de_tarea = self.ingresar_tarea()
        self.busqueda_de_tarea = self.buscar_tarea()

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
            self.modo_elejido = "Simple"

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
            self.boton_modificar_tarea.clicked.connect(self.modificar_tarea)
            self.boton_modificar_tarea.clicked.connect(self.sonido_click.play)
            aplicar_fade_in(self.boton_modificar_tarea,1000)
            self.boton_modificar_tarea.setFixedSize(200,55)

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
            layout_botones.addWidget(self.boton_eliminar_tarea,alignment=Qt.AlignCenter)
            layout_botones.addStretch()
            layout_botones.addWidget(boton_volver_al_menu_principal,alignment=Qt.AlignRight)
            layout_botones.addStretch()

            layout.addWidget(contenedor_lista_tareas)
            layout.addWidget(self.contenedor_acciones)

            self.layout_acciones.addWidget(contenedor_botones)
            self.layout_acciones.addWidget(self.ingreso_de_tarea)
            self.layout_acciones.addWidget(self.busqueda_de_tarea)

        self.layout_acciones.setCurrentIndex(0)
        self.stacked_widget.setCurrentWidget(self.overlay_modo_simple)
    
    def ingresar_tarea(self):
        contenedor = QWidget()
        layout = QVBoxLayout()
        contenedor.setLayout(layout)

        self.tarea_ingresada = QLineEdit()
        self.tarea_ingresada.setPlaceholderText("Ingrese la tarea aquí")
        aplicar_fade_in(self.tarea_ingresada,1000)

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

        layout.addStretch()
        layout.addWidget(self.tarea_ingresada)
        layout.addStretch()
        layout.addWidget(boton_confirmar_ingresar_tarea,alignment=Qt.AlignCenter)
        layout.addStretch()
        layout.addWidget(boton_cancelar_ingresar_tarea,alignment=Qt.AlignCenter)
        layout.addStretch()

        return contenedor
    
    def confirmar_ingresar_tarea(self):
        tarea_ingresada = self.tarea_ingresada.text().strip()
        if tarea_ingresada:
            self.indice_tarea += 1
            tarea = f"{self.indice_tarea}) {tarea_ingresada}"
            respuesta = QMessageBox.question(self,"Confirmar tarea","¿Desea ingresar la tarea?",QMessageBox.Yes | QMessageBox.No)
            if respuesta == QMessageBox.Yes:
                item = QListWidgetItem(tarea)
                self.tareas_modo_simple.addItem(item)
                self.layout_acciones.setCurrentIndex(0)
            else:
                pass
        else:
            QMessageBox.warning(self,"Error","La tarea no puede estar vacía")

    def buscar_tarea(self):
        contenedor = QWidget()
        layout = QVBoxLayout()
        contenedor.setLayout(layout)

        combobox_tareas = QComboBox()
        aplicar_fade_in(combobox_tareas,1000)

        boton_cancelar_buscar_tarea = QPushButton("Cancelar")
        aplicar_fade_in(boton_cancelar_buscar_tarea,1000)
        boton_cancelar_buscar_tarea.setFixedSize(200,55)
        boton_cancelar_buscar_tarea.clicked.connect(self.sonido_click.play)
        boton_cancelar_buscar_tarea.clicked.connect(lambda: self.layout_acciones.setCurrentIndex(0))

        for tarea in range(self.tareas_modo_simple.count()):
            item = QListWidgetItem(tarea)
            combobox_tareas.addItem(item)

        layout.addWidget(combobox_tareas)
        layout.addWidget(boton_cancelar_buscar_tarea,alignment=Qt.AlignRight)
        return contenedor

    def modificar_tarea(self):
        pass

    def eliminar_tarea(self):
        pass
    
    def usar_modo_calendario(self):
        print("Has elejido el modo calendario")
        self.modo_elejido = "Calendario"
        return self.modo_elejido
    
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
        self.combobox_modos.setCurrentText(self.modo_elejido)

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
        if self.modo_elejido != "":
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
    gestor_de_tareas.showMaximized()
    sys.exit(app.exec_())
