"""
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
        print("Inicializando ....")
        catalog = controller.newCatalog()
        print("Cargando información de los archivos ....")
        resultado = controller.loadData(catalog) #Tupla que contiene catalogo y mas tuplas con la info solicitada. Una para cada grafo
        print("\n=== Grafo 1 ===\n")
        print("Aeropuertos: ",resultado[0][0])
        print("Rutas aéreas: ",resultado[0][1])
        print("Primer y ultimo aeropuerto cargado en el grafo: ")
        print(resultado[0][2])
        
        print("\n=== Grafo 2 ===\n")
        print("Aeropuertos: ",resultado[1][0])
        print("Rutas aéreas: ",resultado[1][1])
        print("Primer y ultimo aeropuerto cargado en el grafo: ")
        print(resultado[0][2])

        print("\n=== Red de ciudades ===\n")
        print("Numero de ciudades: ",resultado[2][0])
        print("Primera y ultima ciudad cargada en la estructura de datos: ")
        print(resultado[2][1])
        

    elif int(inputs[0]) == 2:
        resultado = controller.findConnections(catalog)
        print("Aeropuertos conectados en la red: ",resultado[0]) #Imprimir lista
        print("Aeropuertos dentro de la red: ", resultado[1] )
        print("Top 5 aeropuertos interconectados: ")
        print(resultado[2])


    #Req 2
    elif int(inputs[0]) == 3: #TODO: Modificar para que solicite datos al usuario
        #codigo1 = input("Codigo IATA del aeropuerto 1: ")
        #codigo2 = input("Codigo IATA del aeropuerto 2: ")
        codigo1 = "LED"
        codigo2 = "RTP"
        resultado = controller.findCluster(catalog,codigo1,codigo2)
        print("Numero de clusteres presentes en la red de transporte aereo: ",resultado[0])
        if resultado[1]:
            print("Los aeropuertos SI se encuentran en el mismo cluster.")
        else:
            print("Los aeropuertos NO se encuentran en el mismo cluster.")

    elif int(inputs[0]) == 4:
        ciudadOrigen = 'St. Petersburg' #input("Ciudad de origen: ")
        ciudadDestino = 'Lisbon' #input("Ciudad de destino: ")
        part1 = controller.getAir(catalog, ciudadOrigen, ciudadDestino)
        print(part1[0][0])
        option1 = int(input('Seleccione la ciudad de salida: '))
        print(part1[1][0])
        option1 = int(input('Seleccione la ciudad de salida: '))
        #resultado = controller.findRoute(catalog, ciudadOrigen, ciudadDestino)
        print("El aeropuerto de la ciudad origen (",ciudadOrigen,") es: ",resultado[0])
        print("El aeropuerto de la ciudad destino (",ciudadDestino,") es: ",resultado[1])
        print("Ruta: ",resultado[2])
        print("Distancia total de viaje: ",resultado[3])

    #Req 4
    elif int(inputs[0]) == 5:
        ciudad = "Lisbon" #input("Ciudad origen: ")
        millas = 1000 #int(input("Cantidad de millas disponibles: "))
        resultado = controller.useMiles(catalog,ciudad,millas)
        if resultado[0]:
            print("Numero de aeropuertos conectados a la red de expansion minima: ",resultado[1])
            print("Costo total al arbol de expansion minima: ",resultado[2])
            print("Rama mas larga: ",resultado[3]) #Imprimir rama
            if resultado[4] < 0:
                print("Millas faltantes para realizar el recorrido:",resultado[4])
            else:
                print("Millas excedentes para realizar el recorrido:",resultado[4])
        else:
            print("No hay manera de salir y llegar a",ciudad)

    #Req5
    elif int(inputs[0]) == 6:
        #aeropuerto = input("Código IATA del aeropuerto fuera de servicio: ")
        aeropuerto = "DXB"
        resultado = controller.closedAirport(catalog,aeropuerto)
        print("--- Datos originales ---")
        print("El grafo dirigido cuenta con",resultado[0][0],"aeropuertos y",resultado[0][1],"rutas.")
        print("El grafo no dirigido cuenta con",resultado[1][0],"aeropuertos y",resultado[1][1],"rutas.")

        print("--- Nuevos datos ---")
        print("El grafo dirigido contaria con",resultado[2][0],"aeropuertos y",resultado[2][1],"rutas restantes.")
        print("El grafo no dirigido contaria con",resultado[3][0],"aeropuertos y",resultado[3][1],"rutas restantes.")
        print("\nHay",resultado[4][0],"aeropuertos afectados por el cierre de",aeropuerto)
        print("Los tres primeros y tres ultimoa esropuertos afectados son: ")
        print(resultado[4][1])

    #elif int(inputs[0]) == 7:
    #    pass

    #elif int(inputs[0]) == 8:
    #    pass

    else:
        sys.exit(0)
sys.exit(0)
