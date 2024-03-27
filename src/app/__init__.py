from flask import Flask
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from app.api.v1.resources.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/api/v1/admin')

    return app
