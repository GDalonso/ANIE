# from flask import Flask, render_template, session, request
from flask_compress import Compress
import os
# from Database import dbretrieve, dblogaction, dbretrievepost, dbretrievecategoria, dbretrieveusuario
# from datetime import datetime
# from models import BlogPost, User
from flask import Flask, render_template, request, redirect, session, flash, url_for
from functools import wraps
from Database import dbinsert, dbretrieve, dbretrieveusuario, dbinsertusuario, dbretrievepost, dbretrievecategoria, \
    removepost, dblogaction, dbretrieveusers, removeuser
from werkzeug.security import check_password_hash
# from pprint import pprint
# from markdown import markdown
from models import BlogPost, User
from datetime import datetime

# Configura a aplicação, os diretorios de CSS, JS, Imagens e fontes
app = Flask(__name__, template_folder='templates', static_folder='static')
# Define uma chave para o HEROKU
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'WYZ')

# GZIP - Utilizado para compactar a pagina
gzip = Compress(app)

# Index page
@app.route('/')
def index():
    if request.args.get('type_user') and not 'type_user' in session.keys():
        session['type_user'] = request.args.get('type_user')
    if 'type_user' in session.keys() and session['type_user'] == 'not_blind':
        bancolista = dbretrieve()
        # todo DAR DISPLAY NO POST
        return render_template('not_blind/index.html', titulo="Anie")
    elif 'type_user' in session.keys() and session['type_user'] == 'blind':
        bancolista = dbretrieve()
        # todo DAR DISPLAY NO POST
        return render_template('not_blind/index.html', titulo="Anie")

    return render_template('select_type.html', titulo="Anie")

@app.route('/postagens')
def postlist():
        '''
        List all posts in the database to the manage posts screen
        '''

        dblogaction(
            {'Log': str(request), 'ip': request.remote_addr, 'time': datetime.now()})  # Log the action to the database

        if 'user_logged' not in session or session['user_logged'] == None:
            # Dynamic route to the login function
            return redirect(url_for('formlogin', proxima=url_for('index')))

        # Retrieve all posts from database
        bancolista = dbretrieve()
        return render_template('adminpostslist.html', titulo='Latest Posts', posts=bancolista)

@app.route('/post/<_postid>')
def postview(_postid: str):
    '''

    :param _postid: Post id in database
    :return: Render the post with given id to the user
    '''

    dblogaction({'Log': str(request), 'ip': request.remote_addr, 'time': datetime.now()}) #Log to the database

    post = dbretrievepost(_postid)
    local_post = BlogPost(nomePost=post['nomePost'], conteudoPost=post['conteudoPost'],
                descPost=post['descPost'], categoriaPost=post['categoriaPost'],
                imagemPost=post['imagemPost'], dataPost=post['dataPost'])
    #todo fix render template
    return render_template('postview.html', titulo=post['nomePost'], post=local_post)

@app.route('/categoria/<_category>')
def categorie(_category: str):
    '''

    :param _category: string name if a category
    :return: The categories view with the posts by that category
    '''

    dblogaction({'Log': str(request), 'ip': request.remote_addr, 'time': datetime.now()}) #Log action to the database

    postsincategory = dbretrievecategoria(_category)
    if postsincategory:
        return render_template('categorie.html', titulo=_category, posts=postsincategory)
    else:
        return render_template('notfound.html')

# Login related
@app.route('/login')
def formlogin():
    '''
    present to the user the login screen
    '''

    dblogaction({'Log': str(request), 'ip': request.remote_addr, 'time': datetime.now()}) #log the action to the database

    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

#Verify user password when logging in
def check_password(mongouser, password):
    return check_password_hash(mongouser['pw_hash'], password)

@app.route('/autenticar', methods=['POST', ])
def authenticatelogin():
    '''
    Verify the user and passwords inputed in the login page
    '''

    usuario = dbretrieveusuario(request.form['usuario'])

    if usuario:
        if check_password(usuario, request.form['senha']):
            session['user_logged'] = usuario["username"]
            flash(usuario["username"] + ' is now logged!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)

    # Show the error message if login fails
    flash('User or Passowrd incorrect, try again')
    return redirect(url_for('formlogin'))

@app.route('/logout')
def logout():
    '''
    Nullify the logged user
    '''

    session['user_logged'] = None
    flash('You need to log in to see this page!')
    return redirect(url_for('formlogin'))

@app.route('/novousuario')
def formcreateuser():
    '''
    Shows the new user creation screen to the user
    '''

    if 'user_logged' not in session or session['user_logged'] == None:
        # Dynamic route to the login function
        return redirect(url_for('formlogin', proxima=url_for('index')))
    return render_template('criausuario.html', titulo='Novo usuario')


@app.route('/criarusuario', methods=['POST',])
def createuser():
    '''
    Create a User with the create user form contents
    '''

    dblogaction({'Log': str(request), 'ip': request.remote_addr, 'time': datetime.now()}) #Log the action to the database

    # Form contents
    nomeusuario = request. form['nomeusuario']
    senha = request. form['senha']
    nomedisplay = request. form['nomedisplay']
    usuario = User(nomeusuario, nomedisplay, senha)

    # Insert the object converted to dict in the database
    dbinsertusuario(usuario.__dict__)

    # Dynamic route to the index function
    return redirect(url_for('index'))

#DELETE SHIT

@app.route('/remover/<_postid>')
def deletepost(_postid: str):
    '''
    Remove the post with the given id from the database
    :param _postid: Id of a post to be removed from database
    '''

    dblogaction({'Log': str(request), 'ip': request.remote_addr, 'time': datetime.now()}) # Log the action to the database

    if 'user_logged' not in session or session['user_logged'] == None:
        # Dynamic route to the login function
        return redirect(url_for('formlogin', proxima=url_for('index')))

    post = removepost(_postid)
    return postlist()

if __name__ == '__main__':
    app.run()