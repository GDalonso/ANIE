from werkzeug.security import generate_password_hash as p_hash, check_password_hash as c_hash
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user
from .db_users import add_user, find_user
from .validations import validate_user, active_user
from .users import User

log_in = Blueprint('signin', __name__)

# Rota de cadastro
@log_in.route('/registrar')
def register():
    try:
        # Se existir um usuário logado, redireciona para o index
        if active_user():
            return redirect(url_for('index.index'))
    except:
        return render_template('signup.html', titulo='Sign up', imagem='imgs/signinup.jpg')

# Rota para autenticar o cadastro
@log_in.route('/novousuario', methods=['POST', 'GET'])
def new_user():
    # Recebe os dados do form
    name =  request.form['nome']
    username =  request.form['usuario']
    password = request.form['psw']
    confirm_password = request.form['password']
    email = request.form['email']
    # Verifica se o usuario e email já constam no banco de dados
    if not validate_user(username, email, password, confirm_password):
        # Se existir, retorna para a página de registro
        return render_template('signup.html', titulo='Sign up', imagem='imgs/signinup.jpg',
            username=username, email=email, name=name)
    # Faz o hash da senha
    password = p_hash(request.form['psw'], method='sha256') # Faz Hash da senha
    # Cria uma instancia do tipo User
    user = User(username, name, password, email, "user")
    # Armazena no MongoDB
    add_user(user.__dict__)
    # Apresenta mensagem para o usuário
    flash("Usuário cadastrado com sucesso!")
    # Redireciona para a tela de login
    return redirect(url_for('signin.login'))

# Rota de Login
@log_in.route('/entrar')
def login():
    try:
        # Se existir um usuário logado, redireciona para o index
        if active_user():
            return redirect(url_for('index.index'))
    except:
        # Recebe o valor da variavel proxima na URI
        next_page = request.args.get('proxima')
        # Determina a proxima página pós login
        return render_template('login.html', proxima=next_page, titulo='Sign in',
        imagem='imgs/signinup.jpg')

# Rota para autenticar o login
@log_in.route('/autenticar', methods=['POST',])
def autenticate():
    # Recebe o usuário do form
    user = request.form['usuario']
    # Busca o usuário no banco de dados caso ele exista
    user_database = find_user(user)
    # Se existir, tenta autenticar, se não, retorna mensagem de usuário invalido
    if user_database:
        # Compara a senha digitada com a do banco
        if c_hash(user_database['password'], request.form['senha']):
            # Cria uma instancia do tipo User para guardar na sessão do Flask_Login
            user_obj = User(user_database['_id'], user_database['name'], user_database['password'],
                user_database['email'], 'user')
            # Faz o Login do usuário
            login_user(user_obj)
            # Se a senha e usuário estiverem corretos, redireciona para o index
            return redirect(url_for('index.index'))
        else:
            flash("Senha inválida")
    else:
        flash("Username inválido")
    # Se a senha e usuário não estiverem corretos, redireciona para a página de login
    return redirect(url_for('signin.login'))

# Rota de logout
@log_in.route('/sair')
def logout():
    logout_user()
    return redirect(url_for('index.index'))