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
from DISClib.ADT.graph import gr, numVertices
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

def newCatalog():
    """
    Inicia el analizador

    routes: Digrafo con todas las rutas entre todos los aeropuertos
    connections: Grafo no dirigido para verificar si hay una
                conexion de ida y vuelta entre aeropuertos
    cities: Arbol RBT con los datos de las ciudades
    citiesID: Lista con las ciudades como llave y sus IDs como valor
    """
    catalog = {
                "routes": None,
                "connections": None,
                "cities": None,
                "citiesID": None,
                "airportsID": None
                }
    
    catalog["routes"] = gr.newGraph(datastructure='ADJ_LIST', #Grafo denso con todos los aeropuertos y todas las rutas
                                              directed=False,
                                              size=200, #TODO: Cambiar a 100000 para la version final
                                              comparefunction=compareairportiata)

    catalog["connections"] = gr.newGraph(datastructure='ADJ_LIST', #Grafo que se encargara de tener un arco para verificar que ciertos aeropuertos sean paralelos
                                              directed=True,
                                              size=20000,
                                              comparefunction=compareairportiata)

    catalog["cities"] = om.newMap(omaptype='RBT', #Mapa organizado por ids
                                      comparefunction=compareID)

    catalog["airportsID"] = om.newMap(omaptype="BST",comparefunction=compareID)

    return catalog

# Funciones para agregar informacion al catalogo

def loadData(catalog):

    airports_file = cf.data_dir + 'airports-utf8-small.csv'
    airports_input_file = csv.DictReader(open(airports_file, encoding="utf-8"),
                                delimiter=",")
    for airport in airports_input_file:
        om.put(catalog["airportsID"],airport["IATA"],airport["id"])
        gr.insertVertex(catalog["routes"],float(airport["id"]))
        #gr.insertVertex(catalog["connections"],float(airport["id"]))
        
    routes_file = cf.data_dir + 'routes-utf8-small.csv'
    routes_input_file = csv.DictReader(open(routes_file, encoding="utf-8"),
                                delimiter=",")
    for route in routes_input_file:
        gr.addEdge(catalog["routes"],getIDbyIATA(catalog,route["Departure"]),getIDbyIATA(catalog,route["Destination"]),float(route["distance_km"]))
        #gr.addEdge(catalog["connections"],getIDbyIATA(catalog,route["Departure"]),getIDbyIATA(route["Destination"]),1)

    cities_file = cf.data_dir + 'worldcities-utf8.csv'
    cities_input_file = csv.DictReader(open(cities_file, encoding="utf-8"),
                                delimiter=",")
    for city in cities_input_file:
        om.put(catalog["cities"],city["id"],city)
    

    
    return ((gr.numVertices(catalog["routes"]),gr.numEdges(catalog["routes"])),(gr.numVertices(catalog["routes"]),gr.numEdges(catalog["routes"])),(om.size(catalog["cities"])))

# Funciones para creacion de datos

# Funciones de consulta

def getIDbyIATA(catalog,IATA):
    return int(om.get(catalog["airportsID"],IATA)["value"])



# Funciones utilizadas para comparar elementos dentro de una lista

def compareairportiata(airportid, keyvalueairport):
    """
    Compara dos aeropuertos
    """

    airportcode = int(keyvalueairport['key'])
    if (airportid == airportcode):
        return 0
    elif (airportid > airportcode):
        return 1
    else:
        return -1

def compareID(ID1,ID2):
    if (ID1 == ID2):
        return 0
    elif (ID1 > ID2):
        return 1
    else:
        return -1

# Funciones de ordenamiento
