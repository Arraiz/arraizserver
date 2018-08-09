from flask import Flask,jsonify
import playas_api
# -*- coding: utf-8 -*-


PORT = 8080
TEMPLATES_FOLDER = 'templates'

app = Flask(__name__, template_folder=TEMPLATES_FOLDER)
app.config['JSON_AS_ASCII'] = False
api=playas_api.PlayasApi()



# subdomains


@app.route('/')
def homeapi():
    return 'Bienvenido a la API no oficial de playas de bizkaia todo esto gracias al aburrimiento de Mikel Diez Garcia (Arraiz)'

@app.route('/getPlayas')
def getPlayas():
    playas = api.GetPlayasList()
    return jsonify(playas)
@app.route('/get<id>')
def getPlaya(id):
    unaPlaya = api.playaDetail(int(id))
    return jsonify(unaPlaya)


if __name__ == '__main__':
    app.run(port=PORT, host='0.0.0.0', debug=True)









