from flask import Flask,jsonify,request
import playas_api
import bicis_api
# -*- coding: utf-8 -*-


PORT = 8080
TEMPLATES_FOLDER = 'templates'

app = Flask(__name__, template_folder=TEMPLATES_FOLDER)
app.config['JSON_AS_ASCII'] = False
apiPlayas=playas_api.PlayasApi()
apiBicis = bicis_api.bicisApi()
CONST_API_KEY_PLAYAS = 'thisisplayasapi'
CONST_API_KEY_BICIS = 'thisisbicisapi'






@app.route('/',methods=['GET'])
def homeapi():
    try:
        if(request.headers['X-Api-Key'] ==  CONST_API_KEY_PLAYAS):
            return 'Bienvenido a la API no oficial de playas de bizkaia todo esto gracias al aburrimiento de Mikel Diez Garcia (Arraiz)'
        elif (request.headers['X-Api-Key'] is not CONST_API_KEY_PLAYAS):
            return 'No deberias estar aqui pirata consulte con el admin :pexodeadmin:'
    except KeyError:
        return 'No deberias estar aqui pirata consulte con el admin :pexodeadmin:'


@app.route('/getPlayas',methods=['GET'])
def getPlayas():

    try:
        if(request.headers['X-Api-Key'] ==  CONST_API_KEY_PLAYAS):
            playas = apiPlayas.GetPlayasList()
            return jsonify(playas)
        elif (request.headers['X-Api-Key'] is not CONST_API_KEY_PLAYAS):
            return 'No deberias estar aqui pirata consulte con el admin :pexodeadmin:'
    except KeyError:
        return 'No deberias estar aqui pirata consulte con el admin :pexodeadmin:'


@app.route('/getBicis',methods=['GET'])
def getBicis():

    try:
        if(request.headers['X-Api-Key'] ==  CONST_API_KEY_BICIS):
            zonas = apiBicis.getZonas()
            return jsonify(zonas)
        elif (request.headers['X-Api-Key'] is not CONST_API_KEY_BICIS):
            return 'No deberias estar aqui pirata consulte con el admin :pexodeadmin:'
    except KeyError:
        return 'No deberias estar aqui pirata consulte con el admin :pexodeadmin:'


@app.route('/get<id>',methods=['GET'])
def getPlaya(id):
    try:
        if(request.headers['X-Api-Key'] ==  CONST_API_KEY_PLAYAS):
            unaPlaya = apiPlayas.playaDetail(int(id))
            return jsonify(unaPlaya)
        elif (request.headers['X-Api-Key'] is not CONST_API_KEY_PLAYAS):
            return 'No deberias estar aqui pirata consulte con el admin :pexodeadmin:'
    except KeyError:
        return 'No deberias estar aqui pirata consulte con el admin :pexodeadmin:'



if __name__ == '__main__':
    app.run(port=PORT, host='0.0.0.0', debug=True)









