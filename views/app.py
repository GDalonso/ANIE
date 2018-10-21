from flask import Flask, render_template, session, request
from flask_compress import Compress
import os

# Configura a aplicação, os diretorios de CSS, JS, Imagens e fontes
app = Flask(__name__, template_folder='../templates', static_folder='../static')
# Define uma chave para o HEROKU
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'WYZ')

# GZIP - Utilizado para compactar a pagina
gzip = Compress(app)

# Página de inicio
@app.route('/')
def index():
    if request.args.get('type_user') and not 'type_user' in session.keys():
        session['type_user'] = request.args.get('type_user')
    if 'type_user' in session.keys() and session['type_user'] == 'not_blind':
        return render_template('not_blind/index.html', titulo="Anie")
    elif 'type_user' in session.keys() and session['type_user'] == 'not_blind':
        return render_template('not_blind/index.html', titulo="Anie")

    return render_template('select_type.html', titulo="Anie")

if __name__ == '__main__':
    app.run()