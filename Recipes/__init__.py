from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Initialize SQLAlchemy and Bcrypt extensions (not yet associated with any Flask app).
db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app(config_name=None):
    """
    Create an instance of the Flask application.
    """
    app = Flask(__name__)

    # A secret key for signing session cookies
    app.config["SECRET_KEY"] = "93220d9b340cf9a6c39bac99cce7daf220167498f91fa"

    # Application configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqldb://24_webapp_031:dGlvdf65@mysql.lab.it.uc3m.es/24_webapp_031c"
    # Uncomment the following line to use MySQL
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db.init_app(app)

    # Login manager.
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # User loader for login management
    from . import model
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(model.User, int(user_id))

    # Register blueprints
    from . import main, auth, explore
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(explore.bp)

    return app