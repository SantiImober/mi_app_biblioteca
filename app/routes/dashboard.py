from flask import Blueprint, render_template
from app.extensions import db
from app.models.libro import Libro
from app.models.usuario import Usuario
from app.models.prestamo import Prestamo
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
def index():
    total_libros = Libro.query.count()
    total_usuarios = Usuario.query.count()
    total_prestamos_activos = Prestamo.query.filter_by(fecha_devolucion=None).count()
    total_ejemplares = db.session.query(db.func.sum(Libro.cantidad_ejemplares)).scalar() or 0
    
    prestamos_vencidos = Prestamo.query.filter(
        Prestamo.fecha_devolucion == None,
        Prestamo.fecha_vencimiento < datetime.now()
    ).count()

    ultimos_prestamos = Prestamo.query.order_by(
        Prestamo.fecha_prestamo.desc()
    ).limit(5).all()

    return render_template('dashboard.html',
        total_libros=total_libros,
        total_usuarios=total_usuarios,
        total_prestamos_activos=total_prestamos_activos,
        total_ejemplares=total_ejemplares,
        prestamos_vencidos=prestamos_vencidos,
        ultimos_prestamos=ultimos_prestamos,
        now=datetime.now()
    )