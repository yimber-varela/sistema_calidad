from flask import Blueprint, request, jsonify
from models import conectar_db
from datetime import datetime, timedelta
import json

papelera_bp = Blueprint('papelera', __name__)

# 🗑️ Insertar en papelera (cuando se elimina algo)
def mover_a_papelera(tabla, contenido):
    con = conectar_db()
    cur = con.cursor()
    fecha_eliminacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cur.execute('''
        INSERT INTO papelera (tabla, contenido, fecha_eliminacion)
        VALUES (?, ?, ?)
    ''', (tabla, json.dumps(contenido), fecha_eliminacion))

    con.commit()
    con.close()

# 📥 Restaurar desde papelera
@papelera_bp.route('/papelera/restaurar/<int:item_id>', methods=['POST'])
def restaurar_item(item_id):
    con = conectar_db()
    cur = con.cursor()

    # Buscar el ítem en papelera
    cur.execute("SELECT tabla, contenido FROM papelera WHERE id = ?", (item_id,))
    fila = cur.fetchone()

    if not fila:
        con.close()
        return jsonify({"error": "Elemento no encontrado en la papelera"}), 404

    tabla, contenido = fila
    data = json.loads(contenido)

    if tabla == "inspecciones":
        cur.execute('''
            INSERT INTO inspecciones (titulo, descripcion, estado)
            VALUES (?, ?, ?)
        ''', (data["titulo"], data["descripcion"], data["estado"]))
    elif tabla == "reportes":
        cur.execute('''
            INSERT INTO reportes (rep, act, request, date, scope, kind, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (data["rep"], data["act"], data["request"], data["date"], data["scope"], data["kind"], data["status"]))
    else:
        con.close()
        return jsonify({"error": "Tipo de dato no soportado para restauración"}), 400

    # Eliminar de la papelera
    cur.execute("DELETE FROM papelera WHERE id = ?", (item_id,))
    con.commit()
    con.close()
    return jsonify({"mensaje": "Elemento restaurado correctamente"}), 200

# 🗂️ Ver contenido de la papelera
@papelera_bp.route('/papelera', methods=['GET'])
def ver_papelera():
    con = conectar_db()
    cur = con.cursor()
    cur.execute("SELECT id, tabla, contenido, fecha_eliminacion FROM papelera")
    filas = cur.fetchall()
    con.close()

    papelera = []
    for fila in filas:
        papelera.append({
            "id": fila[0],
            "tabla": fila[1],
            "contenido": json.loads(fila[2]),
            "fecha_eliminacion": fila[3]
        })
    return jsonify(papelera), 200

# 🧹 Limpiar elementos antiguos (más de 30 días)
@papelera_bp.route('/papelera/limpiar', methods=['DELETE'])
def limpiar_papelera():
    con = conectar_db()
    cur = con.cursor()

    hace_30_dias = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("DELETE FROM papelera WHERE fecha_eliminacion <= ?", (hace_30_dias,))
    
    con.commit()
    con.close()
    return jsonify({"mensaje": "Papelera limpiada"}), 200

