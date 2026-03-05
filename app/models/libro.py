from app import db

class Libro(db.Model):
    __tablename__ = 'libros'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    editorial = db.Column(db.String(100), nullable=False)
    anio_publicacion = db.Column(db.Integer, nullable=False)
    cantidad_ejemplares = db.Column(db.Integer, nullable=False)