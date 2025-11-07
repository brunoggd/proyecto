import mysql.connector
from mysql.connector import Error

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *

class Db:
    def conectar_mysql(self):
        try:
            self.conexion=mysql.connector.connect(
                host='localhost',
                user='root',
                password='root',
                database='base_de_datos_proyecto'
            )

            if self.conexion.is_connected():
                print("Conexión establecida")

            return self.conexion

        except Error as e:
            rdo=f"Error al conectar a MySQL: {e}"
            print(rdo)

    def crear_tabla_tareas(self):
        if not self.conexion:
            print("No hay nada conectado")
            return
        try:
            consulta = f"""CREATE TABLE IF NOT EXISTS tareas(
                            id_tarea INT PRIMARY KEY AUTO_INCREMENT,
                            nombre VARCHAR(50) NOT NULL,
                            descripcion VARCHAR(200) NOT NULL,
                            categoria VARCHAR(100) NOT NULL,
                            prioridad ENUM('Alta','Media','Baja'),
                            fecha DATE NOT NULL)"""
            
            cursor = self.conexion.cursor()
            cursor.execute(consulta)
            cursor.close()

            print("tabla tareas creada bien")

        except Error as e:
            rdo=f"Error al crear la tabla: {e}"
            print(rdo)

    def crear_tabla_config(self):
        if not self.conexion:
            print("No hay nada conectado")
            return
        try:
            consulta = f"""CREATE TABLE IF NOT EXISTS config(
                            id_config INT PRIMARY KEY DEFAULT 1,
                            tema_elegido VARCHAR(6) NOT NULL,
                            pantalla_completa INT NOT NULL,
                            volumen INT NOT NULL);
                            """
            consulta2 = """INSERT IGNORE INTO config (id_config,tema_elegido,pantalla_completa,volumen) VALUES (1, "Claro", 0, 60);"""


            cursor = self.conexion.cursor()
            cursor.execute(consulta)
            cursor.execute(consulta2)
            self.conexion.commit()
            cursor.close()
            
            print("tabla config piola")
            
        except Error as e:
            rdo=f"Error al crear la tabla config: {e}"
            print(rdo)

    def guardar_config_mysql(self):
        if not self.conexion:
            print("No hay nada conectado")
            return
        try:
            consulta = f"""UPDATE config
                        SET tema_elegido = %s,
                            pantalla_completa = %s,
                            volumen = %s
                        WHERE id_config = 1"""
            
            config_actualizada = (self.tema_elegido,self.pantalla_completa,self.volumen)

            cursor = self.conexion.cursor()
            cursor.execute(consulta,config_actualizada)
            self.conexion.commit()
            cursor.close()

            print("config updateada")
            self.cargar_config() 

        except Error as e:
            rdo=f"Error al actualizar la configuración: {e}"
            print(rdo)

    def cargar_config(self):
        if not self.conexion:
            print("No hay nada conectado")
            return
        try:
            cursor = self.conexion.cursor()
            consulta=f"""SELECT * FROM config;"""

            cursor.execute(consulta)

            fila=cursor.fetchone()
            cursor.close()
            
            self.tema_elegido = fila[1]
            self.pantalla_completa = fila[2]
            self.volumen = fila[3]

            print(f"Tema pantalla: {self.tema_elegido}")
            print(f"Pantalla completa: {self.pantalla_completa}")
            print(f"Volumen: {self.volumen}")
            self.cargar_pantalla_completa()
            self._configurar_tema()

        except Error as e:
            rdo=f"Error al cargar configuracion: {e}"
            print(rdo)

    def insertar_tarea(self, nombre, descripcion, categoria, prioridad, fecha):
        if not self.conexion:
            print("No hay nada conectado")
            return
        try:
            cursor = self.conexion.cursor()
            consulta = "INSERT INTO tareas(nombre,descripcion,categoria,prioridad,fecha) VALUES (%s,%s,%s,%s,%s)"
            campos = (nombre,descripcion,categoria,prioridad,fecha)
            cursor.execute(consulta,campos)
            id_tarea = cursor.lastrowid
            
            self.conexion.commit()
            cursor.close()

            print("Tarea insertada correctamente")
            print(f"INSERT con:{campos}")
            print(f"ID: {id_tarea}")
            return id_tarea

        except Error as e:
            rdo=f"Error al insertar tarea: {e}"
            print(rdo)
            return str(e)

    def cargar_tareas(self):
        if not self.conexion:
            print("No hay nada conectado")
            return
        try:
            consulta = "SELECT id_tarea,nombre,descripcion,categoria,prioridad,fecha FROM base_de_datos_proyecto.tareas"
            cursor = self.conexion.cursor()
            cursor.execute(consulta)
            filas = cursor.fetchall()
            cursor.close()

            self.lista_tareas.clear()
            self.diccionario_tareas_modo_calendario.clear()

            for fila in filas:
                id_tarea, nombre, descripcion, categoria, prioridad, fecha = fila

                fecha_str = fecha.strftime("%Y-%m-%d")
                fecha_en_qdate = QDate.fromString(str(fecha_str),"yyyy-MM-dd")

                tarea = f"• {nombre}"

                item = QListWidgetItem(tarea)
                item.setData(Qt.UserRole, id_tarea)
                item.setData(Qt.UserRole + 1, nombre)
                item.setData(Qt.UserRole + 2, descripcion)
                item.setData(Qt.UserRole + 3, categoria)
                item.setData(Qt.UserRole + 4, prioridad)
                item.setData(Qt.UserRole + 5, fecha_en_qdate)

                self.lista_tareas.addItem(item)

                tareas_dict = {
                    "id":id_tarea,
                    "nombre":nombre,
                    "descripcion":descripcion,
                    "categoria":categoria,
                    "prioridad":prioridad,
                    "fecha":fecha_str
                }

                self.diccionario_tareas_modo_calendario.setdefault(fecha_str, []).append(tareas_dict)
                print(f"Cargando tarea id={id_tarea}, nombre={nombre}")

                formato = self.resaltado_segun_prioridad(prioridad)
                self.calendario.setDateTextFormat(fecha_en_qdate,formato)
                self.calendario.update()

            self.calendario.update()

        except Error as e:
            rdo=f"Error al cargar tareas: {e}"
            print(rdo)

    def modificar_tarea(self, id_tarea, nombre, descripcion, categoria, prioridad, fecha):
        if not self.conexion:
            print("No hay nada conectado")
            return
        try:
            fecha_str = fecha.toString("yyyy-MM-dd")
            consulta = """
                        UPDATE tareas
                        SET nombre = %s, descripcion = %s, categoria = %s, prioridad = %s, fecha = %s
                        WHERE id_tarea = %s"""
            campos = (nombre, descripcion, categoria, prioridad, fecha_str, id_tarea)
            cursor = self.conexion.cursor()
            cursor.execute(consulta,campos)
            self.conexion.commit()
            cursor.close()
            
            print("Tarea modificada correctamente")
            print(f"UPDATE con:{campos}")
            print(f"ID: {id_tarea}")

        except Error as e:
            return e
        
    def eliminar_tarea(self,id_tarea):
        if not self.conexion:
            print("No hay nada conectado")
            return
        try:
            consulta = "DELETE FROM tareas WHERE id_tarea = %s"
            cursor = self.conexion.cursor()
            cursor.execute(consulta, (id_tarea,))
            self.conexion.commit()
            cursor.close()
            
            print(f"Tarea con ID {id_tarea} eliminada de la base de datos")
            return True
    
        except Error as e:
            print(f"Error al eliminar tarea: {e}")
            return str(e)
        
    def consultar_tareas(self, consulta):
        cursor = self.conexion.cursor()
        cursor.execute(consulta)
        filas = cursor.fetchall()
        cursor.close()

        self.lista_tareas.clear()
        for id_tarea, nombre, descripcion, categoria, prioridad, fecha in filas:
            fecha_str = fecha.strftime("%Y-%m-%d")

            item = QListWidgetItem(f"• {nombre}")
            item.setData(Qt.UserRole, id_tarea)
            item.setData(Qt.UserRole + 1, nombre)
            item.setData(Qt.UserRole + 2, descripcion)
            item.setData(Qt.UserRole + 3, categoria)
            item.setData(Qt.UserRole + 4, prioridad)
            item.setData(Qt.UserRole + 5, fecha_str)
            self.lista_tareas.addItem(item)

    def avanzar_paginas(self):
        try:
            fecha_actual = self.calendario.selectedDate().toString("yyyy-MM-dd")

            cursor = self.conexion.cursor()
            cursor.execute("SELECT COUNT(*) FROM tareas WHERE fecha = %s", (fecha_actual,))
            total_tareas = cursor.fetchone()[0]
            cursor.close()

            total_paginas = max(1, (total_tareas - 1) // self.limite_paginas + 1)

            if self.flag:
                consulta = f"""
                    SELECT id_tarea, nombre, descripcion, categoria, prioridad, fecha
                    FROM tareas
                    WHERE fecha = '{fecha_actual}'
                    ORDER BY id_tarea
                    LIMIT {self.limite_paginas} OFFSET {self.paginas_salteadas};
                """
                self.consultar_tareas(consulta)
                self.flag = False

            else:
                if self.indice_pagina < total_paginas:
                    self.indice_pagina += 1
                    self.paginas_salteadas = (self.indice_pagina - 1) * self.limite_paginas

                    consulta = f"""
                        SELECT id_tarea, nombre, descripcion, categoria, prioridad, fecha
                        FROM tareas
                        WHERE fecha = '{fecha_actual}'
                        ORDER BY id_tarea
                        LIMIT {self.limite_paginas} OFFSET {self.paginas_salteadas};
                    """
                    self.consultar_tareas(consulta)

        except Error as e:
            print(f"Error al avanzar páginas: {e}")

    def retroceder_paginas(self):
        try:
            if self.indice_pagina <= 1:
                self.indice_pagina = 1
                self.paginas_salteadas = 0
            else:
                self.paginas_salteadas -= self.limite_paginas
                self.indice_pagina -= 1

            fecha_actual = self.calendario.selectedDate().toString("yyyy-MM-dd")
            consulta = f"""
                SELECT id_tarea, nombre, descripcion, categoria, prioridad, fecha
                FROM tareas
                WHERE fecha = '{fecha_actual}'
                ORDER BY id_tarea
                LIMIT {self.limite_paginas} OFFSET {self.paginas_salteadas};
            """
            fecha_actual = self.calendario.selectedDate().toString("yyyy-MM-dd")

            cursor = self.conexion.cursor()
            cursor.execute("SELECT COUNT(*) FROM tareas WHERE fecha = %s", (fecha_actual,))
            total_tareas = cursor.fetchone()[0]
            total_paginas = max(1, (total_tareas - 1) // self.limite_paginas + 1)
            cursor.close()
            self.consultar_tareas(consulta)

        except Error as e:
            print(f"Error al retroceder páginas: {e}")