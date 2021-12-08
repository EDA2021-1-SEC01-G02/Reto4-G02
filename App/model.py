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
from DISClib.ADT import stack as tk
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import mergesort as ms
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from haversine import haversine, Unit
import math as math
import pandas as pd
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
                "airportsID": None,
                "airports": None
                }
    
    catalog["routes"] = gr.newGraph(datastructure='ADJ_LIST', #Grafo denso con todos los aeropuertos y todas las rutas
                                              directed=True,
                                              size=100000,
                                              comparefunction=compareairportiata)

    catalog["connections"] = gr.newGraph(datastructure='ADJ_LIST', #Grafo que se encargara de tener un arco para verificar que ciertos aeropuertos sean paralelos
                                              directed=False,
                                              size=20000,
                                              comparefunction=compareairportiata)

    catalog["cities"] = mp.newMap(maptype='PROBING')

    catalog["airportsID"] = mp.newMap(maptype="PROBING")

    catalog["airports"] = mp.newMap(maptype="PROBING")

    catalog['airCity'] =  mp.newMap(maptype="PROBING")
    catalog['allRoutes'] = mp.newMap(maptype="PROBING")

    return catalog

# Funciones para agregar informacion al catalogo

def getAirports(map, city):
    lst = onluMapValue(map, city)
    return lst

def dijk(catalog,id1,id2):
    search = djk.Dijkstra(catalog['routes'], int(id1))
    if not djk.hasPathTo(search, int(id2)):
        return 
    distance = (djk.distTo(search, int(id2)))
    path =  djk.pathTo(search, int(id2))
    
    return distance, lstFromSt(catalog, path)

def lstFromSt(catalog,stack):
    dict = {}
    newList = lt.newList('ARRAT_LIST', cmpfunction=cmpIATA)
    for it in range(1, tk.size(stack)+1):
        first = tk.pop(stack)
        dep = (onluMapValue(catalog['airports'], (first['vertexA'])))
        depIATA = (onluMapValue(catalog['airports'], (first['vertexA'])))['IATA']
        des = (onluMapValue(catalog['airports'], (first['vertexB'])))
        desIATA = (onluMapValue(catalog['airports'], (first['vertexB'])))['IATA']
        lst = onluMapValue(catalog['allRoutes'], depIATA)
        for pos in range(1, lt.size(lst)+1):
            temp= lt.getElement(lst, pos)
            if temp['Departure'] == depIATA and temp['Destination'] == desIATA:
                final = temp
                break
        if lt.size(newList) == 0:
            lt.addLast(newList, dep)
        elif dep != lt.getElement(newList, lt.size(newList)):
            lt.addLast(newList, dep)
        if des != lt.getElement(newList, lt.size(newList)):
            lt.addLast(newList, des)
        dict[it]= final
    return routesDF(dict), thTable(newList, lt.size(newList)+1)

def thTable(lst, len):
    dict = {}
    for pos in range(1, len):
        temp = lt.getElement(lst, pos)
        dict[pos] = temp
    return pd.DataFrame.from_dict(dict, orient = 'index')[['IATA', 'Name', 'City', 'Country']]

def cmpIATA(item1, item2):
    if item1['IATA'] > item2['IATA']:
        return  True
    else: 
        return False

def routesDF(dict):
    return pd.DataFrame.from_dict(dict, orient='index')
    
def getNear(lst, cityCor):
    size = lt.size(lst)+1
    min = 100000000000*1000000000
    airport = 0
    for pos in range(1, size):
        temp = lt.getElement(lst, pos)
        corTemp = float(temp['Latitude']), float(temp['Longitude'])
        tempDis =calDis(cityCor, corTemp)
        if tempDis < min:
            min =  tempDis
            airport = temp

    return airport
def onlyOneDF(item):
    dict = {1: item}
    return pd.DataFrame.from_dict(dict, orient='index')[['IATA', 'Name', 'City', 'Country']]

