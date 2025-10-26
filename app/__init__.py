from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_mail import Mail
from dotenv import load_dotenv
import os

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
mail = Mail()  # ← sem to patrí globálne

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    load_dotenv()

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['MAIL_SERVER'] = 'sandbox.smtp.mailtrap.io'
    app.config['MAIL_PORT'] = 2525
    app.config['MAIL_USERNAME'] = '74567f09f8aeab'
    app.config['MAIL_PASSWORD'] = 'dcd799dc1d03db'
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_DEFAULT_SENDER'] = ('Expense App Alerts', 'noreply@budgetapp.local')

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)  # ← inicializácia tu, nie vytváranie

    from . import models
    from app.models import User

    with app.app_context():
        db.create_all()

    login_manager.login_view = 'auth.login'

    from .auth import auth_bp
    from .expenses import expenses_bp
    from .budgets import budgets_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(expenses_bp)
    app.register_blueprint(budgets_bp)

    @app.route('/')
    def index():
        from flask import render_template
        return render_template('index.html')

    return app
