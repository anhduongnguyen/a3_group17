from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from .utils import status_badge_class
import datetime

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.debug = True
    app.secret_key = '8D2E19734841292FF3DC76283B6E5'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sitedata.sqlite'
    app.jinja_env.filters['badge_class'] = status_badge_class


    db.init_app(app)
    Bcrypt(app)
    Bootstrap5(app)

    # Login manager setup
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'You need to be logged in to access this page.'
    login_manager.login_message_category = 'warning'

    from .models import User  # avoid duplicate
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))  # preferred over scalar+where

    # Register blueprints
    from . import views
    app.register_blueprint(views.main_bp)
    app.register_blueprint(views.event_bp)

    from . import auth
    app.register_blueprint(auth.auth_bp)

    # Context processors
    @app.context_processor
    def inject_year():
        return dict(year=datetime.datetime.today().year)

    @app.context_processor
    def price_formatting():
        def format_price(price):
            return f"${price:.2f}"
        return dict(format_price=format_price)
    
    return app
