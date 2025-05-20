from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
import os
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    os.makedirs(os.path.join(app.root_path, 'static', 'uploads'), exist_ok=True)


    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app.auth.routes import auth as auth_blueprint
    from app.style_transfer.routes import style_transfer as style_transfer_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(style_transfer_blueprint)

    return app