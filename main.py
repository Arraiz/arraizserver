from flask import Flask


app = Flask(__name__)

@app.route('/')
def home():
    return 'Ongi etorri'

@app.route("/", subdomain="juegos")
def juegos():
    return 'Phaser3 jolasak'

@app.route("/", subdomain="enigma")
def juegos():
    return 'Que sera'




if __name__ == "__main__":
    app.run()