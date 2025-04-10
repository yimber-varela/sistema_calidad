from flask import Blueprint, request, jsonify, session, redirect, render_template
from models import conectar_db

# 🔐 Clave maestra para permitir registros
CLAVE_SECRETA = "registro2025"

login_bp = Blueprint('login', __name__)

# 🧾 Registro de usuario vía API con JSON (mantener)
@login_bp.route('/registro', methods=['POST'])
def registrar_usuario():
    data = request.get_json()
    nombre = data.get('nombre')
    contraseña = data.get('contraseña')
    clave = data.get('clave')

    if not nombre or not contraseña or not clave:
        return jsonify({"error": "Faltan datos"}), 400

    if clave != CLAVE_SECRETA:
        return jsonify({"error": "Clave secreta incorrecta"}), 403

    con = conectar_db()
    cur = con.cursor()

    cur.execute("SELECT * FROM usuarios WHERE nombre = ?", (nombre,))
    existente = cur.fetchone()
    if existente:
        con.close()
        return jsonify({"error": "El usuario ya existe"}), 409

    cur.execute("INSERT INTO usuarios (nombre, contraseña) VALUES (?, ?)", (nombre, contraseña))
    con.commit()
    con.close()

    return jsonify({"mensaje": "Usuario registrado correctamente"}), 201


# 🔐 Login clásico desde formulario HTML (no JSON)
@login_bp.route('/login', methods=['POST'])
def iniciar_sesion():
    nombre = request.form.get('usuario')
    contraseña = request.form.get('contraseña')

    if not nombre or not contraseña:
        return "Faltan datos", 400

    con = conectar_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM usuarios WHERE nombre = ? AND contraseña = ?", (nombre, contraseña))
    usuario = cur.fetchone()
    con.close()

    if usuario:
        session["usuario"] = nombre
        return redirect("/home")  # redirige a la página principal
    else:
        return render_template("login.html", error="Usuario o contraseña incorrectos")


# ✅ Verificar si hay sesión activa
@login_bp.route('/verificar_sesion', methods=['GET'])
def verificar_sesion():
    if "usuario" in session:
        return jsonify({"autenticado": True, "usuario": session["usuario"]}), 200
    else:
        return jsonify({"autenticado": False}), 401


# 🚪 Cerrar sesión
@login_bp.route('/logout', methods=['POST'])
def cerrar_sesion():
    session.pop("usuario", None)
    return jsonify({"mensaje": "Sesión cerrada correctamente"}), 200



