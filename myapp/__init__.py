from flask import Flask
from flask_admin import Admin
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_manager


admin = Admin(template_mode='bootstrap4')
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'user.login'



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    admin.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from myapp.main.routes import main
    from myapp.scraper.routes import scraper
    from myapp.user.routes import user

    app.register_blueprint(main)
    app.register_blueprint(scraper)
    app.register_blueprint(user)

    from myapp.admin import myadmin
    app.register_blueprint(myadmin)

    return app