from flask import Blueprint, render_template, request, redirect, url_for, flash
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
    libros = Libro.query.filter(Libro.cantidad_ejemplares > 0).all()
    usuarios = Usuario.query.all()
    if request.method == 'POST':
        libro = Libro.query.get_or_404(request.form['id_libro'])

        if libro.cantidad_ejemplares <= 0:
            return render_template('prestamos/agregar.html',
                                   libros=libros,
                                   usuarios=usuarios,
                                   error='No hay ejemplares disponibles de este libro.')

        prestamo = Prestamo(
            id_libro=libro.id,
            id_usuario=request.form['id_usuario'],
            fecha_prestamo=datetime.now(),
            fecha_vencimiento=datetime.strptime(request.form['fecha_vencimiento'], '%Y-%m-%d')
        )
        libro.cantidad_ejemplares -= 1
        db.session.add(prestamo)
        db.session.commit()
        flash('Préstamo registrado correctamente.', 'success')
        return redirect(url_for('prestamos.listar'))
    return render_template('prestamos/agregar.html', libros=libros, usuarios=usuarios, error=None)

@prestamos_bp.route('/devolver/<int:id>', methods=['POST'])
def devolver(id):
    prestamo = Prestamo.query.get_or_404(id)
    prestamo.fecha_devolucion = datetime.now()
    prestamo.libro.cantidad_ejemplares += 1
    db.session.commit()
    flash('Libro devuelto correctamente.', 'success')
    return redirect(url_for('prestamos.listar'))