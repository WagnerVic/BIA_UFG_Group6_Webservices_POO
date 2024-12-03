from flask import render_template, request, redirect, url_for, jsonify, session
from app import app
import json
import os

# Caminho para o arquivo JSON onde os usuários serão armazenados
USERS_FILE = 'app/users.json'

# Função para carregar os usuários do arquivo JSON
def load_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r') as file:
                users = json.load(file)
                print(f"Usuários carregados: {users}")  # Imprime os usuários carregados
                return users
        except Exception as e:
            print(f"Erro ao carregar usuários do arquivo: {e}")
            return []
    print("Arquivo de usuários não encontrado, retornando lista vazia.")
    return []

# Função para salvar os usuários no arquivo JSON
def save_users(users):
    try:
        # Verifica se o diretório onde o arquivo está localizado existe
        if not os.path.exists(os.path.dirname(USERS_FILE)):
            os.makedirs(os.path.dirname(USERS_FILE))  # Cria o diretório, se necessário

        with open(USERS_FILE, 'w') as file:
            print(f"Salvando usuários: {users}")  # Imprime os usuários antes de salvar
            json.dump(users, file, indent=4)
            print(f"Usuários salvos com sucesso no arquivo {USERS_FILE}")
    except Exception as e:
        print(f"Erro ao salvar usuários: {e}")

# Página inicial
@app.route("/")
def home():
    if 'username' in session:
        # Redireciona para a página específica do perfil
        if session.get('profile') == 1:
            return redirect(url_for('home_loggedin'))  # Usuário comum
        elif session.get('profile') == 2:
            return redirect(url_for('home_admin'))  # Administrador
    return render_template('index.html')

# Página do usuário logado
@app.route("/user")
def home_loggedin():
    #if 'username' in session and session.get('profile') == 1:
        return render_template('index-logged.html')#, username=session['username'])
    #return redirect(url_for('login'))  # Se o usuário não estiver logado ou for admin, redireciona para login

# Página de admin
@app.route("/admin")
def home_admin():
    #if 'username' in session and session.get('profile') == 2:
        return render_template('index-admin.html')#, username=session['username'])
    #return redirect(url_for('login'))  # Se não for admin ou não estiver logado, redireciona para login

# Página de login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        
        # Carrega os usuários
        users = load_users()
        
        # Verifica se o usuário existe e se a senha está correta
        user = next((u for u in users if u['username'] == username), None)
        
        if user and user['password'] == password:  # Verifica se as senhas coincidem
            # Usuário autenticado, cria sessão e redireciona para home
            session['username'] = username  # Armazena o nome de usuário na sessão
            session['profile'] = user['profile']  # Armazena o perfil do usuário

            # Redireciona com base no perfil
            if user['profile'] == 1:
                return redirect(url_for('home_loggedin'))  # Redireciona para a página do usuário
            elif user['profile'] == 2:
                return redirect(url_for('home_admin'))  # Redireciona para a página do admin
        else:
            # Caso contrário, mostra a mensagem de erro
            return render_template('login.html', error="Usuário ou senha inválidos.")
    return render_template('login.html')


# Página de registro
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        # Define o perfil como 1 (usuário comum)
        profile = 1

        # Carrega os usuários
        users = load_users()

        # Verifica se o nome de usuário já existe
        if any(user['username'] == username for user in users):
            return render_template('register.html', error="Usuário já existe.")

        # Cria o novo usuário com a senha em texto simples (sem criptografia)
        new_user = {'username': username, 'password': password, 'profile': profile}
        
        users.append(new_user)
        
        # Salva os usuários atualizados no arquivo JSON
        save_users(users)

        return redirect(url_for('login'))  # Redireciona para a página de login

    return render_template('register.html')


# Verifica se o usuário está logado
@app.route("/loggedin")
def logged_in():
    if 'username' in session:
        return jsonify({"message": f"Usuário {session['username']} está logado."})
    else:
        return jsonify({"message": "Nenhum usuário está logado."}), 401

# Roteamento para logout
@app.route("/logout")
def logout():
    session.pop('username', None)  # Remove o usuário da sessão
    session.pop('profile', None)  # Remove o perfil do usuário
    return redirect(url_for('home'))  # Redireciona para a página inicial

# Endpoint para obter todos os usuários (API)
@app.route("/api/users", methods=["GET"])
def api_get_users():
    users = load_users()  # Carrega os usuários
    return jsonify(users)

# Endpoint para salvar ou atualizar os usuários (API)
@app.route("/api/users", methods=["PUT"])
def api_save_users():
    users = request.get_json()  # Obtém os dados enviados no corpo da requisição
    save_users(users)  # Salva os usuários no arquivo
    return jsonify({"message": "Usuários atualizados com sucesso!"}), 200

# Endpoint para exibir o carrinho de compras
@app.route("/cart")
def carrinho():
    return render_template('cart.html')

