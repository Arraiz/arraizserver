import bs4 as bs
import requests
import csv
import js2py
import json


class bicisApi:

    def __init__(self):
        self.bilbaoURL = "http://www.bilbao.eus/WebServicesBilbao/WSBilbao?s=ODPRESBICI&u=OPENDATA&r=CSV&p0=A&p1=A"
        pass

    def getZonas(self):
        listadoBicis=[]
        bilbaoCSV = requests.get(self.bilbaoURL)
        estaciones = bilbaoCSV.text.split('\r\n')

        for i in range(1,32):
            listadoBicis.append(self._crearZona(estaciones[i]))


        return listadoBicis
    def _crearZona(self,estacion):
        temp = estacion.split(';')
        return {
            'anclajes_averiados':temp[0],
            'anclajes_libres': temp[1],
            'anclajes_usados': temp[2],
            'bicis_libres': temp[3],
            'bicis_averiadas': temp[4],
            'estado': temp[5],
            'id': temp[6],
            'lat': temp[7],
            'long': temp[8],
            'nombre': temp[9],
        }




if __name__ == '__main__':
    bicis = bicisApi()
    zonas = bicis.getZonas()
    print(zonas[3]['anclajes_averiados'])


