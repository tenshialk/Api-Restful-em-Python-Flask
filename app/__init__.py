from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # aplica as configurações
    # Desativa ordenação alfabética das chaves JSON
    app.json.sort_keys = False

    db.init_app(app)  # associa o SQLAlchemy à aplicação Flask
    ma.init_app(app)
    migrate.init_app(app, db)

    from .routes.messages import messages_bp
    app.register_blueprint(messages_bp, url_prefix="/messages")
    
    with app.app_context():
        from app.models.usuario import Usuario
        from app.models.message import Message
        db.create_all()

    return app