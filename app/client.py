from flask import render_template, request, redirect, url_for, jsonify, session
import json
import os
from app import app

# Product data for demonstration (static)
with open('app/products.json', 'r', encoding='utf-8') as file:
    PRODUCTS = json.load(file)

# File path for user data
USERS_FILE = 'app/users.json'

# Function to load users from the backend (JSON file)
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    return []

# Function to save users to the backend (JSON file)
def save_users(users):
    with open(USERS_FILE, 'w', encoding='utf-8') as file:
        json.dump(users, file, ensure_ascii=False, indent=4)

# API endpoint to get users
@app.route("/api/users", methods=["GET"])
def get_users():
    users = load_users()
    return jsonify(users)

# API endpoint to add a new user
@app.route("/api/users", methods=["POST"])
def create_user():
    new_user = request.json
    users = load_users()

    # Check if username already exists
    if any(user['username'] == new_user['username'] for user in users):
        return jsonify({"error": "Username already exists"}), 400

    # Add new user to the list
    users.append(new_user)
    save_users(users)
    return jsonify(new_user), 201

# Página inicial
@app.route("/")
def home():
    if 'username' in session:
        if session.get('profile') == 1:
            return redirect(url_for('home_loggedin'))
        elif session.get('profile') == 2:
            return redirect(url_for('home_admin'))
    return render_template('index.html')

# Página do usuário logado
@app.route("/user")
def home_loggedin():
    return render_template('index-logged.html')

# Página de admin
@app.route("/admin")
def home_admin():
    return render_template('index-admin.html')

# Página de login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        
        users = load_users()
        user = next((u for u in users if u['username'] == username and u['password'] == password), None)
        
        if user:
            session['username'] = username
            session['profile'] = user['profile']
            if user['profile'] == 1:
                return redirect(url_for('home_loggedin'))
            elif user['profile'] == 2:
                return redirect(url_for('home_admin'))
        else:
            return render_template('login.html', error="Usuário ou senha inválidos.")
    return render_template('login.html')

# Página de logout
@app.route("/logout")
def logout():
    session.pop('username', None)
    session.pop('profile', None)
    session.pop('cart', None)  # Limpa o carrinho
    return redirect(url_for('home'))

# Página de registro
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']
        
        if password != confirmPassword:
            return render_template('register.html', error="As senhas não coincidem.")
        
        users = load_users()
        if any(user['username'] == username for user in users):
            return render_template('register.html', error="Nome de usuário já existe.")
        
        new_user = {'username': username, 'password': password, 'profile': 1}  # Default profile is 'user'
        users.append(new_user)
        save_users(users)
        
        return redirect(url_for('login'))
    
    return render_template('register.html')

# Página de produto (exemplo estático)
@app.route("/product/<int:product_id>")
def product(product_id):
    # Encontra o produto pelo ID
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if not product:
        return redirect(url_for('home'))  # Redireciona caso o produto não exista
    
    return render_template('product.html', product=product)

# Página do carrinho de compras
@app.route("/cart")
def cart():
    # Recupera o carrinho da sessão
    cart = session.get('cart', [])
    return render_template('cart.html', cart=cart)

# Adicionar ao carrinho
@app.route("/add_to_cart/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    # Encontra o produto
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if not product:
        return redirect(url_for('home'))  # Redireciona caso o produto não exista
    
    # Recupera o carrinho da sessão
    cart = session.get('cart', [])
    
    # Verifica se o produto já está no carrinho
    existing_item = next((item for item in cart if item['id'] == product_id), None)
    if existing_item:
        existing_item['quantity'] += 1  # Aumenta a quantidade
    else:
        # Adiciona o produto com quantidade 1
        cart.append({'id': product_id, 'name': product['name'], 'price': product['price'], 'quantity': 1, 'image': product['image']})
    
    # Atualiza o carrinho na sessão
    session['cart'] = cart
    
    return redirect(url_for('cart'))  # Redireciona para a página do carrinho

# Página de catálogo
@app.route("/catalogo")
def catalogo():
    return render_template('catalogue.html', PRODUCTS=PRODUCTS)
