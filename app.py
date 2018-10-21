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

        posts.append({'nomeImagem': 'img/about-img.jpg', 'textoImagem': 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.'})
        if 'type_user' in session.keys() and session['type_user'] == 'not_blind':
            #bancolista = dbretrieve()
            return render_template('not_blind/index.html', titulo="Anie", posts=posts)
        elif 'type_user' in session.keys() and session['type_user'] == 'blind':
            #bancolista = dbretrieve()
            return render_template('not_blind/index.html', titulo="Anie", posts=posts)

    return render_template('select_type.html', titulo="Anie")

if __name__ == '__main__':
    app.run()