from flask import Flask

# Inicializa o aplicativo Flask
app = Flask(__name__)

# Importa as rotas
from app.client import *

if __name__ == "__main__":
    app.run(debug=True)
