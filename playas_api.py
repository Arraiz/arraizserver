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
            '1': [43.3466729,-3.1202796],
            '2': [43.3466729,-3.1202796],
            '3': [43.3466729,-3.1202796],
            '4': [43.3466729,-3.1202796],
            '5': [43.3466729,-3.1202796],
            '6': [43.3466729,-3.1202796],
            '7': [43.3466729,-3.1202796],
            '8': [43.3466729,-3.1202796],
            '9': [43.3466729,-3.1202796],
            '10': [43.3466729,-3.1202796],
            '11': [43.3466729,-3.1202796],
            '12': [43.3466729,-3.1202796],
            '13': [43.3466729,-3.1202796],
            '14': [43.3466729,-3.1202796],
            '15': [43.3466729,-3.1202796],
            '16': [43.3466729,-3.1202796],
            '17': [43.3466729,-3.1202796],
            '18': [43.3466729,-3.1202796],
            '19': [43.3466729,-3.1202796],
            '20': [43.3466729,-3.1202796],
            '21': [43.3466729,-3.1202796],
            '22': [43.3466729,-3.1202796],
            '23': [43.3466729,-3.1202796],
            '24': [43.3466729,-3.1202796],
            '25': [43.3466729,-3.1202796],
            '26': [43.3466729,-3.1202796],
            '27': [43.3466729,-3.1202796],
            '28': [43.3466729,-3.1202796],
            '30': [43.3466729,-3.1202796]
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
        observation = self.apiTiempo.weather_at_coords(43.3466729,-3.1202796)
        w = observation.get_weather()
        temp=w.get_temperature('celsius')
        print(temp)

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
        }
     #   detailJson = json.dumps(detail)
        return detail


async def asyncInfo():
    loop = asyncio.get_event_loop()
    future1 = loop.run_in_executor(None, requests.get, 'http://www.google.com')
    future2 = loop.run_in_executor(None, requests.get, 'http://www.google.co.uk')
    response1 = await future1
    response2 = await future2
    print(response1.text)
    print(response2.text)

if __name__ == '__main__':
    api = PlayasApi()
   # playas=api.GetPlayasList()
   # print(playas)
    playa=api.playaDetail(30)
    print(playa)


# ids de playas problematicas
#la playa con index 29 no exite luego el rango de playas es 1-28 30