def getCityCor(catalog, city):
    temp = mp.get(catalog['cities'], city)
    cor =  temp['lat'], temp['lng']
    return cor
def getCityInfo(catalog, city):
    lst = onluMapValue(catalog['cities'], city)
    return slecTable(lst), lst

def slecTable(lst):
    dict ={}
    len = lt.size(lst)+1
    for pos in range(1, len):
        temp = lt.getElement(lst, pos)
        dict[pos] = temp
    return (pd.DataFrame.from_dict(dict, orient = 'index'))


def loadAirPorts(catalog,airport, firstAirport, lastAirport, firstAirportInfo, lastAirportInfo):
    """
    Carga los datos ademas de mostrar informacion solicitada

    Recibe la estructura de datos (idealmente vacia)

    Retorna tres tuplas:
        1.(Numero de aeropuertos del grafo dirigido, numero de rutas del grafo dirigido y dataframe de los aeropuertos)
        2.(Numero de aeropuertos del grafo no dirigido y numero de rutas del grafo no dirigido)
        3.(Numero de ciudades cargadas en el RBT y dataframe de las ciudades)
    """
    addAirCity(catalog['airCity'], airport)

    #Crear vertices en los grafos   
    tempid = int(airport["id"]) #Conversion de str a int para comparar valores
    if (tempid > lastAirport) : #Si el registro tiene un id mas grande o no hay un id registrado
        lastAirport = tempid #Reemplaza por el nuevo id
        lastAirportInfo = airport #Guarda los datos
    if (tempid < firstAirport)or (firstAirport ==0) : #Si el registro tiene un id mas pequeño o no hay un id registrado
        firstAirport = tempid #Reemplaza por el nuevo id
        firstAirportInfo = airport #Guarda los datos
    mp.put(catalog["airportsID"],airport["IATA"],airport["id"]) #Guarda el id y el IATA del aeropuerto en el bst para cambiar de IATA a id facil
    mp.put(catalog["airports"],int(airport["id"]),airport)
    gr.insertVertex(catalog["routes"],float(airport["id"])) #Añade vertices a los grafos
    gr.insertVertex(catalog["connections"],float(airport["id"])) #Lo de arriba
    return firstAirport, lastAirport, firstAirportInfo, lastAirportInfo

def addAirCity(table, airport):
    if mp.get(table,airport['City']) is None:
        mp.put(table,airport['City'], lt.newList('ARRAY_LIST'))
    map = onluMapValue(table, airport['City'])
    lt.addLast(map, airport)



def routes(catalog, route):
    addRoutesByDep(catalog['allRoutes'] , route)
    vertexDep = getIDbyIATA(catalog,route["Departure"]) #Conversion del IATA a id
    vertexDes = getIDbyIATA(catalog,route["Destination"]) #Lo de arriba
    gr.addEdge(catalog["routes"],vertexDep,vertexDes,float(route["distance_km"])) #Añadir arco al grafo dirigido
    edge = gr.getEdge(catalog['connections'], vertexDep, vertexDes)
    if edge is None:
        gr.addEdge(catalog["connections"],vertexDep,vertexDes,0) #Añade arco al grafo no dirigido

def addRoutesByDep(catalog, route):
    if not mp.contains(catalog, route['Departure']):
        mp.put(catalog, route['Departure'],lt.newList('ARRAY_LIST'))
    item = onluMapValue(catalog, route['Departure'])
    lt.addLast(item, route)


def calDis(first, sec):
    return haversine(first, sec)

def addCity(catalog, city, firstCityInfo, cont):
    if firstCityInfo == 0: #Si no es el primer registro del csv
        firstCityInfo = city 
    lastCityInfo = city
    if mp.get(catalog["cities"],(city["city"])) is None: #Añade los datos a un mapa, donde la llave sera el id en int y el valor seran los datos
        lst = lt.newList('ARRAY_LIST')
        mp.put(catalog["cities"],(city["city"]),lst)
    lst2 = onluMapValue(catalog["cities"],city["city"])
    lt.addLast(lst2, city)
    cont += 1
    
    return (firstCityInfo, lastCityInfo, cont)

