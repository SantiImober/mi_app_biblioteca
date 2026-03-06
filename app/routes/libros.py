from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.extensions import db
from app.models.libro import Libro

libros_bp = Blueprint('libros', __name__)

@libros_bp.route('/')
def listar():
    libros = Libro.query.all()
    return render_template('libros/listar.html', libros=libros)

@libros_bp.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        existe = Libro.query.filter_by(
            titulo=request.form['titulo'],
            autor=request.form['autor']
        ).first()

        if existe:
            return render_template('libros/agregar.html',
                                   error='Ya existe un libro con ese título y autor.')

        libro = Libro(
            titulo=request.form['titulo'],
            autor=request.form['autor'],
            editorial=request.form['editorial'],
            anio_publicacion=request.form['anio_publicacion'],
            cantidad_ejemplares=request.form['cantidad_ejemplares']
        )
        db.session.add(libro)
        db.session.commit()
        flash('Libro agregado correctamente.', 'success')
        return redirect(url_for('libros.listar'))
    return render_template('libros/agregar.html', error=None)

@libros_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    libro = Libro.query.get_or_404(id)
    if libro.prestamos and any(p.fecha_devolucion is None for p in libro.prestamos):
        flash('No podés eliminar un libro con préstamos activos.', 'error')
        return redirect(url_for('libros.listar'))
    db.session.delete(libro)
    db.session.commit()
    flash('Libro eliminado correctamente.', 'success')
    return redirect(url_for('libros.listar'))

@libros_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    libro = Libro.query.get_or_404(id)
    if request.method == 'POST':
        libro.titulo = request.form['titulo']
        libro.autor = request.form['autor']
        libro.editorial = request.form['editorial']
        libro.anio_publicacion = request.form['anio_publicacion']
        libro.cantidad_ejemplares = request.form['cantidad_ejemplares']
        db.session.commit()
        flash('Libro actualizado correctamente.', 'success')
        return redirect(url_for('libros.listar'))
    return render_template('libros/editar.html', libro=libro)