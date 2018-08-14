import bs4 as bs
import requests
import js2py
import json
import asyncio
import pyowm

class PlayasApi:

    def __init__(self):
        # playas de bizkaia
        self.apiTiempo = owm = pyowm.OWM('f6748bc87ddf9c819dff7dc3060ced06')
        self._playasUrl = 'http://www.bizkaia.eus/Ingurugiroa_Lurraldea/Hondartzak/listadoplayas.asp?Tem_Codigo=350&idioma=CA&dpto_biz=2&codpath_biz=2|350'
        #esto deberia estar en una base de datos
        self.coordenadas_por_id={
            '1': [43.387837, -2.996004], #arrietara
            '2': [43.323418, -2.418899], #Arrigorri
            '3': [43.355344, -3.019137], #arrigunaga
            '4': [43.430436, -2.806984],#Bakio
            '5': [43.383383, -3.003901],#Barinatxe
            '6': [43.404563, -2.974155],#Barrika
            '7': [43.426173, -2.729596],#Aritzatxu
            '8': [43.432867, -2.892484],#Armintza
            '9': [43.385058, -2.583236],#Ea
            '10': [43.342507, -3.013517],#Ereaga
            '11': [43.418268, -2.945359],#Gorliz
            '12': [43.380476, -3.014484],#Gorrondatxe
            '13': [43.363833, -2.501934],#Isuntza
            '14': [43.382968, -2.680126],#Kanala
            '15': [43.381846164937, -2.67851829528809],#kanalape
            '16': [43.3628169481706, -2.49423980712891],#Karraspio
            '17': [43.349232, -3.115733], #La Arena
            '18': [43.409038, -2.659332],#Laga
            '19': [43.398937, -2.685233],#Laida
            '20': [43.4049851306295, -2.69937515258789],#laidatxu
            '21': [43.348507, -3.119675],#Las Arenas
            '22': [43.3951630640074, -2.98562049865723],#meñakoz
            '23': [43.373044, -2.545325],#ogella
            '24': [43.4112828877988, -2.94708251953125],#plentzia
            '25': [43.3865245658954, -2.68916130065918],#San Antonio
            '27': [43.3910778627597, -2.69182205200195],#Toña
            '29': [43.407335, -2.698322],#Hondartzape
            '30': [43.4130286847514, -2.95995712280273]#Muriola
        }
    def GetPlayasList(self):
        response = requests.get(self._playasUrl)

        paginaPlayas = bs.BeautifulSoup(response.content, 'html.parser')
        scriptPlayas = paginaPlayas.find('script', {'type': 'text/javascript'})

        # obatenemos el JS de su pagina y exportamos el objeto que contiene la info delas playas!!!
        context = js2py.EvalJs()
        js_code = scriptPlayas.getText()
        context.execute(js_code)
        ArrayPlayas = context.ArrayPlayas
        #Listado de las Playas
        listaPlayas = []

        # recorremos el array de playas
        for i in range(0, 28):
            playa = self._crearPlaya(ArrayPlayas[i * 11], ArrayPlayas[(i * 11) + 1], ArrayPlayas[(i * 11) + 2],
                                     ArrayPlayas[(i * 11) + 3], ArrayPlayas[(i * 11) + 4], ArrayPlayas[(i * 11) + 5])
            listaPlayas.append(playa)

        #al usar jsonify en flask no hace falta que convirtamos a json aqui
        playasJson = json.dumps(listaPlayas)
        return listaPlayas

    def _crearPlaya(self, id, nombre, bandera, viento, oleaje, temp_agua):
        return {
            'id': id,
            'nombre': nombre,
            'bandera': bandera,
            'viento': viento,
            'oleaje': oleaje,
            'temp_agua': temp_agua
        }

    def playaDetail(self, id):
        _url = 'http://www.bizkaia.eus/Ingurugiroa_Lurraldea/Hondartzak/detallePlaya.asp?nPlaya=' + str(
            id) + '&Tem_Codigo=350&Idioma=CA&banoAsistidoPulsado=0'
        playa_request = requests.get(_url)
        soup = bs.BeautifulSoup(playa_request.content, 'html.parser')
        # nombre playa
        cabecera = soup.find("div", {"id": "cabecera_detalle_playa"})
        nombre = cabecera.find("h4")

        _nombrePlaya = nombre.getText();
        #temporada baño
        tempBanio = soup.find('div', {'id': 'temporada_bano'})

        info = tempBanio.findAll('p')

        _temporadaBanio = info[0].getText()
        try:
            _horarioBanio = info[1].getText()[17:]
        except IndexError:
            _horarioBanio = 'None'
        ##pleamar
        pleamar = soup.find('div', {'class': 'caja_pleamar1 ico_pleamar'})

        _pleamar = pleamar.getText()[10:]
        ##bajamar
        bajamar = soup.find('div', {'class': 'caja_bajamar1 ico_bajamar'})

        _bajamar = bajamar.getText()[10:]
        ##socorristas
        servicios = soup.find('dl', {'id': 'servicios'})
        socorristas = servicios.find('dd', {'class': 'desc_item'})

        _socorristas = socorristas.getText()
        ##aparcamientos para discapacitados

        try:
            discapcitados = servicios.findAll('dd', {'class': 'desc_item_2lines'})
            _aparcamientosDiscapacitados = discapcitados[2].getText()
        except IndexError:
            _aparcamientosDiscapacitados = 'No disponible'

        ##a partir de la 11++ hay informacion diaria en la pagina
        infoDiaria = soup.find('div', {'id': 'info_diaria'})

        try:
            informaciones = infoDiaria.findAll('img', alt=True)
            _bandera = informaciones[0]['alt']
            _viento = informaciones[1]['alt']
            _oleaje = informaciones[2]['alt']
            _tempAgua = informaciones[3]['alt']
            _ocupacion = informaciones[4]['alt']
            _parking = informaciones[5]['alt']
        except Exception as e:
            _bandera = 'none'
            _viento = 'none'
            _oleaje = 'none'
            _tempAgua = 'none'
            _ocupacion = 'none'
            _parking = 'none'


        #aqui viene la asincronia necesitamos consultar varias apis en paralelo para obtener los datos
        observation = self.apiTiempo.three_hours_forecast_at_coords(self.coordenadas_por_id[str(id)][0],self.coordenadas_por_id[str(id)][1])
        w = observation.get_forecast()
        #el array tiene [hora y temperatura a es hora]
        _tempArray=[]
        for weather in w.get_weathers():
            auxArr=[weather.get_temperature(unit='celsius')['temp'],weather.get_reference_time('iso')[11:16]]
            _tempArray.append(auxArr)

        detail = {
            'nombre': _nombrePlaya,
            'temporada': _temporadaBanio,
            'horario': _horarioBanio,
            'pleamar': _pleamar,
            'bajamar': _bajamar,
            'socorristas': _socorristas,
            'aparcaminentos_discapacitados': _aparcamientosDiscapacitados,
            'bandera': _bandera,
            'viento': _viento,
            'oleaje': _oleaje,
            'temp_agua': _tempAgua,
            'ocupacion': _ocupacion,
            'parking': _parking,
            'id': id,
            'forecast':_tempArray,
            'coordenadas':self.coordenadas_por_id[str(id)]
        }
     #   detailJson = json.dumps(detail)
        return detail


# async def asyncInfo():
#     loop = asyncio.get_event_loop()
#     future1 = loop.run_in_executor(None, requests.get, 'http://www.google.com')
#     future2 = loop.run_in_executor(None, requests.get, 'http://www.google.co.uk')
#     response1 = await future1
#     response2 = await future2
#     print(response1.text)
#     print(response2.text)

if __name__ == '__main__':
    api = PlayasApi()
   # playas=api.GetPlayasList()
   # print(playas)
    playa=api.playaDetail(17)
    print(playa['coordenadas'])


# ids de playas problematicas
#la playa con index 29 no exite luego el rango de playas es 1-28 30
