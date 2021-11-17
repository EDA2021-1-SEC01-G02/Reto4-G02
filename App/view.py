﻿"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Encontrar puntos de interconexión aérea")
    print("3- Encontrar clústeres de tráfico aéreo")
    print("4- Encontrar la ruta más corta entre ciudades")
    print("5- Utilizar las millas de viajero")
    print("6- Cuantificar el efecto de un aeropuerto cerrado")
    #print("7- Comparar con servicio WEB externo")
    #print("8- Visualizar gráficamente los requerimientos")

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        resultado = controller.loadData() #Tupla que contiene catalogo y mas tuplas con la info solicitada. Una para cada grafo
        catalog = resultado[0]
        print("\n-------\nGrafo 1\n-------")
        print("Aeropuertos: ",resultado[1][0])
        print("Rutas aéreas: ",resultado[1][1])
        print("Ciudades: ",resultado[1][2])
        print("Primer aeropuerto cargado:\n",resultado[1][3])
        print("Ultima ciudad cargada:\n",resultado[1][4])
        print("\n-------\nGrafo 2\n-------")
        print("Aeropuertos: ",resultado[2][0])
        print("Rutas aéreas: ",resultado[2][1])
        print("Ciudades: ",resultado[2][2])
        print("Primer aeropuerto cargado:\n",resultado[2][3])
        print("Ultima ciudad cargada:\n",resultado[2][4])


    elif int(inputs[0]) == 2:
        resultado = controller.findConnections(catalog)
        print("Aeropuertos: ",resultado[0]) #Imprimir lista
        print("Numero de aerpouertos interconectados: ",resultado[1])

    elif int(inputs[0]) == 3:
        codigo1 = input("Codigo IATA del aeropuerto 1: ")
        codigo2 = input("Codigo IATA del aeropuerto 2: ")
        resultado = controller.findCluster(catalog,codigo1,codigo2)
        print("Numero de clusteres presentes en la red de transporte aereo: ",resultado[0])
        if resultado[1]:
            print("Los aeropuertos SI se encuentran en el mismo cluster.")
        else:
            print("Los aeropuertos NO se encuentran en el mismo cluster.")

    elif int(inputs[0]) == 4:
        ciudadOrigen = input("Ciudad de origen: ")
        ciudadDestino = input("Ciudad de destino: ")
        resultado = controller.findRoute(catalog, ciudadOrigen, ciudadDestino)
        print("El aeropuerto de la ciudad origen (",ciudadOrigen,") es: ",resultado[0])
        print("El aeropuerto de la ciudad destino (",ciudadDestino,") es: ",resultado[1])
        print("Ruta: ",resultado[2])
        print("Distancia total de viaje: ",resultado[3])


    elif int(inputs[0]) == 5:
        ciudad = input("Ciudad origen: ")
        millas = input("Cantidad de millas disponibles: ")
        resultado = controller.useMiles(catalog,ciudad,millas)
        print("Numero de nodos conectados a la red de expansion minima: ",resultado[0])
        print("Costo total de la red de expansion minima: ",resultado[1])
        print("Rama mas larga: ",resultado[2]) #Imprimir rama
        print("Lista de ciudades recomendadas: ",resultado[3])

    elif int(inputs[0]) == 6:
        aeropuerto = input("Código IATA del aeropuerto fuera de servicio: ")
        resultado = controller.closedAirport(catalog,aeropuerto)
        print("Número de vuelos de salida afectados: ",resultado[0])
        print("Numero de vuelos de entrada afectados: ",resultado[1])
        print("Número de ciudades afectadas: ",resultado[2])
        print("Lista de ciudades afectadas: ",resultado[3])

    #elif int(inputs[0]) == 7:
    #    pass

    #elif int(inputs[0]) == 8:
    #    pass

    else:
        sys.exit(0)
sys.exit(0)
