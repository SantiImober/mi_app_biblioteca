from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.extensions import db
from app.models.usuario import Usuario
from app.models.prestamo import Prestamo

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/')
def listar():
    usuarios = Usuario.query.all()
    return render_template('usuarios/listar.html', usuarios=usuarios)

@usuarios_bp.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        usuario = Usuario(
            nombre=request.form['nombre'],
            apellido=request.form['apellido'],
            direccion=request.form['direccion'],
            telefono=request.form['telefono']
        )
        db.session.add(usuario)
        db.session.commit()
        flash('Usuario agregado correctamente.', 'success')
        return redirect(url_for('usuarios.listar'))
    return render_template('usuarios/agregar.html')

@usuarios_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    usuario = Usuario.query.get_or_404(id)
    if request.method == 'POST':
        usuario.nombre = request.form['nombre']
        usuario.apellido = request.form['apellido']
        usuario.direccion = request.form['direccion']
        usuario.telefono = request.form['telefono']
        db.session.commit()
        flash('Usuario actualizado correctamente.', 'success')
        return redirect(url_for('usuarios.listar'))
    return render_template('usuarios/editar.html', usuario=usuario)

@usuarios_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    usuario = Usuario.query.get_or_404(id)
    if any(p.fecha_devolucion is None for p in usuario.prestamos):
        flash('No podés eliminar un usuario con préstamos activos.', 'error')
        return redirect(url_for('usuarios.listar'))
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuario eliminado correctamente.', 'success')
    return redirect(url_for('usuarios.listar'))