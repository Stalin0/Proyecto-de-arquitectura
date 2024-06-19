from flask import render_template, request, redirect, url_for, flash, session
from app import app
from app.models import crear_curso, crear_usuario, obtener_usuario_por_email, obtener_todos_los_cursos, agregar_curso_seleccionado, obtener_cursos_seleccionados, obtener_todos_los_usuarios
from app.auth import creator_required, admin_required
from app.db import get_db_connection

@app.route('/')
def index():
    if 'email' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM usuario WHERE email = %s AND password = %s", (email, password))
    usuario = cur.fetchone()
    conn.close()

    if usuario:
        session['email'] = usuario[3]  # usuario[3] es el índice de 'email' en la tabla
        flash('Inicio de sesión exitoso', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('Credenciales incorrectas. Por favor, intenta de nuevo.', 'danger')
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('email', None)
    flash('Cierre de sesión exitoso', 'success')
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'email' not in session:
        return redirect(url_for('index'))

    email = session['email']
    usuario = obtener_usuario_por_email(email)


    #conn = get_db_connection()
    #cur = conn.cursor()
    #cur.execute("SELECT * FROM usuario WHERE email = %s", (email,))
    #usuario = cur.fetchone()
    #conn.close()

    if usuario[5] == 'Administrador':
        return render_template('admin_dashboard.html', usuario=usuario)
    elif usuario[5] == 'Creador de Cursos':
        return render_template('creator_dashboard.html', usuario=usuario)
    elif usuario[5] == 'Consumidor de Cursos':
        return render_template('consumer_dashboard.html', usuario=usuario)

@app.route('/admin_dashboard', methods=['GET', 'POST'])
@admin_required  # Asegura que solo los administradores puedan acceder
def admin_dashboard():
    email = 'admin@admin.com'  # Simular el email del administrador (puedes modificar según necesites)

    if request.method == 'POST':
        # Procesar el formulario para registrar nuevo usuario
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        user_type = request.form['user_type']

        # Validar que el usuario que se está registrando no sea administrador
        if user_type == 'Administrador':
            flash('Solo los administradores pueden registrar usuarios como administradores.', 'danger')
        else:
            crear_usuario(first_name, last_name, email, password, user_type)
            flash('Registro de usuario exitoso.', 'success')

    # Obtener todos los usuarios para mostrar en la página
    usuarios = obtener_todos_los_usuarios()

    return render_template('admin_dashboard.html', email=email, usuarios=usuarios)

@app.route('/usuarios')
@admin_required
def ver_usuarios():
    usuarios = obtener_todos_los_usuarios()
    return render_template('usuarios.html', usuarios=usuarios)

@app.route('/creator_dashboard', methods=['GET', 'POST'])
@creator_required
def creator_dashboard():
    email = session['email']
    usuario = obtener_usuario_por_email(email)

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        status = request.form['status']
        creator_id = usuario[0]  # Suponiendo que el ID del usuario está en la primera posición

        crear_curso(title, description, status, creator_id)

        flash('El curso ha sido creado exitosamente.', 'success')
        return redirect(url_for('creator_dashboard'))

    return render_template('creator_dashboard.html', usuario=usuario)

@app.route('/consumer_dashboard')
def consumer_dashboard():
    email = session['email']
    usuario = obtener_usuario_por_email(email)
    cursos = obtener_todos_los_cursos()
    return render_template('consumer_dashboard.html', usuario=usuario, cursos=cursos)

@app.route('/select_course', methods=['POST'])
def select_course():
    curso_id = request.form.get('curso_id')
    if not curso_id:
        flash('Debes seleccionar un curso.', 'danger')
        return redirect(url_for('consumer_dashboard'))

    email = session['email']
    usuario = obtener_usuario_por_email(email)
    agregar_curso_seleccionado(usuario[0], curso_id)  # Suponiendo que el ID del usuario está en la primera posición
    flash('El curso ha sido seleccionado exitosamente.', 'success')
    return redirect(url_for('consumer_dashboard'))

@app.route('/selected_courses')
def selected_courses():
    email = session['email']
    usuario = obtener_usuario_por_email(email)
    cursos_seleccionados = obtener_cursos_seleccionados(usuario[0])  # Suponiendo que el ID del usuario está en la primera posición
    return render_template('selected_courses.html', usuario=usuario, cursos_seleccionados=cursos_seleccionados)