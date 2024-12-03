from flask import Flask

app = Flask(__name__)

# Importa as rotas que estarão no arquivo routes.py
from app import client