def first_to_show(catalog, airportDF, cityDF, cont):
    return ((gr.numVertices(catalog["routes"]),gr.numEdges(catalog["routes"]),airportDF),(lt.size(gr.vertices(catalog["connections"])),gr.numEdges(catalog["connections"])),(str(cont),cityDF))
# Funciones para creacion de datos

def firstAndLastAirportsDF(firstinfo,lastinfo):
    """
    Crea el DataFrame para mostrar la primera y la ultima ciudad cargada en los grafos de routes y connections
    """
    airports = {}
    airports[0] = firstinfo["IATA"],firstinfo["Name"],firstinfo["City"],firstinfo["Country"],firstinfo["Latitude"],firstinfo["Longitude"]
    airports[1] = lastinfo["IATA"],lastinfo["Name"],lastinfo["City"],lastinfo["Country"],lastinfo["Latitude"],lastinfo["Longitude"]
    return pd.DataFrame.from_dict(airports,orient="index",columns=["IATA","Nombre","Ciudad","Pais","Latitud","Longitud"])

def firstAndLastCitiesDF(firstinfo,lastinfo):
    cities = {}
    cities[0] = firstinfo["city"],firstinfo["country"],firstinfo["lat"],firstinfo["lng"],firstinfo["population"]
    cities[1] = lastinfo["city"],lastinfo["country"],lastinfo["lat"],lastinfo["lng"],lastinfo["population"]
    return pd.DataFrame.from_dict(cities,orient="index",columns=["Ciudad","Pais","Latitud","Longitud","Poblacion"])

def closedAirportDF(catalog,airports):
    ms.sort(airports,cmpAirportsByID)
    cities = {}
    size = lt.size(airports)
    for city in range(1,4):
        if (city > size):
            break
        else:
            temp = lt.getElement(airports,city)
            tempdata = mp.get(catalog["airports"],temp)
            data = tempdata["value"]
            cities[city] = data["IATA"],data["Name"],data["City"],data["Country"]
        
    for city in range (size-3,size+1):
        if not (city in range(1,4)):
            temp = lt.getElement(airports,city)
            tempdata = mp.get(catalog["airports"],temp)
            data = tempdata["value"]
            cities[city] = data["IATA"],data["Name"],data["City"],data["Country"]
    
    return (size,pd.DataFrame.from_dict(cities, orient="index", columns=["IATA","Nombre","Ciudad","Pais"]))


# Funciones de consulta

def findConnections(catalog):
    cont2 = 0
    cont = 0
    items = gr.vertices(catalog['routes'])
    lst = lt.newList('ARRAY_LIST')
    for pos in range(0, lt.size(items)):
        ver = lt.getElement(items,pos)
        inbound = gr.indegree(catalog['connections'], ver)
        outdegree = gr.outdegree(catalog['connections'], ver)
        inbound2 = gr.indegree(catalog['routes'], ver)
        outdegree2 = gr.outdegree(catalog['routes'], ver)
        degree = inbound+ inbound2 + outdegree + outdegree2
        degree1 =gr.degree(catalog['routes'], ver)
        degree2 = gr.degree(catalog['connections'], ver)
        cont2 = degree1 + degree2

        item = onluMapValue(catalog['airports'], ver)
        item['inbound'] = inbound + inbound2
        item['outbound'] = outdegree + outdegree2
        item['Connections'] = degree 
        item['Connections False'] = cont2
        lt.addLast(lst, item)
        if degree > 0 :
            cont +=1  
    ms.sort(lst, cmpDegree)
    tabla = crTable(lst, 6)
    numv = gr.numVertices(catalog['routes'])
    
    return numv,cont, tabla

