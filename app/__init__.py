from flask import Flask
from app.extensions import db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///biblioteca.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)

    app.secret_key = 'biblioteca_secret_key'

    from app.routes.libros import libros_bp
    app.register_blueprint(libros_bp, url_prefix='/libros')

    from app.routes.usuarios import usuarios_bp
    app.register_blueprint(usuarios_bp, url_prefix='/usuarios')
    from app.routes.prestamos import prestamos_bp
    app.register_blueprint(prestamos_bp, url_prefix='/prestamos')
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)
    from app.routes.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp)

    return app