from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# Inicializa la extensión SQLAlchemy, pero todavía no la asocia con ninguna aplicación.
db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app(config_name=None):
    """
    Crea una instancia de la aplicación Flask.
    """
    app = Flask(__name__)

    # A secret for signing session cookies
    app.config["SECRET_KEY"] = "93220d9b340cf9a6c39bac99cce7daf220167498f91fa"

    # Configuración de la aplicación.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    # Inicializa las extensiones
    db.init_app(app)

    # Register blueprints
    from . import main
    from . import auth

    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)

    return app