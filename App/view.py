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
import sys
import config
import threading
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

catalog = None

"""
Menu principal
"""

def thread_cycle():
    while True:
        printMenu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs[0]) == 1:
            print("Inicializando ....")
            catalog = controller.newCatalog()
            print("Cargando información de los archivos ....")
            resultado = controller.loadData(catalog) 
            print("\n=== Grafo 1 ===\n")
            print("Aeropuertos: ",resultado[0][0][0])
            print("Rutas aéreas: ",resultado[0][0][1])
            print("Nodes:",resultado[1][0],"& Edges:",resultado[1][1])
            print("Primer y ultimo aeropuerto cargado en el grafo: ")
            print(resultado[0][0][2])
            
            print("\n=== Grafo 2 ===\n")
            print("Aeropuertos: ",resultado[0][1][0])
            print("Rutas aéreas: ",resultado[0][1][1])
            print("Nodes:",resultado[1][0],"& Edges:",resultado[1][2])
            print("Primer y ultimo aeropuerto cargado en el grafo: ")
            print(resultado[0][0][2])

            print("\n=== Red de ciudades ===\n")
            print("Numero de ciudades: ",resultado[0][2][0])
            print("Primera y ultima ciudad cargada en la estructura de datos: ")
            print(resultado[0][2][1])
            
        #Req1
        elif int(inputs[0]) == 2:
            resultado = controller.findConnections(catalog)
            print("Aeropuertos conectados en la red: ",resultado[0]) #Imprimir lista
            print("Aeropuertos dentro de la red: ", resultado[1] )
            print("Top 5 aeropuertos interconectados: ")
            print(resultado[2])

        #Req 2
        elif int(inputs[0]) == 3:
            codigo1 = input("Codigo IATA del aeropuerto 1: ")
            codigo2 = input("Codigo IATA del aeropuerto 2: ")
            codigo1 = "LED"
            codigo2 = "RTP"
            resultado = controller.findCluster(catalog,codigo1,codigo2)
            print("Numero de clusteres presentes en la red de transporte aereo: ",resultado[0])
            if resultado[1]:
                print("Los aeropuertos SI se encuentran en el mismo cluster.")
            else:
                print("Los aeropuertos NO se encuentran en el mismo cluster.")

        elif int(inputs[0]) == 4:
            ciudadOrigen = input("Ciudad de origen: ")
            ciudadDestino = input("Ciudad de destino: ")
            part1 = controller.getAir(catalog, ciudadOrigen, ciudadDestino)
            print(part1[0][0])
            option1 = int(input('\nSeleccione el aeropuerto de la ciudad de salida: '))
            cityF = part1[0][1]
            print(part1[1][0])
            option2 = int(input('\nSeleccione el aeropuerto de la ciudad de llegada: '))
            cityD = part1[1][1]
            resultado = controller.findRoute(catalog,option1,option2, cityF, cityD)
            if resultado[0] is None:
                print('El aeropuerto de partida es: ')
                print(resultado[1])
                print('El aeropuerto de llegada es: ')
                print(resultado[2])
                print("No se puede llegar de %s a %s" %(ciudadOrigen, ciudadDestino))
                continue
            print('============ Resultados Req. 3 ============')
            print("\n======= El aeropuerto de la ciudad origen ",ciudadOrigen," es: =======")
            print('\n',resultado[1])
            print("\n=======El aeropuerto de la ciudad destino ",ciudadDestino," es: =======")
            print('\n', resultado[2])
            print("\n==== Segun Dijsktra, la mejor ruta seria ==== ")
            print("\nDistancia total de viaje es ",resultado[0][0], ' km')
            print("\n=== Ruta del viaje es: ===")
            print(resultado[0][1][0])
            print("\n=== Paradas de la ruta ===")
            print(resultado[0][1][1])

        #Req 4
        elif int(inputs[0]) == 5:
            ciudad = input("Ciudad origen: ")
            parte1=controller.getAir(catalog,ciudad,ciudad) #Obtener aeropuertos de las ciudades
            print(parte1[0][0]) #Mostrar al usuario la lista de las ciudades
            seleccion = int(input("Seleccione el aeropuerto: ")) #Seleccionar un aeropuerto de los disponibles
            origen = parte1[0][1] #Seleccion de la lista de los aeropuertos de la ciudad. No importa si es parte[0] o parte[1] ya que ambas son la misma ciudad
            millas = float(input("Cantidad de millas disponibles del pasajero: "))
            resultado = controller.useMiles(catalog,millas,seleccion,origen) #Llamar a la funcion
            print("+++ Aeropuerto de salida para el codigo IATA:",resultado[0],"+++") #Imprime IATA
            print(resultado[1]) #Imprime Dataframe del aeropuerto
            print("\nNumero de aeropuertos posibles:",resultado[2]) 
            print("Distancia de viaje entre aeropuertos: ",resultado[3])
            print("Millas de pasajero disponibles en kilometros:",resultado[4])
            print("\n+++ Ruta mas larga posible con el aeropuerto",resultado[0],"+++")
            print("Distancia de la ruta mas larga posible: ",resultado[5])
            print("Detalles de la ruta mas larga: ")
            print(resultado[6]) #Imprimir rama (posible dataframe)

        #Req5
        elif int(inputs[0]) == 6:
            aeropuerto = input("Código IATA del aeropuerto fuera de servicio: ")
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

        else:
            sys.exit(0)

if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=thread_cycle)
    thread.start()