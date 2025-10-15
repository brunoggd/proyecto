import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

import requests

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

def obtener_equipo(equipo):
    url = f"https://www.thesportsdb.com/api/v1/json/123/searchteams.php?t={equipo}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['teams']:
            team = data['teams'][0]
            texto=(
                f"Nombre: {team['strTeam']}\n"
                f"Estadio: {team['strStadium']}\n"
                f"Liga en la que juega: {team['strLeague']}\n"
                f"País: {team['strCountry']}\n"
                f"Descripción: {team['strDescriptionES']}\n")
        else:
            print("No se encontró el equipo que buscabas, ingresa el nombre completo.")
    else:
        print("Error:", response.status_code)
    return texto

def obtener_jugador(jugador):
    url = f"https://www.thesportsdb.com/api/v1/json/123/searchplayers.php?p={jugador}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['player']:
            player = data['player'][0]
            texto=(
                f"Nombre: {player['strPlayer']}\n"
                f"Género:  {player['strGender']}\n"
                f"Nacionalidad: {player['strNationality']}\n"
                f"Fecha de nacimiento: {player['dateBorn']}\n"
                f"Club en el que juega: {player['strTeam']}\n"
                f"Posición: {player['strPosition']}\n")
        else:
            print("No se encontró el jugador que buscabas, ingresa el nombre completo.")
    else:
        print("Error:", response.status_code)
    return texto

def obtener_ligas():
    url = "https://www.thesportsdb.com/api/v1/json/123/all_leagues.php"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['leagues']
    else:
        print("Error:", response.status_code)
    return []

def obtener_liga(liga):
    url = f"https://www.thesportsdb.com/api/v1/json/123/lookupleague.php?id={liga}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['leagues']:
            liga = data['leagues'][0]
            texto=(
                f"Nombre de la liga: {liga['strLeague']}\n"
                f"País de la liga: {liga['strCountry']}\n"
                f"Temporada actual: {liga['strCurrentSeason']}\n"
                f"Descripción: {liga['strDescriptionES']}\n")
        else:
            print("No se encontró la liga que buscabas, ingresa el nombre completo.")
    else:
        print("Error:", response.status_code)
    return texto

