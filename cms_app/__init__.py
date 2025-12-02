from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from dotenv import load_dotenv  # added

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "main.login"
mail = Mail()

def create_app():
    load_dotenv()  # added so Railway/MySQL env vars load

    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from .routes import main
    app.register_blueprint(main)

    # init-db command
    @app.cli.command("init-db")
    def init_db():
        db.create_all()
        print("Database initialized.")

    # move user loader here, import User locally to avoid circular import
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
