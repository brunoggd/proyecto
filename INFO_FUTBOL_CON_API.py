import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import requests

def obtener_equipo():
    equipo = input("Ingresá el nombre del equipo (Debe ser el nombre completo): ")
    url = f"https://www.thesportsdb.com/api/v1/json/123/searchteams.php?t={equipo}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['teams']:
            team = data['teams'][0]
            print("Nombre:", team['strTeam'])
            print("Estadio:", team['strStadium'])
            print("Liga en la que juega:", team['strLeague'])
            print("País:",team['strCountry'])
            print("Descripción:", team['strDescriptionES'])
        else:
            print("No se encontró el equipo que buscabas, ingresa el nombre completo.")
    else:
        print("Error:", response.status_code)
    return data

def obtener_jugador():
    jugador = input("Ingresá el nombre del jugador (Debe ser el nombre y apellido completo): ")
    url = f"https://www.thesportsdb.com/api/v1/json/123/searchplayers.php?p={jugador}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['player']:
            player = data['player'][0]
            print("Nombre:", player['strPlayer'])
            print("Género:", player['strGender'])
            print("Fecha de nacimiento:", player['dateBorn'])
            print("Club en el que juega:", player['strTeam'])
            print("Posición:", player['strPosition'])
        else:
            print("No se encontró el jugador que buscabas, ingresa el nombre completo.")
    else:
        print("Error:", response.status_code)
    return data

def obtener_liga():
    liga = input("Ingresá el ID de la liga que quieras buscar: ")
    url = f"https://www.thesportsdb.com/api/v1/json/123/lookupleague.php?id={liga}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['leagues']:
            liga = data['leagues'][0]
            print("Nombre de la liga:", liga['strLeague'])
            print("País de la liga:", liga['strCountry'])
            print("Temporada actual:",liga['strCurrentSeason'])
            print("Descripción:",liga['strDescriptionES'])
        else:
            print("No se encontró la liga que buscabas, ingresa el nombre completo.")
    else:
        print("Error:", response.status_code)
    return data

if __name__ == "__main__":
    obtener_equipo()
    obtener_jugador()
    obtener_liga()
