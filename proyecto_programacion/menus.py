import requests
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

from translate import Translator

from estilos import *
from funciones_y_extras import *
from texto_informativo import *

class Menu:
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
        boton_iniciar.clicked.connect(self._actualizar_resaltado_fechas)
        boton_iniciar.clicked.connect(self.usar_modo_calendario)
        boton_iniciar.clicked.connect(self.sonido_click.play)

        boton_informacion = QPushButton("Información")
        boton_informacion.clicked.connect(self.menu_informacion)
        boton_informacion.clicked.connect(self.sonido_click.play)

        boton_opciones = QPushButton("Opciones")
        boton_opciones.clicked.connect(self.opciones)
        boton_opciones.clicked.connect(self.sonido_click.play)
        
        boton_salir = QPushButton("Salir")
        boton_salir.clicked.connect(self.guardar_y_salir)
        boton_salir.clicked.connect(self.sonido_click.play)
        
        layout.addWidget(etiqueta,alignment=Qt.AlignCenter | Qt.AlignTop)
        layout.addWidget(etiqueta_2,alignment=Qt.AlignCenter | Qt.AlignTop)
        layout.addWidget(boton_iniciar)
        layout.addWidget(boton_informacion)
        layout.addWidget(boton_opciones)
        layout.addWidget(boton_salir)

        self.stacked_widget.setCurrentWidget(self.contenedor_menu_principal)
        
    def ingresar_tarea_modo_calendario(self):
        contenedor = QWidget()
        layout = QGridLayout()
        contenedor.setLayout(layout)
        contenedor.setStyleSheet(estilo_contenedor)

        grupo_botones = QGroupBox()
        grupo_botones.setFixedSize(150,200)
        layout_grupo_botones = QVBoxLayout()
        grupo_botones.setLayout(layout_grupo_botones)

        self.combobox_categoria_modo_calendario = QComboBox()
        self.combobox_categoria_modo_calendario.addItems(["Estudio","Trabajo","Hogar","Personal","Otro"])
        self.combobox_categoria_modo_calendario.currentTextChanged.connect(self.categoria_otro)
        self.combobox_categoria_modo_calendario.setStyleSheet("""background-color: #3B73FF;
                                                                color: white;
                                                                border: 2px solid #0C5AFA;
                                                                selection-background-color: #2C6DF5;
                                                                selection-color: white;
                                                                font-size: 18px;""")

        etiqueta_nombre = QLabel("Nombre:")
        etiqueta_nombre.setStyleSheet("background: transparent;")

        etiqueta_descripcion = QLabel("Descripción:")
        etiqueta_descripcion.setStyleSheet("background: transparent;")

        etiqueta_categoria = QLabel("Categoría:")
        etiqueta_categoria.setStyleSheet("background: transparent;")

        etiqueta_prioridad = QLabel("Prioridad:")
        etiqueta_prioridad.setStyleSheet("background: transparent;")

        etiqueta_fecha_seleccionada = QLabel("Fecha:")
        etiqueta_fecha_seleccionada.setStyleSheet("background: transparent;")

        self.etiqueta_fecha_seleccionada = QLabel("Ninguna")
        self.etiqueta_fecha_seleccionada.setStyleSheet(estilo_etiqueta_fecha)
        self.etiqueta_fecha_seleccionada.setFixedSize(100,50)

        self.nombre_tarea_modo_calendario = QLineEdit()
        self.nombre_tarea_modo_calendario.setPlaceholderText("...")

        self.descripcion_tarea_modo_calendario = QLineEdit()
        self.descripcion_tarea_modo_calendario.setPlaceholderText("...")

        self.boton_prioridad_alta_modo_calendario = QRadioButton("Alta")
        self.boton_prioridad_alta_modo_calendario.setChecked(True)
        self.boton_prioridad_alta_modo_calendario.clicked.connect(self.sonido_click.play)
        self.boton_prioridad_alta_modo_calendario.setStyleSheet("""color: white;
                                                                    background: transparent;""")

        self.boton_prioridad_media_modo_calendario = QRadioButton("Media")
        self.boton_prioridad_media_modo_calendario.clicked.connect(self.sonido_click.play)
        self.boton_prioridad_media_modo_calendario.setStyleSheet("""color: white;
                                                                    background: transparent;""")

        self.boton_prioridad_baja_modo_calendario = QRadioButton("Baja")
        self.boton_prioridad_baja_modo_calendario.clicked.connect(self.sonido_click.play)
        self.boton_prioridad_baja_modo_calendario.setStyleSheet("""color: white;
                                                                    background: transparent;""")

        layout_grupo_botones.addWidget(self.boton_prioridad_alta_modo_calendario,alignment=Qt.AlignCenter)
        layout_grupo_botones.addWidget(self.boton_prioridad_media_modo_calendario,alignment=Qt.AlignCenter)
        layout_grupo_botones.addWidget(self.boton_prioridad_baja_modo_calendario,alignment=Qt.AlignCenter)

        boton_confirmar_ingresar_tarea = QPushButton("Confirmar")
        boton_confirmar_ingresar_tarea.setFixedSize(150,55)
        boton_confirmar_ingresar_tarea.clicked.connect(self.sonido_click.play)
        boton_confirmar_ingresar_tarea.clicked.connect(self.confirmar_ingresar_tarea_modo_calendario)

        boton_cancelar_ingresar_tarea = QPushButton("Cancelar")
        boton_cancelar_ingresar_tarea.setFixedSize(150,55)
        boton_cancelar_ingresar_tarea.clicked.connect(self.sonido_click.play)
        boton_cancelar_ingresar_tarea.clicked.connect(lambda: self.layout_acciones_modo_calendario.setCurrentIndex(0))

        layout.addWidget(etiqueta_nombre,1,0,alignment=Qt.AlignLeft)
        layout.addWidget(self.nombre_tarea_modo_calendario,1,1,alignment=Qt.AlignLeft)
        layout.addWidget(etiqueta_descripcion,2,0,alignment=Qt.AlignLeft)
        layout.addWidget(self.descripcion_tarea_modo_calendario,2,1,alignment=Qt.AlignLeft)
        layout.addWidget(etiqueta_categoria,3,0,alignment=Qt.AlignLeft)
        layout.addWidget(self.combobox_categoria_modo_calendario,3,1,alignment=Qt.AlignRight)
        layout.addWidget(etiqueta_prioridad,4,0,alignment=Qt.AlignLeft)
        layout.addWidget(grupo_botones,4,1,alignment=Qt.AlignRight)
        layout.addWidget(etiqueta_fecha_seleccionada,5,0,alignment=Qt.AlignLeft)
        layout.addWidget(self.etiqueta_fecha_seleccionada,5,1,alignment=Qt.AlignRight)
        layout.addWidget(boton_confirmar_ingresar_tarea,6,0,alignment=Qt.AlignLeft)
        layout.addWidget(boton_cancelar_ingresar_tarea,6,1,alignment=Qt.AlignRight)

        return contenedor
    
    def buscar_tarea_modo_calendario(self):
        contenedor = QWidget()
        layout = QGridLayout()
        contenedor.setLayout(layout)
        contenedor.setStyleSheet(estilo_contenedor)

        self.ingresar_tarea_a_buscar_modo_calendario = QLineEdit()
        self.ingresar_tarea_a_buscar_modo_calendario.setPlaceholderText("Ingrese el nombre de la tarea aquí")

        boton_buscar_tarea = QPushButton("Buscar")
        boton_buscar_tarea.clicked.connect(self.sonido_click.play)
        boton_buscar_tarea.clicked.connect(self.encontrar_tarea)
        boton_buscar_tarea.setFixedSize(150,55)

        boton_cancelar_buscar_tarea = QPushButton("Cancelar")
        boton_cancelar_buscar_tarea.setFixedSize(150,55)
        boton_cancelar_buscar_tarea.clicked.connect(self.sonido_click.play)
        boton_cancelar_buscar_tarea.clicked.connect(lambda: self.layout_acciones_modo_calendario.setCurrentIndex(0))

        layout.addWidget(self.ingresar_tarea_a_buscar_modo_calendario,1,0,1,3)
        layout.addWidget(boton_buscar_tarea,2,0,alignment=Qt.AlignLeft)
        layout.addWidget(boton_cancelar_buscar_tarea,2,2,alignment=Qt.AlignRight)
        return contenedor
    
    def modificar_tarea_modo_calendario(self):
        contenedor = QWidget()
        layout = QGridLayout()
        contenedor.setLayout(layout)
        contenedor.setStyleSheet(estilo_contenedor)

        grupo_botones = QGroupBox()
        grupo_botones.setFixedSize(150,200)
        layout_grupo_botones = QVBoxLayout()
        grupo_botones.setLayout(layout_grupo_botones)

        self.combobox_categoria_modificada_modo_calendario = QComboBox()
        self.combobox_categoria_modificada_modo_calendario.addItems(["Estudio","Trabajo","Hogar","Personal","Otro"])
        self.combobox_categoria_modificada_modo_calendario.currentTextChanged.connect(self.categoria_otro)
        self.combobox_categoria_modificada_modo_calendario.setStyleSheet("""background-color: #3B73FF;
                                                                color: white;
                                                                border: 2px solid #0C5AFA;
                                                                selection-background-color: #2C6DF5;
                                                                selection-color: white;
                                                                font-size: 18px;""")

        etiqueta_modificacion_tarea = QLabel("Modificación de tarea ⤵")
        etiqueta_modificacion_tarea.setStyleSheet("background: transparent;")

        etiqueta_nombre = QLabel("Nombre:")
        etiqueta_nombre.setStyleSheet("background: transparent;")

        etiqueta_descripcion = QLabel("Descripción:")
        etiqueta_descripcion.setStyleSheet("background: transparent;")

        etiqueta_categoria = QLabel("Categoría:")
        etiqueta_categoria.setStyleSheet("background: transparent;")

        etiqueta_prioridad = QLabel("Prioridad:")
        etiqueta_prioridad.setStyleSheet("background: transparent;")

        etiqueta_fecha_modificada = QLabel("Fecha:")
        etiqueta_fecha_modificada.setStyleSheet("background: transparent;")

        self.etiqueta_fecha_modificada_modo_calendario = QLabel("Ninguna")
        self.etiqueta_fecha_modificada_modo_calendario.setStyleSheet(estilo_etiqueta_fecha)
        self.etiqueta_fecha_modificada_modo_calendario.setFixedSize(100,50)

        self.nombre_tarea_modificada_modo_calendario = QLineEdit()
        self.nombre_tarea_modificada_modo_calendario.setPlaceholderText("...")

        self.descripcion_tarea_modificada_modo_calendario = QLineEdit()
        self.descripcion_tarea_modificada_modo_calendario.setPlaceholderText("...")

        self.boton_prioridad_alta_modificada_modo_calendario = QRadioButton("Alta")
        self.boton_prioridad_alta_modificada_modo_calendario.setChecked(True)
        self.boton_prioridad_alta_modificada_modo_calendario.clicked.connect(self.sonido_click.play)
        self.boton_prioridad_alta_modificada_modo_calendario.setStyleSheet("""color: white;
                                                                    background: transparent;""")

        self.boton_prioridad_media_modificada_modo_calendario = QRadioButton("Media")
        self.boton_prioridad_media_modificada_modo_calendario.clicked.connect(self.sonido_click.play)
        self.boton_prioridad_media_modificada_modo_calendario.setStyleSheet("""color: white;
                                                                    background: transparent;""")

        self.boton_prioridad_baja_modificada_modo_calendario = QRadioButton("Baja")
        self.boton_prioridad_baja_modificada_modo_calendario.clicked.connect(self.sonido_click.play)
        self.boton_prioridad_baja_modificada_modo_calendario.setStyleSheet("""color: white;
                                                                    background: transparent;""")

        layout_grupo_botones.addWidget(self.boton_prioridad_alta_modificada_modo_calendario,alignment=Qt.AlignCenter)
        layout_grupo_botones.addWidget(self.boton_prioridad_media_modificada_modo_calendario,alignment=Qt.AlignCenter)
        layout_grupo_botones.addWidget(self.boton_prioridad_baja_modificada_modo_calendario,alignment=Qt.AlignCenter)

        boton_modificar_tarea = QPushButton("Modificar")
        boton_modificar_tarea.setFixedSize(150,55)
        boton_modificar_tarea.clicked.connect(self.sonido_click.play)
        boton_modificar_tarea.clicked.connect(self.modificar_tarea_seleccionada_modo_calendario)

        boton_cancelar = QPushButton("Cancelar")
        boton_cancelar.setFixedSize(150,55)
        boton_cancelar.clicked.connect(self.sonido_click.play)
        boton_cancelar.clicked.connect(lambda: self.layout_acciones_modo_calendario.setCurrentIndex(0))
        boton_cancelar.clicked.connect(self.cancelar_modificacion_tarea)

        layout.addWidget(etiqueta_modificacion_tarea,1,0,1,2,alignment=Qt.AlignCenter)
        layout.addWidget(etiqueta_nombre,2,0,alignment=Qt.AlignLeft)
        layout.addWidget(self.nombre_tarea_modificada_modo_calendario,2,1)
        layout.addWidget(etiqueta_descripcion,3,0,alignment=Qt.AlignLeft)
        layout.addWidget(self.descripcion_tarea_modificada_modo_calendario,3,1)
        layout.addWidget(etiqueta_categoria,4,0,alignment=Qt.AlignLeft)
        layout.addWidget(self.combobox_categoria_modificada_modo_calendario,4,1)
        layout.addWidget(etiqueta_prioridad,5,0,alignment=Qt.AlignLeft)
        layout.addWidget(grupo_botones,5,1,alignment=Qt.AlignRight)
        layout.addWidget(etiqueta_fecha_modificada,6,0,alignment=Qt.AlignLeft)
        layout.addWidget(self.etiqueta_fecha_modificada_modo_calendario,6,1,alignment=Qt.AlignRight)
        layout.addWidget(boton_modificar_tarea,7,0,alignment=Qt.AlignLeft)
        layout.addWidget(boton_cancelar,7,1,alignment=Qt.AlignRight)

        return contenedor
    
    def visualizar_tarea_modo_calendario(self):
        contenedor = QWidget()
        layout = QGridLayout()
        contenedor.setLayout(layout)
        contenedor.setStyleSheet(estilo_contenedor)

        self.lienso_modo_calendario = QTextEdit()
        self.lienso_modo_calendario.setPlaceholderText("Aquí se pueden ver los datos de la tarea que selecciones.")
        self.lienso_modo_calendario.setReadOnly(True)
        self.lienso_modo_calendario.setFixedHeight(485)

        boton_ver = QPushButton("Ver tarea")
        boton_ver.clicked.connect(self.sonido_click.play)
        boton_ver.clicked.connect(self.ver_datos_tarea_modo_calendario)
        boton_ver.setFixedSize(150,55)

        boton_volver = QPushButton("Volver")
        boton_volver.clicked.connect(self.sonido_click.play)
        boton_volver.clicked.connect(lambda: self.layout_acciones_modo_calendario.setCurrentIndex(0))
        boton_volver.clicked.connect(self.lienso_modo_calendario.clear)
        boton_volver.setFixedSize(150,55)

        layout.addWidget(self.lienso_modo_calendario,1,0,1,3)
        layout.addWidget(boton_ver,2,0,alignment=Qt.AlignLeft)
        layout.addWidget(boton_volver,2,2,alignment=Qt.AlignRight)

        return contenedor
    
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
        self.combobox_temas.setCurrentText(self.tema_elegido)

        self.boton_pantalla_completa = QPushButton()
        self.boton_pantalla_completa.clicked.connect(self.sonido_click.play)
        self.boton_pantalla_completa.clicked.connect(self.configurar_pantalla_completa)
        self.boton_pantalla_completa.clicked.connect(self.guardar_config_mysql)
        self.boton_pantalla_completa.setFixedSize(200,55)
        if self.pantalla_completa == 0:
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
            etiqueta_mis_tareas.setStyleSheet(titulo_mis_tareas)

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

            boton_avanzar = QPushButton("Avanzar")
            boton_avanzar.clicked.connect(self.sonido_click.play)
            boton_avanzar.clicked.connect(self.avanzar_paginas)
            boton_avanzar.setFixedSize(200,55)

            boton_retroceder = QPushButton("Retroceder")
            boton_retroceder.clicked.connect(self.sonido_click.play)
            boton_retroceder.clicked.connect(self.retroceder_paginas)
            boton_retroceder.setFixedSize(200,55)

            layout_calendario.addWidget(etiqueta_mis_tareas,1,4,1,4,alignment=Qt.AlignCenter)
            layout_calendario.addWidget(self.calendario,2,0,1,4,alignment=Qt.AlignCenter)
            layout_calendario.addWidget(self.lista_tareas,2,4,1,4,alignment=Qt.AlignRight)
            layout_calendario.addWidget(boton_avanzar,3,4,1,4,alignment=Qt.AlignRight)
            layout_calendario.addWidget(boton_retroceder,3,4,1,4,alignment=Qt.AlignLeft)
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

    def categoria_otro(self):
        input_categoria = QInputDialog()
        categoria_elegida = self.combobox_categoria_modo_calendario.currentText()
        categoria_elegida_2 = self.combobox_categoria_modificada_modo_calendario.currentText()
        if categoria_elegida=="Otro":
            self.texto=input_categoria.getText(self, "Categoria", "Ingresar categoria")
            self.texto=self.texto[0].strip() 
        elif categoria_elegida_2=="Otro":
            self.texto=input_categoria.getText(self, "Categoria", "Ingresar categoria")
            self.texto=self.texto[0].strip()

    def confirmar_ingresar_tarea_modo_calendario(self):
        nombre_tarea = self.nombre_tarea_modo_calendario.text().strip()
        descripcion_tarea = self.descripcion_tarea_modo_calendario.text().strip()
        self.categoria_elegida = self.combobox_categoria_modo_calendario.currentText()
        prioridad_asignada = ""
        fecha_tarea = self.etiqueta_fecha_seleccionada.text()
        fecha_en_qdate = self.calendario.selectedDate()
        fecha_adaptada_a_string = fecha_en_qdate.toString("yyyy-MM-dd")

        if self.boton_prioridad_alta_modo_calendario.isChecked():
            prioridad_asignada = "Alta"
        elif self.boton_prioridad_media_modo_calendario.isChecked():
            prioridad_asignada = "Media"
        elif self.boton_prioridad_baja_modo_calendario.isChecked():
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
                    if self.categoria_elegida=="Otro":
                        self.categoria_elegida = self.texto

                    id_tarea = self.insertar_tarea(nombre_tarea,
                                        descripcion_tarea,
                                        self.categoria_elegida,
                                        prioridad_asignada,
                                        fecha_adaptada_a_string)
                    
                    if id_tarea is None:
                        QMessageBox.warning(self,"Error","No se pudo guardar la tarea :(")
                        return
                                        
                    item = QListWidgetItem(tarea)
                    item.setData(Qt.UserRole, id_tarea)
                    item.setData(Qt.UserRole + 1, nombre_tarea)
                    item.setData(Qt.UserRole + 2, descripcion_tarea)
                    item.setData(Qt.UserRole + 3, self.categoria_elegida,)
                    item.setData(Qt.UserRole + 4, prioridad_asignada)
                    item.setData(Qt.UserRole + 5, fecha_en_qdate)

                    tarea_dict = {
                        "id":id_tarea,
                        "nombre":nombre_tarea,
                        "descripcion":descripcion_tarea,
                        "categoria":self.categoria_elegida,
                        "prioridad": prioridad_asignada,
                        "fecha": fecha_adaptada_a_string
                    }
                    
                    self.diccionario_tareas_modo_calendario.setdefault(fecha_adaptada_a_string, []).append(tarea_dict)

                    self.cargar_tareas()
                    
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
        fecha_str = fecha.toString("yyyy-MM-dd")
        self.lista_tareas.clear()

        tareas = self.diccionario_tareas_modo_calendario.get(fecha_str,[])
        if tareas:
            for t in tareas:
                tarea = f"• {t['nombre']}"
                item = QListWidgetItem(tarea)
                item.setData(Qt.UserRole, t["id"])
                item.setData(Qt.UserRole + 1, t["nombre"])
                item.setData(Qt.UserRole + 2, t["descripcion"])
                item.setData(Qt.UserRole + 3, t["categoria"])
                item.setData(Qt.UserRole + 4, t["prioridad"])
                item.setData(Qt.UserRole + 5, t["fecha"])
                self.lista_tareas.addItem(item)

    def seleccionar_tarea_por_nombre_y_descripcion(self,nombre,descripcion):
        for i in range(self.lista_tareas.count()):
            item = self.lista_tareas.item(i)
            if item.data(Qt.UserRole + 1) == nombre and item.data(Qt.UserRole + 2) == descripcion:
                self.lista_tareas.setCurrentItem(item)
                break

    def buscar_tareas_duplicadas(self,nombre_tarea,descripcion_tarea):
        for i in range(self.lista_tareas.count()):
            tarea_duplicada = self.lista_tareas.item(i)
            if tarea_duplicada.data(Qt.UserRole + 1) == nombre_tarea:
                QMessageBox.warning(self,"Error","Ya existe una tarea con ese nombre.")
                return True
            if tarea_duplicada.data(Qt.UserRole + 2) == descripcion_tarea:
                QMessageBox.warning(self,"Error","Ya existe una tarea con esa descripción.")
                return True
        return False
    
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
            datos = item.data(Qt.UserRole + 1)
            if datos.lower() == nombre_tarea_a_buscar.lower():
                self.lista_tareas.setCurrentItem(item)
                self.ingresar_tarea_a_buscar_modo_calendario.clear()   
                return
        QMessageBox.information(self,"Tarea no encontrada","No hay tareas con el nombre que ingresaste.")
        self.ingresar_tarea_a_buscar_modo_calendario.clear()            

    def modificar_tarea_seleccionada_modo_calendario(self):
        try:
            if self.lista_tareas.count() == 0:
                QMessageBox.warning(self,"Error","No hay tareas ingresadas, prueba ingresando algo que tengas que hacer :)")
                return
            
            tarea_seleccionada = self.lista_tareas.currentItem()      
            if not tarea_seleccionada:
                QMessageBox.warning(self,"Error","Seleccione la tarea que desea modificar.")
                return
            
            id_tarea = tarea_seleccionada.data(Qt.UserRole)
            
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

            self.modificar_tarea(id_tarea,
                                nuevo_nombre_tarea,
                                nueva_descripcion_tarea,
                                nueva_categoria,
                                nueva_prioridad,
                                nueva_fecha_en_qdate)
                
            self.cargar_tareas()

            self.nombre_tarea_modificada_modo_calendario.clear()
            self.descripcion_tarea_modificada_modo_calendario.clear()
            self.etiqueta_fecha_modificada_modo_calendario.setText("Ninguna")
            self.combobox_categoria_modificada_modo_calendario.setCurrentIndex(0)
            self.boton_prioridad_alta_modificada_modo_calendario.setChecked(True)
            self.boton_prioridad_media_modificada_modo_calendario.setChecked(False)
            self.boton_prioridad_baja_modificada_modo_calendario.setChecked(False)

            QMessageBox.information(self,"Exito","Tarea modificada correctamente")

        except Exception as e:
            QMessageBox.critical(self,"Error",f"Ha ocurrido un error inesperado: {str(e)}")

    def mostrar_datos_tarea_actual_modo_calendario(self):
        tarea_seleccionada = self.lista_tareas.currentItem()
        if not tarea_seleccionada:
            return
        
        nombre_tarea_seleccionada = tarea_seleccionada.data(Qt.UserRole + 1)
        descripcion_tarea_seleccionada = tarea_seleccionada.data(Qt.UserRole + 2)
        categoria_tarea_seleccionada = tarea_seleccionada.data(Qt.UserRole + 3)
        prioridad_tarea_seleccionada = tarea_seleccionada.data(Qt.UserRole + 4)
        fecha_en_qdate = tarea_seleccionada.data(Qt.UserRole + 5)
        if isinstance(fecha_en_qdate, QDate):
            fecha_str = fecha_en_qdate.toString("yyyy-MM-dd")
        else:
            fecha_str = str(fecha_en_qdate)

        self.nombre_tarea_modificada_modo_calendario.setText(nombre_tarea_seleccionada)
        self.descripcion_tarea_modificada_modo_calendario.setText(descripcion_tarea_seleccionada)
        self.combobox_categoria_modificada_modo_calendario.setCurrentText(categoria_tarea_seleccionada)
        self.etiqueta_fecha_modificada_modo_calendario.setText(fecha_str)
        
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
            id_tarea = tarea_seleccionada.data(Qt.UserRole)
            nombre_tarea = tarea_seleccionada.data(Qt.UserRole + 1)
            fecha_en_qdate = tarea_seleccionada.data(Qt.UserRole + 5)
            fecha_en_qdate_mod = QDate.fromString(str(fecha_en_qdate),"yyyy-MM-dd")

            self.eliminar_tarea(id_tarea)
            
            fila = self.lista_tareas.row(tarea_seleccionada)
            self.lista_tareas.takeItem(fila)

            tareas_a_eliminar = self.diccionario_tareas_modo_calendario.get(fecha_en_qdate,[])
            tareas_restantes = []

            for tarea in tareas_a_eliminar:
                if tarea["nombre"] != nombre_tarea:
                    tareas_restantes.append(tarea)

            self.diccionario_tareas_modo_calendario[fecha_en_qdate] = tareas_restantes

            self.actualizar_resaltado_fechas(fecha_en_qdate_mod)

            self.mostrar_tareas_por_fecha()

    def actualizar_resaltado_fechas(self,fecha_en_qdate):
        fecha_str = fecha_en_qdate.toString("yyyy-MM-dd")
        tareas = self.diccionario_tareas_modo_calendario.get(fecha_str,[])
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
                    formato.setBackground(QBrush(QColor("66F6FF")))
                    break

        self.calendario.setDateTextFormat(fecha_en_qdate,formato)

    def ver_datos_tarea_modo_calendario(self):
        if self.lista_tareas.count() == 0:
            QMessageBox.warning(self,"Error","No hay tareas ingresadas, prueba ingresando algo que tengas que hacer :)")
            return
        
        tarea_seleccionada = self.lista_tareas.currentItem()
        if not tarea_seleccionada:
            QMessageBox.warning(self,"Error","Seleccione una tarea para visualizar.")
            return
        
        id_tarea = tarea_seleccionada.data(Qt.UserRole)
        nombre_tarea = tarea_seleccionada.data(Qt.UserRole + 1)
        descripcion_tarea = tarea_seleccionada.data(Qt.UserRole + 2)
        categoria_tarea = tarea_seleccionada.data(Qt.UserRole + 3)
        prioridad_tarea = tarea_seleccionada.data(Qt.UserRole + 4)
        fecha_en_qdate = tarea_seleccionada.data(Qt.UserRole + 5)

        datos_tarea = f"""
<b>ID:</b>  {id_tarea}<br>
<b>Nombre:</b>  {nombre_tarea}<br>
<b>Descripción:</b> {descripcion_tarea}<br>
<b>Categoría:</b>   {categoria_tarea}<br>
<b>Prioridad:</b>   {prioridad_tarea}<br>
<b>Fecha:</b>    {fecha_en_qdate}
"""
        self.lienso_modo_calendario.setText(datos_tarea)
        print("DEBUG item:", tarea_seleccionada.text(), "ID:", tarea_seleccionada.data(Qt.UserRole))

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
        translator = Translator(to_lang="es")
        for feriado in data['response']['holidays']:
            fecha = feriado['date']['datetime']
            razon = feriado['description']
            #razon = translator.translate(razon) 
            feriados.append((fecha['year'], fecha['month'], fecha['day'], razon))

        return feriados
    
    def marcar_feriados(self):
        formato = QTextCharFormat()
        formato.setBackground(QBrush(QColor("#66F6FF")))

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