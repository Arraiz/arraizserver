from flask import Flask


app = Flask(__name__)




@app.route('/', subdomain="juegos")
def juegos():
    return 'Phaser3 jolasak'

@app.route('/', subdomain="enigma")
def enigma():
    return 'Que sera'


@app.route('/')
def home():
    return 'Ongi etorri'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)