class informefutbol(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Guía Futbolística")
        self.setGeometry(100, 100, 900, 600)
        self.setStyleSheet("""
        QMainWindow {background:transparent;}
                           
        QPushButton {background-color: #0F0063;
                    color: white;
                    font-size: 20px;
                    border-radius: 20px;
                    padding: 10px 10px;
                    font-family: 'Impact';}
                           
        QLabel {color: white;
                font-size: 50px;
                font-family: 'SimSun';}
                           
        QTextEdit {background-color: rgba(0,0,0,100);
                    color: white;
                    font-size: 30px;
                    font-family: 'Georgia';}
                           
        QLineEdit {background-color: rgba(0,0,0,100);
                    color: white;
                    font-size: 20px;
                    border-radius: 20px;
                    padding: 10px 10px;
                    font-family: 'Impact';}
        
        QComboBox {background-color: rgba(0,0,0,100);
                    color: white;
                    font-size: 20px;
                    border-radius: 20px;
                    padding: 10px 10px;
                    font-family: 'Impact';}
                           
        QSplitter::handle {background-color: #7F18D9;}
                           
        QMessageBox {background-color: #0F0063;
                    color: white;}""")
        
        self.centrar_ventana()

        self.nombre_video="fondo.mp4"
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.ruta_video = os.path.join(self.script_dir, self.nombre_video)

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
        self.playlist.setPlaybackMode(QMediaPlaylist.CurrentItemInLoop)#posible solución a un error, andá a saber

        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        """es el motor que reproduce el video. None significa que el reproductor no tiene un widget padre.
           VideoSurface: el video se va a renderizar en una superficie personalizada, como QGraphicsVideoItem, QVideoWidget, etc.
           Es necesario para que el video se pueda mostrar en objetos gráficos."""
        self.media_player.setPlaylist(self.playlist)#le asigna la lista de reproducción.
        self.media_player.setVideoOutput(self.video_item)#le dice que muestre el video en video_item.
        self.media_player.setVolume(50)
        self.media_player.mediaStatusChanged.connect(self.repetir_video_actual)
        self.media_player.play()#comienza la reproducción.

        self.menu()

    def menu(self):
        self.overlay=QWidget(self)
        self.overlay_layout=QVBoxLayout()
        self.overlay_layout.setAlignment(Qt.AlignCenter)

        etiqueta=QLabel("Guía Futbolística con API")
        aplicar_fade_in(etiqueta,1000)

        boton_buscar_equipo=QPushButton("BUSCAR EQUIPO")
        boton_buscar_equipo.clicked.connect(self.mostrar_equipo)
        aplicar_fade_in(boton_buscar_equipo,1000)

        boton_buscar_jugador=QPushButton("BUSCAR JUGADOR")
        boton_buscar_jugador.clicked.connect(self.mostrar_jugador)
        aplicar_fade_in(boton_buscar_jugador,1000)

        boton_buscar_liga=QPushButton("LIGAS")
        boton_buscar_liga.clicked.connect(self.mostrar_liga)
        aplicar_fade_in(boton_buscar_liga,1000)

        boton_salir=QPushButton("SALIR")
        boton_salir.clicked.connect(lambda: self.close())
        aplicar_fade_in(boton_salir,1000)

        self.overlay_layout.addWidget(etiqueta)
        self.overlay_layout.addWidget(boton_buscar_equipo,alignment=Qt.AlignCenter)
        self.overlay_layout.addWidget(boton_buscar_jugador,alignment=Qt.AlignCenter)
        self.overlay_layout.addWidget(boton_buscar_liga,alignment=Qt.AlignCenter)
        self.overlay_layout.addWidget(boton_salir,alignment=Qt.AlignCenter)

        self.overlay.setLayout(self.overlay_layout)
        self.setCentralWidget(self.overlay)
        return self.overlay

    def mostrar_equipo(self):
        self.overlay=QWidget(self)
        self.overlay_layout=QVBoxLayout()
        self.overlay_layout.setAlignment(Qt.AlignCenter)

        splitter=QSplitter(Qt.Horizontal)
        self.overlay_layout.addWidget(splitter)
        self.overlay.setLayout(self.overlay_layout)

        self.overlay_layout_izquierda=QVBoxLayout()
        self.overlay_izquierda=QWidget()
        self.overlay_izquierda.setLayout(self.overlay_layout_izquierda)

        self.overlay_layout_derecha=QVBoxLayout()
        self.overlay_derecha=QWidget()
        self.overlay_derecha.setLayout(self.overlay_layout_derecha)

        etiqueta_informativa=QLabel("Ingrese el nombre completo del equipo que desea buscar:")
        etiqueta_informativa.setStyleSheet("font-size: 20px;")
        etiqueta_informativa.setWordWrap(True)

        self.lienso=QTextEdit()
        self.lienso.setReadOnly(True)
        aplicar_fade_in(self.lienso,1000)

        boton_buscar_equipo=QPushButton("BUSCAR EQUIPO")
        boton_buscar_equipo.clicked.connect(self.buscar_equipo)
        aplicar_fade_in(boton_buscar_equipo,1000)

        boton_volver_al_menu=QPushButton("VOLVER AL MENU")
        boton_volver_al_menu.clicked.connect(self.volver_al_menu)
        aplicar_fade_in(boton_volver_al_menu,1000)

        self.equipo_input=QLineEdit()
        self.equipo_input.setPlaceholderText("Ingrese el nombre completo del equipo")
        aplicar_fade_in(self.equipo_input,1000)

        self.overlay_layout_izquierda.addWidget(self.lienso)
        self.overlay_layout_derecha.addWidget(etiqueta_informativa,alignment=Qt.AlignCenter)
        self.overlay_layout_derecha.addWidget(self.equipo_input)
        self.overlay_layout_derecha.addWidget(boton_buscar_equipo,alignment=Qt.AlignCenter)
        self.overlay_layout_derecha.addWidget(boton_volver_al_menu,alignment=Qt.AlignCenter)

        splitter.addWidget(self.overlay_izquierda)
        splitter.addWidget(self.overlay_derecha)
        splitter.setSizes([450,200])

        self.setCentralWidget(splitter)
        return splitter
    
    def buscar_equipo(self):
        try:
            equipo= self.equipo_input.text()
            if equipo:
                texto=obtener_equipo(equipo)
                self.lienso.setText(texto)
            else:
                self.lienso.setText("Ingrese el nombre completo del equipo.")
        except:
            QMessageBox.warning(self,"Error","Ocurrió un fallo, intente nuevamente.")
            self.lienso.setText("Ingrese el nombre completo del equipo.")

    def centrar_ventana(self):
        pantalla = QApplication.primaryScreen().availableGeometry()
        ventana = self.frameGeometry()
        ventana.moveCenter(pantalla.center())
        self.move(ventana.topLeft())

    def volver_al_menu(self):
        self.setCentralWidget(self.menu())

    def mostrar_jugador(self):
        self.overlay=QWidget(self)
        self.overlay_layout=QVBoxLayout()
        self.overlay_layout.setAlignment(Qt.AlignCenter)

        splitter=QSplitter(Qt.Horizontal)
        self.overlay_layout.addWidget(splitter)
        self.overlay.setLayout(self.overlay_layout)

        self.overlay_layout_izquierda=QVBoxLayout()
        self.overlay_izquierda=QWidget()
        self.overlay_izquierda.setLayout(self.overlay_layout_izquierda)

        self.overlay_layout_derecha=QVBoxLayout()
        self.overlay_derecha=QWidget()
        self.overlay_derecha.setLayout(self.overlay_layout_derecha)

        etiqueta_informativa=QLabel("Ingrese el nombre completo del jugador que desea buscar:")
        etiqueta_informativa.setStyleSheet("font-size: 20px;")
        etiqueta_informativa.setWordWrap(True)

        self.lienso=QTextEdit()
        self.lienso.setReadOnly(True)
        aplicar_fade_in(self.lienso,1000)

        boton_buscar_jugador=QPushButton("BUSCAR JUGADOR")
        boton_buscar_jugador.clicked.connect(self.buscar_jugador)
        aplicar_fade_in(boton_buscar_jugador,1000)

        boton_volver_al_menu=QPushButton("VOLVER AL MENU")
        boton_volver_al_menu.clicked.connect(self.volver_al_menu)
        aplicar_fade_in(boton_volver_al_menu,1000)

        self.jugador_input=QLineEdit()
        self.jugador_input.setPlaceholderText("Ingrese el nombre completo del jugador")
        aplicar_fade_in(self.jugador_input,1000)

        self.overlay_layout_izquierda.addWidget(self.lienso)
        self.overlay_layout_derecha.addWidget(etiqueta_informativa,alignment=Qt.AlignCenter)
        self.overlay_layout_derecha.addWidget(self.jugador_input)
        self.overlay_layout_derecha.addWidget(boton_buscar_jugador,alignment=Qt.AlignCenter)
        self.overlay_layout_derecha.addWidget(boton_volver_al_menu,alignment=Qt.AlignCenter)

        splitter.addWidget(self.overlay_izquierda)
        splitter.addWidget(self.overlay_derecha)
        splitter.setSizes([450,200])

        self.setCentralWidget(splitter)
        return splitter
    
    def buscar_jugador(self):
        try:
            jugador= self.jugador_input.text()
            if jugador:
                texto=obtener_jugador(jugador)
                self.lienso.setText(texto)
            else:
                self.lienso.setText("Ingrese el nombre completo del jugador.")
        except:
            QMessageBox.warning(self,"Error","Ocurrió un fallo, intente nuevamente.")
            self.lienso.setText("Ingrese el nombre completo del jugador.")

    def mostrar_liga(self):
        self.overlay=QWidget(self)
        self.overlay_layout=QVBoxLayout()
        self.overlay_layout.setAlignment(Qt.AlignCenter)

        splitter=QSplitter(Qt.Horizontal)
        self.overlay_layout.addWidget(splitter)
        self.overlay.setLayout(self.overlay_layout)

        self.overlay_layout_izquierda=QVBoxLayout()
        self.overlay_izquierda=QWidget()
        self.overlay_izquierda.setLayout(self.overlay_layout_izquierda)

        self.overlay_layout_derecha=QVBoxLayout()
        self.overlay_derecha=QWidget()
        self.overlay_derecha.setLayout(self.overlay_layout_derecha)

        etiqueta_informativa=QLabel("Seleccione la liga que desea buscar:")
        etiqueta_informativa.setStyleSheet("font-size: 20px;")
        etiqueta_informativa.setWordWrap(True)
        aplicar_fade_in(etiqueta_informativa,1000)

        self.lienso=QTextEdit()
        self.lienso.setReadOnly(True)
        aplicar_fade_in(self.lienso,1000)

        self.combobox_de_ligas=QComboBox()
        self.llenar_combo_box_de_ligas(self.combobox_de_ligas)
        aplicar_fade_in(self.combobox_de_ligas,1000)

        boton_buscar_liga=QPushButton("BUSCAR LIGA")
        boton_buscar_liga.clicked.connect(self.buscar_liga)
        aplicar_fade_in(boton_buscar_liga,1000)

        boton_volver_al_menu=QPushButton("VOLVER AL MENU")
        boton_volver_al_menu.clicked.connect(self.volver_al_menu)
        aplicar_fade_in(boton_volver_al_menu,1000)

        self.overlay_layout_izquierda.addWidget(self.lienso)
        self.overlay_layout_derecha.addWidget(etiqueta_informativa,alignment=Qt.AlignCenter)
        self.overlay_layout_derecha.addWidget(self.combobox_de_ligas)
        self.overlay_layout_derecha.addWidget(boton_buscar_liga,alignment=Qt.AlignCenter)
        self.overlay_layout_derecha.addWidget(boton_volver_al_menu,alignment=Qt.AlignCenter)

        splitter.addWidget(self.overlay_izquierda)
        splitter.addWidget(self.overlay_derecha)
        splitter.setSizes([450,200])

        self.setCentralWidget(splitter)
        return splitter
    
    def buscar_liga(self):
        id_liga=self.combobox_de_ligas.currentData()
        datos=obtener_liga(id_liga)
        self.lienso.setText(datos)

    def llenar_combo_box_de_ligas(self,combo):
        ligas=obtener_ligas()
        for liga in ligas:
            nombre_liga=liga['strLeague']
            id_liga=liga['idLeague']
            combo.addItem(f"{nombre_liga} (ID: {id_liga})",id_liga)

    def resizeEvent(self, event):
        nuevo_tamaño = QSizeF(self.size())
        self.video_item.setSize(nuevo_tamaño)#Ajustar el tamaño del video
        self.view.setGeometry(0, 0, self.width(), self.height())#Ajustar el tamaño del visor de la escena
        self.view.setSceneRect(0, 0, self.width(), self.height())
        self.overlay.setGeometry(0, 0, self.width(), self.height())

        super().resizeEvent(event)

    def repetir_video_actual(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.media_player.setPosition(0)
            self.media_player.play()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    futbol = informefutbol()
    futbol.show()
    futbol.centrar_ventana()
    sys.exit(app.exec_())
