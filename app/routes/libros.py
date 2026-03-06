from flask import Blueprint, render_template, request, redirect, url_for
from app.extensions import db
from app.models.libro import Libro
libros_bp = Blueprint('libros', __name__)

@libros_bp.route('/')
def listar():
    libros = Libro.query.all()
    return render_template('libros/listar.html', libros=libros)