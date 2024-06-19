import psycopg2
from app.db import get_db_connection

# Funciones para manejar usuarios
def crear_usuario(first_name, last_name, email, password, user_type):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO usuario (first_name, last_name, email, password, user_type) VALUES (%s, %s, %s, %s, %s)",
        (first_name, last_name, email, password, user_type)
    )
    conn.commit()
    conn.close()

def obtener_usuario_por_email(email):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM usuario WHERE email = %s", (email,))
    usuario = cur.fetchone()
    conn.close()
    return usuario

# Funciones para manejar cursos
def crear_curso(title, description, status, creator_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO curso (title, description, status, creator_id) VALUES (%s, %s, %s, %s)",
        (title, description, status, creator_id)
    )
    conn.commit()
    conn.close()

def obtener_cursos_por_creador(creator_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM curso WHERE creator_id = %s", (creator_id,))
    cursos = cur.fetchall()
    conn.close()
    return cursos

def obtener_todos_los_cursos():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM curso")
    cursos = cur.fetchall()
    conn.close()
    return cursos

def obtener_cursos_seleccionados(usuario_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT c.id, c.title, c.description, c.status, u.first_name || ' ' || u.last_name as creador
        FROM curso_seleccionado cs
        JOIN curso c ON cs.curso_id = c.id
        JOIN usuario u ON c.creator_id = u.id
        WHERE cs.usuario_id = %s
    """, (usuario_id,))
    cursos_seleccionados = cur.fetchall()
    conn.close()
    return cursos_seleccionados

def agregar_curso_seleccionado(usuario_id, curso_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO curso_seleccionado (usuario_id, curso_id) VALUES (%s, %s)",
        (usuario_id, curso_id)
    )
    conn.commit()
    conn.close()

def obtener_creador_de_curso(curso_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT creator_id FROM curso WHERE id = %s", (curso_id,))
    creador_id = cur.fetchone()[0]
    conn.close()
    return creador_id

def obtener_todos_los_usuarios():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM usuario")
    usuarios = cur.fetchall()
    conn.close()
    return usuarios
