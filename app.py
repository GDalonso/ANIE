from flask import Flask, render_template, session, request
from flask_compress import Compress
import os
from PIL import Image

from Database import dbretrieve

# Configura a aplicação, os diretorios de CSS, JS, Imagens e fontes
app = Flask(__name__, template_folder='templates', static_folder='static')
# Define uma chave para o HEROKU
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'WYZ')

# GZIP - Utilizado para compactar a pagina
gzip = Compress(app)

# Página de inicio
@app.route('/')
def index():
    posts = []
    if request.args.get('type_user') and not 'type_user' in session.keys():
        session['type_user'] = request.args.get('type_user')
    else:

        posts.append({'nomeImagem': 'img/about-img.jpg', 'textoImagem': 'gfg'})
        if 'type_user' in session.keys() and session['type_user'] == 'not_blind':
            #bancolista = dbretrieve()
            return render_template('not_blind/index.html', titulo="Anie")
        elif 'type_user' in session.keys() and session['type_user'] == 'blind':
            #bancolista = dbretrieve()
            return render_template('not_blind/index.html', titulo="Anie")

    return render_template('select_type.html', titulo="Anie", posts=posts)

if __name__ == '__main__':
    app.run()