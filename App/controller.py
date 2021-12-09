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
 """

from App.model import addCity
import config as cf
import model
import csv

#import time 
#Iniciar: start_time = time.process_time()

#Terminar: stop_time = time.process_time()
#          print((stop_time - start_time)*1000)


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def newCatalog():
    """
    Llama la funcion de inicializacion del modelo.
    """
    # analyzer es utilizado para interactuar con el modelo
    catalog = model.newCatalog()
    return catalog

# Funciones para la carga de datos

def loadData(catalog):
    """
    Carga los datos
    """
    firstAirport = 0
    lastAirport = 0
    firstAirportInfo= 'Ho.a'
    lastAirportInfo = 'Ho.a'
    countNodes = 0
    countEdgesDigraph = 0
    countEdgesGraph = 0

    airports_file = cf.data_dir + 'airports-utf8-large.csv'
    airports_input_file = csv.DictReader(open(airports_file, encoding="utf-8"),
                                delimiter=",")
    for airport in airports_input_file: #Recorrer csv

        datos = model.loadAirPorts(catalog, airport, firstAirport, lastAirport, firstAirportInfo, lastAirportInfo)
        firstAirport = datos[0]
        lastAirport = datos[1]
        firstAirportInfo= datos[2]
        lastAirportInfo = datos[3]
        countNodes+=1

    firstDf = model.firstAndLastAirportsDF(firstAirportInfo, lastAirportInfo)

    routes_file = cf.data_dir + 'routes-utf8-large.csv'
    routes_input_file = csv.DictReader(open(routes_file, encoding="utf-8"),
                                delimiter=",")
    for route in routes_input_file: #Recorrec csv
        toCount = model.routes(catalog, route)
        if toCount[0]:
            countEdgesDigraph += 1
        if toCount[1]:
            countEdgesGraph += 1

    cities_file = cf.data_dir + 'worldcities-utf8.csv' #No cambiar lol
    cities_input_file = csv.DictReader(open(cities_file, encoding="utf-8"),
                                delimiter=",")
    firstCity = 0
    cont = 0
    for city in cities_input_file: #Recorrer csv
        df2 = model.addCity(catalog, city, firstCity, cont)
        cont = df2[2]
        firstCity = df2[0]

    cityDF = model.firstAndLastCitiesDF(df2[0],df2[1])

    return ((model.first_to_show(catalog, firstDf, cityDF, cont)),(countNodes,countEdgesDigraph,countEdgesGraph))

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def findConnections(catalog): #Req1
    return model.findConnections(catalog)

def findCluster(catalog,IATA1,IATA2): #Req2
    return model.findCluster(catalog,IATA1,IATA2)

def useMiles(catalog,miles,indice1,inicio): #Req 4
    dep = model.lt.getElement(inicio,indice1) #Obtiene los datos de la ciudad seleccionada por el usuario de entre la lista
    depAir = model.getAirports(catalog["airCity"],dep["city"]) #Obtiene los aeropuertos de la ciudad
    return model.useMiles(catalog,miles,depAir)

def closedAirport(catalog,airportIATA): #Req5
    return model.closedAirport(catalog,airportIATA)

def getAir(catalog, inicio, destino):
    choTab = model.getCityInfo(catalog, inicio)
    choTab2 = model.getCityInfo(catalog, destino)

    return choTab, choTab2

def findRoute( catalog, indice1, indice2, inicio, destino ):

    dep = model.lt.getElement(inicio, indice1)
    des = model.lt.getElement(destino, indice2)
    corDep = float(dep['lat']), float(dep['lng'])
    corDes = float(des['lat']), float(des['lng'])
    depAirport = model.getNear(catalog, corDep)
    depid = depAirport['id']
    desAirport = model.getNear(catalog, corDes)
    desid = desAirport['id']
    depDF = model.onlyOneDF(depAirport)
    desDF = model.onlyOneDF(desAirport)
    result = (model.dijk(catalog, depid, desid))
    if result is not None:
        return result, depDF, desDF
    return None, depDF, desDF