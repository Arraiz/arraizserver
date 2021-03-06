from flask import Flask,jsonify
import playas_api
PORT = 8080
TEMPLATES_FOLDER = 'templates'

app = Flask(__name__, template_folder=TEMPLATES_FOLDER)
app.config['SERVER_NAME'] = 'arraiz.eus'
api=playas_api.PlayasApi()

@app.route('/')
@app.route('/<name>')
def hello(name='desconocido'):
    return 'que hace aqui pirata '+name


@app.route('/signalvisualizer/download')
def donwload():
    return 'proximamente'


# subdomains
# enigma
@app.route('/', subdomain='enigma')
def enigmaRoute():
    return 'en este subdominio tambien lo es... eskerrik asko'


# subdomains
# juegos
@app.route('/', subdomain='juegos')
def juegosRoute():
    return 'no disponible'


@app.route('/', subdomain="api")
def homeapi():
    return 'Bienvenido a la API no oficial de playas de bizkaia todo esto gracias al aburrimiento de Mikel Diez Garcia (Arraiz)'

@app.route('/getPlayas', subdomain="api")
def getPlayas():
    playas = api.GetPlayasList()
    return jsonify(playas)

@app.route('/get<id>', subdomain="api")
def getPlaya(id):
    unaPlaya = api.playaDetail(int(id))
    return jsonify(unaPlaya)


if __name__ == '__main__':
    app.run(port=PORT, host='0.0.0.0', debug=True)









