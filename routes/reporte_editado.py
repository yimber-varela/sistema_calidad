from flask import Blueprint, request, jsonify
from models import conectar_db

reporte_editado_bp = Blueprint('reporte_editado', __name__)

# 🚀 Guardar contenido del reporte editado
@reporte_editado_bp.route('/reporte_editado/<string:rep>', methods=['POST'])
def guardar_reporte_editado(rep):
    data = request.get_json()
    contenido = data.get("contenido")

    if not contenido:
        return jsonify({"error": "Falta el contenido del reporte"}), 400

    con = conectar_db()
    cur = con.cursor()

    # Verificar si ya existe un contenido previo para ese reporte
    cur.execute("SELECT id FROM reportes_editados WHERE rep = ?", (rep,))
    existente = cur.fetchone()

    if existente:
        cur.execute("UPDATE reportes_editados SET contenido = ? WHERE rep = ?", (contenido, rep))
    else:
        cur.execute("INSERT INTO reportes_editados (rep, contenido) VALUES (?, ?)", (rep, contenido))

    con.commit()
    con.close()
    return jsonify({"mensaje": "✅ Reporte editado guardado correctamente"}), 200


# 📄 Obtener contenido del reporte editado
@reporte_editado_bp.route('/reporte_editado/<string:rep>', methods=['GET'])
def obtener_reporte_editado(rep):
    con = conectar_db()
    cur = con.cursor()
    cur.execute("SELECT contenido FROM reportes_editados WHERE rep = ?", (rep,))
    fila = cur.fetchone()
    con.close()

    if fila:
        return jsonify({"contenido": fila[0]}), 200
    else:
        return jsonify({"contenido": ""}), 200
