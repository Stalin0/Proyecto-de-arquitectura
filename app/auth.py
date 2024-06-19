from functools import wraps
from flask import session, flash, redirect, url_for
from app.db import get_db_connection

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Verificar si el usuario está autenticado y es administrador
        if 'email' in session:
            email = session['email']
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM usuario WHERE email = %s", (email,))
            usuario = cur.fetchone()
            conn.close()

            if usuario and usuario[5] == 'Administrador':  # usuario[5] es el índice de 'user_type'
                return func(*args, **kwargs)
        
        flash('Acceso no autorizado.', 'danger')
        return redirect(url_for('index'))
    
    return wrapper

# Función para requerir que el usuario sea creador de cursos
def creator_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Verificar si el usuario está autenticado y es creador de cursos
        if 'email' in session:
            email = session['email']
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM usuario WHERE email = %s", (email,))
            usuario = cur.fetchone()
            conn.close()

            if usuario and usuario[5] == 'Creador de Cursos':  # Ajustado a 'Creador de Cursos'
                return func(*args, **kwargs)
        
        flash('Acceso no autorizado.', 'danger')
        return redirect(url_for('index'))
    
    return wrapper