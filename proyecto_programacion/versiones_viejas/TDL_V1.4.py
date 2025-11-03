import sys
import os
import requests
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

from estilos import *
from texto_informativo import *

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
        self.tema_elejido = ""
        self.volumen = 50
        self.pantalla_completa=False
        self.centrar_ventana()
        self.setStyleSheet(estilo)

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
        self.aplicar_gradiente(self,"#ebd621","#d1be15")

    def aplicar_gradiente(self,widget,color_1,color_2):
        gradiente = QLinearGradient(0,0,0,widget.height())
        gradiente.setColorAt(0.0,QColor(color_1))
        gradiente.setColorAt(1.0,QColor(color_2))

        paleta = widget.palette()
        paleta.setBrush(widget.backgroundRole(),QBrush(gradiente))
        widget.setPalette(paleta)
        widget.setAutoFillBackground(True)
        aplicar_fade_in(widget,2000)

    def menu_principal(self):
        if self.contenedor_menu_principal.layout() is None:
            layout = QVBoxLayout()
            layout.setAlignment(Qt.AlignCenter)
            self.contenedor_menu_principal.setLayout(layout)
        else:
            layout = self.contenedor_menu_principal.layout()
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()

        etiqueta = QLabel("To Do List")
        etiqueta_2 = QLabel("Gestor de tareas")

        boton_iniciar = QPushButton("Iniciar")
        boton_iniciar.clicked.connect(self.usar_modo_calendario)
        boton_iniciar.clicked.connect(self.sonido_click.play)

        boton_informacion = QPushButton("Información")
        boton_informacion.clicked.connect(self.menu_informacion)
        boton_informacion.clicked.connect(self.sonido_click.play)

        boton_opciones = QPushButton("Opciones")
        boton_opciones.clicked.connect(self.opciones)
        boton_opciones.clicked.connect(self.sonido_click.play)
        
        boton_salir = QPushButton("Salir")
        boton_salir.clicked.connect(self.close)
        boton_salir.clicked.connect(self.sonido_click.play)
        
        layout.addWidget(etiqueta,alignment=Qt.AlignCenter | Qt.AlignTop)
        layout.addWidget(etiqueta_2,alignment=Qt.AlignCenter | Qt.AlignTop)
        layout.addWidget(boton_iniciar)
        layout.addWidget(boton_informacion)
        layout.addWidget(boton_opciones)
        layout.addWidget(boton_salir)

        self.stacked_widget.setCurrentWidget(self.contenedor_menu_principal)
    
    def menu_informacion(self):
        if self.contenedor_menu_informacion.layout() is None:
            layout = QVBoxLayout()
            self.contenedor_menu_informacion.setLayout(layout)
        else:
            layout = self.contenedor_menu_informacion.layout()
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()

        boton_volver_al_menu_principal = QPushButton("Volver")
        boton_volver_al_menu_principal.clicked.connect(self.menu_principal)
        boton_volver_al_menu_principal.clicked.connect(self.sonido_click_2.play)

        informacion = QTextEdit()
        informacion.setReadOnly(True)
        informacion.setFixedSize(900,550)
        informacion.setText(guia_informativa)

        layout.addWidget(informacion,alignment=Qt.AlignCenter)
        layout.addWidget(boton_volver_al_menu_principal,alignment=Qt.AlignLeft)

        self.stacked_widget.setCurrentWidget(self.contenedor_menu_informacion)

    def ingresar_tarea_modo_calendario(self):
        contenedor = QWidget()
        layout = QGridLayout()
        contenedor.setLayout(layout)

        grupo_botones = QGroupBox()
        layout_grupo_botones = QVBoxLayout()
        grupo_botones.setLayout(layout_grupo_botones)

        self.combobox_categoria_modo_calendario = QComboBox()
        self.combobox_categoria_modo_calendario.addItems(["Estudio","Trabajo","Hogar","Personal","Otro"])

        etiqueta_nombre = QLabel("Nombre:")

        etiqueta_descripcion = QLabel("Descripción:")

        etiqueta_categoria = QLabel("Categoría:")

        etiqueta_prioridad = QLabel("Prioridad:")

        etiqueta_fecha_seleccionada = QLabel("Fecha:")

        self.etiqueta_fecha_seleccionada = QLabel("Ninguna")
        self.etiqueta_fecha_seleccionada.setStyleSheet(estilo_etiqueta_fecha)
        self.etiqueta_fecha_seleccionada.setFixedSize(230,50)

        self.nombre_tarea_modo_calendario = QLineEdit()
        self.nombre_tarea_modo_calendario.setPlaceholderText("Ingrese el nombre de la tarea aquí")

        self.descripcion_tarea_modo_calendario = QLineEdit()
        self.descripcion_tarea_modo_calendario.setPlaceholderText("Ingrese la descripcion de la tarea aquí")

        self.boton_prioridad_alta_modo_calendario = QRadioButton("Alta")
        self.boton_prioridad_alta_modo_calendario.setChecked(True)
        self.boton_prioridad_alta_modo_calendario.clicked.connect(self.sonido_click.play)

        self.boton_prioridad_media_modo_calendario = QRadioButton("Media")
        self.boton_prioridad_media_modo_calendario.clicked.connect(self.sonido_click.play)

        self.boton_prioridad_baja_modo_calendario = QRadioButton("Baja")
        self.boton_prioridad_baja_modo_calendario.clicked.connect(self.sonido_click.play)

        layout_grupo_botones.addWidget(self.boton_prioridad_alta_modo_calendario,alignment=Qt.AlignCenter)
        layout_grupo_botones.addWidget(self.boton_prioridad_media_modo_calendario,alignment=Qt.AlignCenter)
        layout_grupo_botones.addWidget(self.boton_prioridad_baja_modo_calendario,alignment=Qt.AlignCenter)

        boton_confirmar_ingresar_tarea = QPushButton("Confirmar")
        boton_confirmar_ingresar_tarea.setFixedSize(200,55)
        boton_confirmar_ingresar_tarea.clicked.connect(self.sonido_click.play)
        boton_confirmar_ingresar_tarea.clicked.connect(self.confirmar_ingresar_tarea_modo_calendario)

        boton_cancelar_ingresar_tarea = QPushButton("Cancelar")
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
        fecha_en_qdate = self.calendario.selectedDate()
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
            tarea = f"• {nombre_tarea}"
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
                    item.setData(Qt.UserRole + 4, fecha_en_qdate)

                    tarea_dict = {
                        "nombre":nombre_tarea,
                        "descripcion":descripcion_tarea,
                        "categoria":categoria_elejida,
                        "prioridad": prioridad_asignada,
                        "fecha": fecha_en_qdate
                    }

                    if fecha_en_qdate in self.diccionario_tareas_modo_calendario:
                        self.diccionario_tareas_modo_calendario[fecha_en_qdate].append(tarea_dict)
                    else:
                        self.diccionario_tareas_modo_calendario[fecha_en_qdate] = [tarea_dict]
                    
                    formato = self.resaltado_segun_prioridad(prioridad_asignada)
                    self.calendario.setDateTextFormat(fecha_en_qdate,formato)
                    self.lista_tareas.addItem(item)
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

    def mostrar_tareas_por_fecha(self):
        fecha = self.calendario.selectedDate()
        self.lista_tareas.clear()

        tareas = self.diccionario_tareas_modo_calendario.get(fecha,[])
        if tareas:
            for t in tareas:
                tarea = f"• {t['nombre']}"
                item = QListWidgetItem(tarea)
                item.setData(Qt.UserRole, t["nombre"])
                item.setData(Qt.UserRole + 1, t["descripcion"])
                item.setData(Qt.UserRole + 2, t["categoria"])
                item.setData(Qt.UserRole + 3, t["prioridad"])
                item.setData(Qt.UserRole + 4, t["fecha"])
                self.lista_tareas.addItem(item)

    def seleccionar_tarea_por_nombre_y_descripcion(self,nombre,descripcion):
        for i in range(self.lista_tareas.count()):
            item = self.lista_tareas.item(i)
            if item.data(Qt.UserRole) == nombre and item.data(Qt.UserRole + 1 ) == descripcion:
                self.lista_tareas.setCurrentItem(item)
                break

    def resaltado_segun_prioridad(self,prioridad):
        formato = QTextCharFormat()
        if prioridad == "Alta":
            formato.setBackground(QColor("#FF5C5C"))
        if prioridad == "Media":
            formato.setBackground(QColor("#FFF45C"))
        if prioridad == "Baja":
            formato.setBackground(QColor("#7AFF5C"))
        return formato

    def buscar_tareas_duplicadas(self,nombre_tarea,descripcion_tarea):
        for i in range(self.lista_tareas.count()):
            tarea_duplicada = self.lista_tareas.item(i)
            if tarea_duplicada.data(Qt.UserRole) == nombre_tarea:
                QMessageBox.warning(self,"Error","Ya existe una tarea con ese nombre.")
                return True
            if tarea_duplicada.data(Qt.UserRole + 1) == descripcion_tarea:
                QMessageBox.warning(self,"Error","Ya existe una tarea con esa descripción.")
                return True
        return False
    
    def buscar_tarea_modo_calendario(self):
        contenedor = QWidget()
        layout = QVBoxLayout()
        contenedor.setLayout(layout)

        etiqueta_buscar_tarea = QLabel("Ingrese el nombre de la tarea a buscar aquí ⤵")
        etiqueta_buscar_tarea.setWordWrap(True)

        self.ingresar_tarea_a_buscar_modo_calendario = QLineEdit()
        self.ingresar_tarea_a_buscar_modo_calendario.setPlaceholderText("Ingrese el nombre de la tarea aquí")

        boton_buscar_tarea = QPushButton("Buscar")
        boton_buscar_tarea.clicked.connect(self.sonido_click.play)
        boton_buscar_tarea.clicked.connect(self.encontrar_tarea)
        boton_buscar_tarea.setFixedSize(200,55)

        boton_cancelar_buscar_tarea = QPushButton("Cancelar")
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
        if self.lista_tareas.count() == 0:
            QMessageBox.warning(self,"Error","No hay tareas ingresadas, prueba ingresando algo que tengas que hacer :)")
            return
        nombre_tarea_a_buscar = self.ingresar_tarea_a_buscar_modo_calendario.text().strip()
        if not nombre_tarea_a_buscar:
            QMessageBox.warning(self,"Error","El campo de búsqueda está vacío.")
            return 
        for i in range(self.lista_tareas.count()):
            item = self.lista_tareas.item(i)
            datos = item.data(Qt.UserRole)
            if datos.lower() == nombre_tarea_a_buscar.lower():
                self.lista_tareas.setCurrentItem(item)
                self.ingresar_tarea_a_buscar_modo_calendario.clear()   
                return
        QMessageBox.information(self,"Tarea no encontrada","No hay tareas con el nombre que ingresaste.")
        self.ingresar_tarea_a_buscar_modo_calendario.clear()            
    
    def modificar_tarea_modo_calendario(self):
        contenedor = QWidget()
        layout = QGridLayout()
        contenedor.setLayout(layout)

        grupo_botones = QGroupBox()
        layout_grupo_botones = QVBoxLayout()
        grupo_botones.setLayout(layout_grupo_botones)

        self.combobox_categoria_modificada_modo_calendario = QComboBox()
        self.combobox_categoria_modificada_modo_calendario.addItems(["Estudio","Trabajo","Hogar","Personal","Otro"])

        etiqueta_modificacion_tarea = QLabel("Modificación de tarea ⤵")

        etiqueta_nombre = QLabel("Nombre:")

        etiqueta_descripcion = QLabel("Descripción:")

        etiqueta_categoria = QLabel("Categoría:")

        etiqueta_prioridad = QLabel("Prioridad:")

        etiqueta_fecha_modificada = QLabel("Fecha:")

        self.etiqueta_fecha_modificada_modo_calendario = QLabel("Ninguna")
        self.etiqueta_fecha_modificada_modo_calendario.setStyleSheet(estilo_etiqueta_fecha)
        self.etiqueta_fecha_modificada_modo_calendario.setFixedSize(230,50)

        self.nombre_tarea_modificada_modo_calendario = QLineEdit()
        self.nombre_tarea_modificada_modo_calendario.setPlaceholderText("Ingrese el nuevo nombre aquí")

        self.descripcion_tarea_modificada_modo_calendario = QLineEdit()
        self.descripcion_tarea_modificada_modo_calendario.setPlaceholderText("Ingrese la nueva descripcion aquí")

        self.boton_prioridad_alta_modificada_modo_calendario = QRadioButton("Alta")
        self.boton_prioridad_alta_modificada_modo_calendario.setChecked(True)
        self.boton_prioridad_alta_modificada_modo_calendario.clicked.connect(self.sonido_click.play)

        self.boton_prioridad_media_modificada_modo_calendario = QRadioButton("Media")
        self.boton_prioridad_media_modificada_modo_calendario.clicked.connect(self.sonido_click.play)

        self.boton_prioridad_baja_modificada_modo_calendario = QRadioButton("Baja")
        self.boton_prioridad_baja_modificada_modo_calendario.clicked.connect(self.sonido_click.play)

        layout_grupo_botones.addWidget(self.boton_prioridad_alta_modificada_modo_calendario,alignment=Qt.AlignCenter)
        layout_grupo_botones.addWidget(self.boton_prioridad_media_modificada_modo_calendario,alignment=Qt.AlignCenter)
        layout_grupo_botones.addWidget(self.boton_prioridad_baja_modificada_modo_calendario,alignment=Qt.AlignCenter)

        boton_modificar_tarea = QPushButton("Modificar")
        boton_modificar_tarea.setFixedSize(200,55)
        boton_modificar_tarea.clicked.connect(self.sonido_click.play)
        boton_modificar_tarea.clicked.connect(self.modificar_tarea_seleccionada_modo_calendario)

        boton_cancelar = QPushButton("Cancelar")
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

    def modificar_tarea_seleccionada_modo_calendario(self):
        try:
            if self.lista_tareas.count() == 0:
                QMessageBox.warning(self,"Error","No hay tareas ingresadas, prueba ingresando algo que tengas que hacer :)")
                return
            
            tarea_seleccionada = self.lista_tareas.currentItem()      
            if not tarea_seleccionada:
                QMessageBox.warning(self,"Error","Seleccione la tarea que desea modificar.")
                return
            
            nombre_tarea_original = tarea_seleccionada.data(Qt.UserRole)
            descripcion_tarea_original = tarea_seleccionada.data(Qt.UserRole + 1)
            fecha_original_en_qdate = tarea_seleccionada.data(Qt.UserRole + 4)
            
            nuevo_nombre_tarea = self.nombre_tarea_modificada_modo_calendario.text().strip()
            nueva_descripcion_tarea = self.descripcion_tarea_modificada_modo_calendario.text()
            nueva_categoria = self.combobox_categoria_modificada_modo_calendario.currentText()
            nueva_fecha_en_qdate = self.calendario.selectedDate()
            nueva_prioridad = ''

            if self.boton_prioridad_alta_modificada_modo_calendario.isChecked():
                nueva_prioridad = "Alta"
            elif self.boton_prioridad_media_modificada_modo_calendario.isChecked():
                nueva_prioridad = "Media"
            else:
                nueva_prioridad = "Baja"

            if not nuevo_nombre_tarea or not nueva_descripcion_tarea:
                QMessageBox.warning(self,"Error","Los campos no pueden estar vacíos.")
                return

            tarea_seleccionada.setText(f"• {nuevo_nombre_tarea}")
            tarea_seleccionada.setData(Qt.UserRole, nuevo_nombre_tarea)
            tarea_seleccionada.setData(Qt.UserRole + 1,nueva_descripcion_tarea)
            tarea_seleccionada.setData(Qt.UserRole + 2, nueva_categoria)
            tarea_seleccionada.setData(Qt.UserRole + 3, nueva_prioridad)
            tarea_seleccionada.setData(Qt.UserRole + 4, nueva_fecha_en_qdate)

            if nueva_fecha_en_qdate != fecha_original_en_qdate:
                tareas_originales = self.diccionario_tareas_modo_calendario.get(fecha_original_en_qdate,[])
                for i in range(len(tareas_originales)):
                    tarea = tareas_originales[i]
                    if tarea["nombre"] == nombre_tarea_original and tarea["descripcion"] == descripcion_tarea_original:
                        tareas_originales.pop(i)
                        break

                nueva_tarea = {
                    "nombre":nuevo_nombre_tarea,
                    "descripcion":nueva_descripcion_tarea,
                    "categoria":nueva_categoria,
                    "prioridad":nueva_prioridad,
                    "fecha":nueva_fecha_en_qdate
                }

                if nueva_fecha_en_qdate in self.diccionario_tareas_modo_calendario:
                    self.diccionario_tareas_modo_calendario[nueva_fecha_en_qdate].append(nueva_tarea)
                else:
                    self.diccionario_tareas_modo_calendario[nueva_fecha_en_qdate] = [nueva_tarea]

                self.actualizar_resaltado_fechas(fecha_original_en_qdate)
                self.actualizar_resaltado_fechas(nueva_fecha_en_qdate)

            else:

                tareas_actuales = self.diccionario_tareas_modo_calendario.get(fecha_original_en_qdate,[])
                for tarea in tareas_actuales:
                    if tarea["nombre"] == nombre_tarea_original and tarea["descripcion"] == descripcion_tarea_original:
                        tarea["nombre"] = nuevo_nombre_tarea
                        tarea["descripcion"] = nueva_descripcion_tarea
                        tarea["categoria"] = nueva_categoria
                        tarea["prioridad"] = nueva_prioridad
                        tarea["fecha"] = nueva_fecha_en_qdate
                        break

                self.actualizar_resaltado_fechas(fecha_original_en_qdate)

            self.nombre_tarea_modificada_modo_calendario.clear()
            self.descripcion_tarea_modificada_modo_calendario.clear()
            self.etiqueta_fecha_modificada_modo_calendario.setText("Ninguna")
            self.combobox_categoria_modificada_modo_calendario.setCurrentIndex(0)
            self.boton_prioridad_alta_modificada_modo_calendario.setChecked(True)
            self.boton_prioridad_media_modificada_modo_calendario.setChecked(False)
            self.boton_prioridad_baja_modificada_modo_calendario.setChecked(False)

            if nueva_fecha_en_qdate != fecha_original_en_qdate:
                self.calendario.setSelectedDate(nueva_fecha_en_qdate)

            self.mostrar_tareas_por_fecha()
            self.seleccionar_tarea_por_nombre_y_descripcion(nuevo_nombre_tarea,nueva_descripcion_tarea)

            QMessageBox.information(self,"Exito","Tarea modificada correctamente")

        except Exception as e:
            QMessageBox.critical(self,"Error",f"Ha ocurrido un error inesperado: {str(e)}")

    def mostrar_datos_tarea_actual_modo_calendario(self):
        tarea_seleccionada = self.lista_tareas.currentItem()
        if not tarea_seleccionada:
            return
        
        nombre_tarea_seleccionada = tarea_seleccionada.data(Qt.UserRole)
        descripcion_tarea_seleccionada = tarea_seleccionada.data(Qt.UserRole + 1)
        categoria_tarea_seleccionada = tarea_seleccionada.data(Qt.UserRole + 2)
        prioridad_tarea_seleccionada = tarea_seleccionada.data(Qt.UserRole + 3)
        fecha_en_qdate = tarea_seleccionada.data(Qt.UserRole + 4)

        self.nombre_tarea_modificada_modo_calendario.setText(nombre_tarea_seleccionada)
        self.descripcion_tarea_modificada_modo_calendario.setText(descripcion_tarea_seleccionada)
        self.combobox_categoria_modificada_modo_calendario.setCurrentText(categoria_tarea_seleccionada)
        self.etiqueta_fecha_modificada_modo_calendario.setText(fecha_en_qdate.toString("dd-MM-yyyy"))
        
        if prioridad_tarea_seleccionada == "Alta":
            self.boton_prioridad_alta_modificada_modo_calendario.setChecked(True)
        elif prioridad_tarea_seleccionada == "Media":
            self.boton_prioridad_media_modificada_modo_calendario.setChecked(True)
        else:
            self.boton_prioridad_baja_modificada_modo_calendario.setChecked(True)

    def cancelar_modificacion_tarea(self):
        self.nombre_tarea_modificada_modo_calendario.clear()
        self.descripcion_tarea_modificada_modo_calendario.clear()
        self.etiqueta_fecha_modificada_modo_calendario.setText("Ninguna")
        self.combobox_categoria_modificada_modo_calendario.setCurrentIndex(0)
        self.boton_prioridad_alta_modificada_modo_calendario.setChecked(True)
        self.boton_prioridad_media_modificada_modo_calendario.setChecked(False)
        self.boton_prioridad_baja_modificada_modo_calendario.setChecked(False)

    def eliminar_tarea_modo_calendario(self):
        if self.lista_tareas.count() == 0:
            QMessageBox.warning(self,"Error","No hay tareas ingresadas, prueba ingresando algo que tengas que hacer :)")
            return
        
        tarea_seleccionada = self.lista_tareas.currentItem()
        if not tarea_seleccionada:
            QMessageBox.warning(self,"Error","Seleccione una tarea para eliminarla.")
            return
        
        respuesta = QMessageBox.question(self,"Eliminar tarea","¿Desea eliminar la tarea seleccionada?",QMessageBox.Yes | QMessageBox.No)
        
        if respuesta == QMessageBox.Yes:
            nombre_tarea = tarea_seleccionada.data(Qt.UserRole)
            fecha_en_qdate = tarea_seleccionada.data(Qt.UserRole + 4)
            
            fila = self.lista_tareas.row(tarea_seleccionada)
            self.lista_tareas.takeItem(fila)

            tareas_a_eliminar = self.diccionario_tareas_modo_calendario.get(fecha_en_qdate,[])
            tareas_restantes = []

            for tarea in tareas_a_eliminar:
                if tarea["nombre"] != nombre_tarea:
                    tareas_restantes.append(tarea)

            self.diccionario_tareas_modo_calendario[fecha_en_qdate] = tareas_restantes

            self.actualizar_resaltado_fechas(fecha_en_qdate)

            self.mostrar_tareas_por_fecha()

    def actualizar_resaltado_fechas(self,fecha_en_qdate):
        tareas = self.diccionario_tareas_modo_calendario.get(fecha_en_qdate,[])
        prioridades = []
        for tarea in tareas:
            prioridades.append(tarea["prioridad"])

        formato = QTextCharFormat()

        if "Alta" in prioridades:
            formato = self.resaltado_segun_prioridad("Alta")
        elif "Media" in prioridades:
            formato = self.resaltado_segun_prioridad("Media")
        elif "Baja" in prioridades:
            formato = self.resaltado_segun_prioridad("Baja")
        else:
            for year, month, day, _ in self.feriados:
                if fecha_en_qdate == QDate(year,month,day):
                    formato.setBackground(QBrush(QColor("#66F6FF")))
                    break

        self.calendario.setDateTextFormat(fecha_en_qdate,formato)
    
    def visualizar_tarea_modo_calendario(self):
        contenedor = QWidget()
        layout = QVBoxLayout()
        contenedor.setLayout(layout)

        self.lienso_modo_calendario = QTextEdit()
        self.lienso_modo_calendario.setPlaceholderText("Aquí se pueden ver los datos de la tarea que selecciones.")
        self.lienso_modo_calendario.setReadOnly(True)

        boton_ver = QPushButton("Ver tarea")
        boton_ver.clicked.connect(self.sonido_click.play)
        boton_ver.clicked.connect(self.ver_datos_tarea_modo_calendario)
        boton_ver.setFixedSize(200,55)

        boton_volver = QPushButton("Volver")
        boton_volver.clicked.connect(self.sonido_click.play)
        boton_volver.clicked.connect(lambda: self.layout_acciones_modo_calendario.setCurrentIndex(0))
        boton_volver.clicked.connect(self.lienso_modo_calendario.clear)
        boton_volver.setFixedSize(200,55)

        layout.addWidget(self.lienso_modo_calendario)
        layout.addWidget(boton_ver,alignment=Qt.AlignCenter)
        layout.addWidget(boton_volver,alignment=Qt.AlignCenter)

        return contenedor

    def ver_datos_tarea_modo_calendario(self):
        if self.lista_tareas.count() == 0:
            QMessageBox.warning(self,"Error","No hay tareas ingresadas, prueba ingresando algo que tengas que hacer :)")
            return
        
        tarea_seleccionada = self.lista_tareas.currentItem()
        if not tarea_seleccionada:
            QMessageBox.warning(self,"Error","Seleccione una tarea para visualizar.")
            return
        
        nombre_tarea = tarea_seleccionada.data(Qt.UserRole)
        descripcion_tarea = tarea_seleccionada.data(Qt.UserRole + 1)
        categoria_tarea = tarea_seleccionada.data(Qt.UserRole + 2)
        prioridad_tarea = tarea_seleccionada.data(Qt.UserRole + 3)
        fecha_en_qdate = tarea_seleccionada.data(Qt.UserRole + 4)
        fecha_tarea = fecha_en_qdate.toString("dd-MM-yyyy")

        datos_tarea = f"""
<b>Nombre:</b>  {nombre_tarea}<br>
<b>Descripción:</b> {descripcion_tarea}<br>
<b>Categoría:</b>   {categoria_tarea}<br>
<b>Prioridad:</b>   {prioridad_tarea}<br>
<b>Fecha:</b>    {fecha_tarea}
"""
        self.lienso_modo_calendario.setText(datos_tarea)
    
    def usar_modo_calendario(self):
        if self.contenedor_modo_calendario.layout() is None:
            layout = QHBoxLayout()
            self.modo_elegido = "Calendario"
            if self.modo_elegido == "Calendario":
                self.lista_tareas.setFixedSize(465,400)
                self.lista_tareas.itemSelectionChanged.connect(self.mostrar_datos_tarea_actual_modo_calendario)
                self.lista_tareas.currentItemChanged.connect(self.mostrar_datos_tarea_actual_modo_calendario)
            self.contenedor_modo_calendario.setLayout(layout)

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
            self.calendario.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
            self.calendario.setMinimumDate(QDate(anio_actual,1,1))
            self.calendario.setMaximumDate(QDate(anio_actual,12,31))

            self.combobox_meses = QComboBox()
            self.meses=[]
            for mes in meses_diccionario:
                self.meses.append(mes)
            mes_elegido = self.meses[mes_actual - 1]
            print(mes_elegido)
            self.combobox_meses.addItems(self.meses)
            self.combobox_meses.setCurrentText(mes_elegido)
            self.combobox_meses.currentTextChanged.connect(self.actualizar_fechas)

            self.label = QLabel()
            self.label.setStyleSheet("font-size: 16px;")
            self.label.setFixedSize(400,100)
            self.label.setWordWrap(True)

            etiqueta_acciones = QLabel("Acciones")

            etiqueta_año_complemento_2 = QLabel(f"{anio_actual}")
            etiqueta_año_complemento_2.setStyleSheet(estilo_etiqueta_año)

            etiqueta_mis_tareas = QLabel("Mis tareas ⤵")

            self.boton_ingresar_tarea_modo_calendario = QPushButton("Ingresar")
            self.boton_ingresar_tarea_modo_calendario.clicked.connect(lambda: self.layout_acciones_modo_calendario.setCurrentIndex(1))
            self.boton_ingresar_tarea_modo_calendario.clicked.connect(self.sonido_click.play)
            self.boton_ingresar_tarea_modo_calendario.setFixedSize(200,55)

            self.boton_buscar_tarea_modo_calendario = QPushButton("Buscar")
            self.boton_buscar_tarea_modo_calendario.clicked.connect(lambda: self.layout_acciones_modo_calendario.setCurrentIndex(2))
            self.boton_buscar_tarea_modo_calendario.clicked.connect(self.sonido_click.play)
            self.boton_buscar_tarea_modo_calendario.setFixedSize(200,55)

            self.boton_modificar_tarea_modo_calendario = QPushButton("Modificar")
            self.boton_modificar_tarea_modo_calendario.clicked.connect(lambda: self.layout_acciones_modo_calendario.setCurrentIndex(3))
            self.boton_modificar_tarea_modo_calendario.clicked.connect(self.sonido_click.play)
            self.boton_modificar_tarea_modo_calendario.setFixedSize(200,55)

            self.boton_ver_tarea_modo_calendario = QPushButton("Visualizar")
            self.boton_ver_tarea_modo_calendario.clicked.connect(lambda: self.layout_acciones_modo_calendario.setCurrentIndex(4))
            self.boton_ver_tarea_modo_calendario.clicked.connect(self.sonido_click.play)
            self.boton_ver_tarea_modo_calendario.setFixedSize(200,55)

            self.boton_eliminar_tarea_modo_calendario = QPushButton("Eliminar")
            self.boton_eliminar_tarea_modo_calendario.clicked.connect(self.eliminar_tarea_modo_calendario)
            self.boton_eliminar_tarea_modo_calendario.clicked.connect(self.sonido_click.play)
            self.boton_eliminar_tarea_modo_calendario.setFixedSize(200,55)

            boton_volver_al_menu_principal = QPushButton("Volver")
            boton_volver_al_menu_principal.clicked.connect(self.menu_principal)
            boton_volver_al_menu_principal.clicked.connect(self.sonido_click_2.play)

            boton_avanzar_mes = QPushButton(">>>")
            boton_avanzar_mes.clicked.connect(self.sonido_click.play)
            boton_avanzar_mes.setFixedSize(200,55)

            boton_retroceder_mes = QPushButton("<<<")
            boton_retroceder_mes.clicked.connect(self.sonido_click.play)
            boton_retroceder_mes.setFixedSize(200,55)

            layout_calendario.addWidget(etiqueta_mis_tareas,1,4,1,4,alignment=Qt.AlignCenter)
            layout_calendario.addWidget(self.calendario,2,0,1,4,alignment=Qt.AlignCenter)
            layout_calendario.addWidget(self.lista_tareas,2,4,1,4,alignment=Qt.AlignRight)
            layout_calendario.addWidget(self.label,3,0,1,4,alignment=Qt.AlignCenter)

            layout_botones.addWidget(etiqueta_acciones,alignment=Qt.AlignTop | Qt.AlignCenter)
            layout_botones.addWidget(self.boton_ingresar_tarea_modo_calendario,alignment=Qt.AlignCenter)
            layout_botones.addWidget(self.boton_buscar_tarea_modo_calendario,alignment=Qt.AlignCenter)
            layout_botones.addWidget(self.boton_modificar_tarea_modo_calendario,alignment=Qt.AlignCenter)
            layout_botones.addWidget(self.boton_ver_tarea_modo_calendario,alignment=Qt.AlignCenter)
            layout_botones.addWidget(self.boton_eliminar_tarea_modo_calendario,alignment=Qt.AlignCenter)
            layout_botones.addWidget(boton_volver_al_menu_principal,alignment=Qt.AlignRight)

            self.feriados = self.obtener_feriados()
            self.marcar_feriados()
            self.calendario.clicked.connect(self.mostrar_fecha)
            self.calendario.clicked.connect(self.mostrar_fecha_seleccionada)
            self.calendario.selectionChanged.connect(self.mostrar_tareas_por_fecha)

            layout.addWidget(contenedor_calendario)
            layout.addWidget(self.contenedor_acciones_modo_calendario)

            self.layout_acciones_modo_calendario.addWidget(contenedor_botones)
            self.layout_acciones_modo_calendario.addWidget(self.ingreso_de_tarea_modo_calendario)
            self.layout_acciones_modo_calendario.addWidget(self.busqueda_de_tarea_modo_calendario)
            self.layout_acciones_modo_calendario.addWidget(self.modificacion_de_tarea_modo_calendario)
            self.layout_acciones_modo_calendario.addWidget(self.visualizacion_de_tarea_modo_calendario)

        self.layout_acciones_modo_calendario.setCurrentIndex(0)
        self.stacked_widget.setCurrentWidget(self.contenedor_modo_calendario)

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
        formato.setBackground(QBrush(QColor("#66F6FF"))) #Color de los dias marcados como feriado en el calendario

        for year, month, day, _ in self.feriados:
            fecha = QDate(year, month, day)
            self.calendario.setDateTextFormat(fecha, formato)

    def mostrar_fecha(self, date):
        festividad = ""

        for year, month, day, razon in self.feriados:
            if year == date.year() and month == date.month() and day == date.day():
                festividad = f"Festividad: {razon}"
                break

        formato_fecha_configurada = date.toString("dd-MM-yyyy")
        self.label.setText(f"Fecha seleccionada: {formato_fecha_configurada}\n{festividad}")

    def mostrar_fecha_seleccionada(self,date):
        formato_fecha_configurada = date.toString("dd-MM-yyyy")
        self.etiqueta_fecha_seleccionada.setText(formato_fecha_configurada)
        self.etiqueta_fecha_modificada_modo_calendario.setText(formato_fecha_configurada)

    def actualizar_fechas(self):
        mes_actual=meses_diccionario[self.combobox_meses.currentText()]
        self.calendario.setCurrentPage(anio_actual,mes_actual)
    
    def opciones(self):
        if self.contenedor_opciones.layout() is None:
            layout = QVBoxLayout()
            self.contenedor_opciones.setLayout(layout)
        else:
            layout = self.contenedor_opciones.layout()
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()

        contenedor_opciones = QWidget()

        layout_opciones = QGridLayout()

        contenedor_opciones.setLayout(layout_opciones)

        etiqueta_opciones = QLabel("Opciones")

        etiqueta_tema = QLabel("Tema:")

        etiqueta_pantalla_completa = QLabel("Pantalla Completa:")

        self.slider_volumen = QSlider(Qt.Horizontal)
        self.slider_volumen.setRange(0, 100)
        self.slider_volumen.setValue(self.volumen)
        self.slider_volumen.setFixedWidth(300)

        self.etiqueta_slider_volumen = QLabel(f"Volumen: {self.volumen}%")
        self.slider_volumen.valueChanged.connect(self.actualizar_volumen)

        self.combobox_temas = QComboBox()
        self.combobox_temas.addItems(['Claro','Oscuro'])
        self.combobox_temas.setFixedSize(200,50)
        self.combobox_temas.setCurrentText(self.tema_elejido)

        self.boton_pantalla_completa = QPushButton()
        self.boton_pantalla_completa.clicked.connect(self.sonido_click.play)
        self.boton_pantalla_completa.clicked.connect(self.configurar_pantalla_completa)
        self.boton_pantalla_completa.setFixedSize(200,55)
        if self.pantalla_completa == False:
            self.boton_pantalla_completa.setText("NO")
        else:
            self.boton_pantalla_completa.setText("SI")

        boton_volver_al_menu_principal = QPushButton("Volver")
        boton_volver_al_menu_principal.clicked.connect(self.menu_principal)
        boton_volver_al_menu_principal.clicked.connect(self.sonido_click_2.play)

        boton_aplicar_cambios = QPushButton("Aplicar Cambios")
        boton_aplicar_cambios.clicked.connect(self.aplicar_cambios)
        boton_aplicar_cambios.clicked.connect(self.sonido_click_3.play)

        layout_opciones.addWidget(etiqueta_opciones,1,0,1,2,alignment=Qt.AlignTop | Qt.AlignCenter)
        layout_opciones.addWidget(etiqueta_tema,2,0,alignment=Qt.AlignTop | Qt.AlignCenter)
        layout_opciones.addWidget(self.combobox_temas,2,1,alignment=Qt.AlignTop | Qt.AlignCenter)
        layout_opciones.addWidget(etiqueta_pantalla_completa,4,0,alignment=Qt.AlignTop | Qt.AlignCenter)
        layout_opciones.addWidget(self.boton_pantalla_completa,4,1,alignment=Qt.AlignTop | Qt.AlignCenter)
        layout_opciones.addWidget(self.etiqueta_slider_volumen,5,0,alignment=Qt.AlignTop | Qt.AlignCenter)
        layout_opciones.addWidget(self.slider_volumen,5,1,alignment=Qt.AlignTop | Qt.AlignCenter)
        layout_opciones.addWidget(boton_volver_al_menu_principal,6,0,alignment=Qt.AlignLeft)
        layout_opciones.addWidget(boton_aplicar_cambios,6,0,1,2,alignment=Qt.AlignCenter)
        
        layout.addWidget(contenedor_opciones)

        self.stacked_widget.setCurrentWidget(self.contenedor_opciones)
    
    def aplicar_cambios(self):
        self.tema_elejido = self.combobox_temas.currentText()
        if self.tema_elejido == "Oscuro":
            self.setStyleSheet(estilo_tema_oscuro)
            self.aplicar_gradiente(self,"#000000","#505404")
        else:
            self.setStyleSheet(estilo)
            self.aplicar_gradiente(self,"#ebd621","#d1be15")

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gestor_de_tareas = Tdl()
    gestor_de_tareas.show()
    sys.exit(app.exec_())
