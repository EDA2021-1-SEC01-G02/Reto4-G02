"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT.graph import gr
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
import csv
assert cf

import model
#import time 
#Iniciar: start_time = time.process_time()

#Terminar: stop_time = time.process_time()
#          print((stop_time - start_time)*1000)

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newAnalyzer():
    """
    Inicia el analizador

    routes: Digrafo con todas las rutas entre todos los aeropuertos
    connections: Grafo no dirigido para verificar si hay una
                conexion de ida y vuelta entre aeropuertos
    cities: Arbol RBT con los datos de las ciudades
    citiesID: Lista con las ciudades como llave y sus IDs como valor
    """
    analyzer = {
                "routes": None,
                "connections": None,
                "cities": None,
                "citiesID": None,
                }
    
    analyzer["routes"] = gr.newGraph(datastructure='ADJ_LIST', #Grafo denso con todos los aeropuertos y todas las rutas
                                              directed=False,
                                              size=100000,
                                              comparefunction=compareStopIds)

    analyzer["connections"] = gr.newGraph(datastructure='ADJ_LIST', #Grafo que se encargara de tener un arco para verificar que ciertos aeropuertos sean paralelos
                                              directed=True,
                                              size=20000,
                                              comparefunction=compareStopIds)

    analyzer["cities"] = om.newMap(omaptype='RBT', #Mapa organizado por ids
                                      comparefunction=compareDates)

    analyzer["citiesID"] = lt.newList('ARRAY_LIST', compareIds) #Lista que tendra por llave el id de la ciudad y como valor sus datos. Posiblemente se pueda remover dependiendo de como se implemente el mapa de ciudades

# Funciones para agregar informacion al catalogo

def loadData(routes,connections,cities,citiesID):
    
    airports_file = cf.data_dir + 'airports-utf8-small.csv'
    airports_input_file = csv.DictReader(open(airports_file, encoding="utf-8"),
                                delimiter=",")
    for airport in airports_input_file:
        print(airport)
        gr.insertVertex(routes,airport["IATA"])
        gr.insertVertex(connections,airport["IATA"])
        

    routes_file = cf.data_dir + 'routes-utf8-small.csv'
    routes_input_file = csv.DictReader(open(routes_file, encoding="utf-8"),
                                delimiter=",")
    for route in routes_input_file:
        gr.addEdge(routes,route["Departure"],route["Destination"],route["distance_km"])
        gr.addEdge(connections,route["Departure"],route["Destination"],1)

    """
    cities_file = cf.data_dir + 'worldcities-utf8.csv'
    cities_input_file = csv.DictReader(open(cities_file, encoding="utf-8"),
                                delimiter=",")
    for city in cities_input_file:
        mp.
    """

    
    return (model.sightSize(catalog)),(model.minKey(catalog)), (model.maxKey(catalog))

# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento
