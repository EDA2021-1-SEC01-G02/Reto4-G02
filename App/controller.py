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
    firstAirport =0
    lastAirport = 0
    firstAirportInfo= 'Ho.a'
    lastAirportInfo = 'Ho.a'

    airports_file = cf.data_dir + 'airports-utf8-small.csv' #TODO: Reemplazar para la version final del codigo
    airports_input_file = csv.DictReader(open(airports_file, encoding="utf-8"),
                                delimiter=",")
    for airport in airports_input_file: #Recorrer csv
        datos = model.loadAirPorts(catalog, airport, firstAirport, lastAirport, firstAirportInfo, lastAirportInfo)
        firstAirport = datos[0]
        lastAirport = datos[1]
        firstAirportInfo= datos[2]
        lastAirportInfo = datos[3]

    firstDf = model.firstAndLastAirportsDF(firstAirportInfo, lastAirportInfo)

    routes_file = cf.data_dir + 'routes-utf8-small.csv' #TODO: Reemplazar para la verion final del codigo
    routes_input_file = csv.DictReader(open(routes_file, encoding="utf-8"),
                                delimiter=",")
    for route in routes_input_file: #Recorrec csv
        model.routes(catalog, route)
    

    cities_file = cf.data_dir + 'worldcities-utf8.csv' #No cambiar lol
    cities_input_file = csv.DictReader(open(cities_file, encoding="utf-8"),
                                delimiter=",")
    firstCity = 0
    for city in cities_input_file: #Recorrer csv
        df2 = model.addCity(catalog, city, firstCity)
        firstCity = df2[0]

    cityDF = model.firstAndLastCitiesDF(df2[0],df2[1])

    return model.first_to_show(catalog, firstDf, cityDF)

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def findConnections(catalog): #Req1
    return model.findConnections(catalog)

def findCluster(catalog,IATA1,IATA2): #Req2
    return model.findCluster(catalog,IATA1,IATA2)

def closedAirport(catalog,airportIATA):
    return model.closedAirport(catalog,airportIATA)
