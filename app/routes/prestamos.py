from flask import Blueprint, render_template, request, redirect, url_for
from app.extensions import db
from app.models.prestamo import Prestamo
from app.models.libro import Libro
from app.models.usuario import Usuario
from datetime import datetime

prestamos_bp = Blueprint('prestamos', __name__)

@prestamos_bp.route('/')
def listar():
    prestamos = Prestamo.query.filter_by(fecha_devolucion=None).all()
    return render_template('prestamos/listar.html', prestamos=prestamos)

@prestamos_bp.route('/agregar', methods=['GET', 'POST'])
def agregar():
    libros = Libro.query.all()
    usuarios = Usuario.query.all()
    if request.method == 'POST':
        prestamo = Prestamo(
            id_libro=request.form['id_libro'],
            id_usuario=request.form['id_usuario'],
            fecha_prestamo=datetime.now(),
            fecha_vencimiento=datetime.strptime(request.form['fecha_vencimiento'], '%Y-%m-%d')
        )
        db.session.add(prestamo)
        db.session.commit()
        return redirect(url_for('prestamos.listar'))
    return render_template('prestamos/agregar.html', libros=libros, usuarios=usuarios)

@prestamos_bp.route('/devolver/<int:id>', methods=['POST'])
def devolver(id):
    prestamo = Prestamo.query.get_or_404(id)
    prestamo.fecha_devolucion = datetime.now()
    db.session.commit()
    return redirect(url_for('prestamos.listar'))

libro = db.relationship('Libro', backref='prestamos')
usuario = db.relationship('Usuario', backref='prestamos')