def crTable(lst, len):
    dict = {}
    if len > lt.size(lst):
        len = lt.size(lst)
    for pos in range(1, len):
        temp = lt.getElement(lst, pos)
        dict[pos] = temp
    return (pd.DataFrame.from_dict(dict, orient = 'index')[['Name', 'City', 'Country', 'IATA', 'Connections','inbound', 'outbound']])

def getIDbyIATA(catalog,IATA):
    """
    Recibe un IATA de un aeropuerto y retorna el ID del aeropuerto
    """
    return int(onluMapValue(catalog["airportsID"],IATA))
def onluMapValue(map, key):
    pair = mp.get(map, key)
    return me.getValue(pair)

#Req 2
def findCluster(catalog,IATA1,IATA2):
    airport1 = getIDbyIATA(catalog,IATA1) #Retorna un ID segun el IATA
    airport2 = getIDbyIATA(catalog,IATA2) #Lo de arriba

    airportsScc = scc.KosarajuSCC(catalog["routes"]) #Algoritmo kosaraju
    numScc = scc.connectedComponents(airportsScc) #Obtener el numero de clusteres en el grafo
    connectedScc = scc.stronglyConnected(airportsScc,airport1,airport2) #Revisar si ambos aeropuertos estan en el mismo cluster

    return (numScc,connectedScc)

#Req4
def useMiles(catalog,city,miles):
    airports = mp.get(catalog["airCity"],city)
    source = lt.getElement(airports["value"],1)
    temp = djk.Dijkstra(catalog["routes"],int(source["id"]))
    for i in range(1,lt.size(airports["value"])+1):
        tempsource = lt.getElement(airports["value"],i)
        canReturn = djk.hasPathTo(temp,int(tempsource["id"]))
        if canReturn:
            numNodes = 0
            kilometers = miles*1.60
            cost = djk.distTo(temp,int(tempsource["id"]))
            finalMiles = (kilometers-cost)/1.60
            break
    if canReturn:
        cost = djk.distTo(temp,int(tempsource["id"]))
    return (canReturn,numNodes,cost,0,finalMiles)

#Req 5
def closedAirport(catalog,airportIATA):
    airportId = getIDbyIATA(catalog,airportIATA) #Obtiene la id de un puerto a traves de el IATA
    
    numAirportsDigraph = gr.numVertices(catalog["routes"]) #Valores originales de los grafos
    numRoutesDigraph = gr.numEdges(catalog["routes"])
    numAirportsGraph = gr.numVertices(catalog["connections"])
    numRoutesGraph = gr.numEdges(catalog["connections"])

    finalNumAirportsDigraph = numAirportsDigraph - 1
    finalNumRoutesDigraph = numRoutesDigraph - (gr.indegree(catalog["routes"],airportId)+gr.outdegree(catalog["routes"],airportId))
    finalNumAirportsGraph = numAirportsGraph - 1
    finalNumRoutesGraph = numRoutesGraph - gr.degree(catalog["connections"],airportId)

    airportsDF = closedAirportDF(catalog,gr.adjacents(catalog["connections"],airportId))

    return ((numAirportsDigraph,numRoutesDigraph),(numAirportsGraph,numRoutesGraph),(finalNumAirportsDigraph,finalNumRoutesDigraph),(finalNumAirportsGraph,finalNumRoutesGraph),(airportsDF))




# Funciones utilizadas para comparar elementos dentro de una lista

def compareairportiata (airportid, keyvalueairport):
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
    if (ID1== ID2):
        return 0
    elif (ID1 > ID2):
        return 1
    else:
        return -1

def cmpAirportsByID(airport1,airport2):
    if (airport1 < airport2):
        return True
    else:
        return False

def cmpDegree(item1, item2):
    if item1['Connections'] > item2['Connections'] :
        return True
    else:
        return False
# Funciones de ordenamiento
