from flask import Blueprint, request, jsonify
from models import conectar_db
from datetime import datetime

reportes_bp = Blueprint('reportes', __name__)

# 📄 Obtener todos o crear nuevo reporte
@reportes_bp.route('/reportes', methods=['GET', 'POST'])
def gestionar_reportes():
    con = conectar_db()
    cur = con.cursor()

    if request.method == 'POST':
        data = request.get_json()

        rep = data.get("rep")
        act = data.get("act")
        request_inspection = data.get("request", False)
        date = data.get("date")
        scope = data.get("scope")
        kind = data.get("kind")
        status = data.get("status", "In progress")

        if not rep or not act or not date or not scope or not kind:
            return jsonify({"error": "Faltan campos requeridos"}), 400

        cur.execute('''
            INSERT INTO reportes (rep, act, request, date, scope, kind, status, issued)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (rep, act, int(request_inspection), date, scope, kind, status, 0))

        con.commit()
        con.close()
        return jsonify({"mensaje": "✅ Reporte creado correctamente"}), 201

    elif request.method == 'GET':
        cur.execute('SELECT id, rep, act, request, date, scope, kind, status, issued FROM reportes')
        filas = cur.fetchall()
        con.close()

        reportes = []
        for fila in filas:
            reportes.append({
                "id": fila[0],
                "rep": fila[1],
                "act": fila[2],
                "request": bool(fila[3]),
                "date": fila[4],
                "scope": fila[5],
                "kind": fila[6],
                "status": fila[7],
                "issued": bool(fila[8])
            })

        return jsonify(reportes), 200


# 📝 Actualizar estado del reporte
@reportes_bp.route('/reportes/<int:reporte_id>', methods=['PUT'])
def actualizar_estado_reporte(reporte_id):
    data = request.get_json()
    nuevo_estado = data.get("status")

    if not nuevo_estado:
        return jsonify({"error": "Estado no proporcionado"}), 400

    con = conectar_db()
    cur = con.cursor()
    cur.execute("UPDATE reportes SET status = ? WHERE id = ?", (nuevo_estado, reporte_id))
    con.commit()
    con.close()
    return jsonify({"mensaje": "Estado del reporte actualizado"}), 200


# ✅ Marcar como "Issued" cuando se genera PDF
@reportes_bp.route('/reportes/<int:reporte_id>/emitido', methods=['PUT'])
def marcar_emitido(reporte_id):
    con = conectar_db()
    cur = con.cursor()
    cur.execute("UPDATE reportes SET issued = 1 WHERE id = ?", (reporte_id,))
    con.commit()
    con.close()
    return jsonify({"mensaje": "Reporte marcado como emitido"}), 200


# 🗑️ Eliminar múltiples reportes y mover a papelera
@reportes_bp.route('/reportes', methods=['DELETE'])
def eliminar_reportes():
    data = request.get_json()
    ids = data.get("ids", [])

    if not ids:
        return jsonify({"error": "No se enviaron IDs para eliminar"}), 400

    con = conectar_db()
    cur = con.cursor()

    for rid in ids:
        cur.execute("SELECT * FROM reportes WHERE id = ?", (rid,))
        fila = cur.fetchone()
        if fila:
            cur.execute('''
                INSERT INTO papelera_reportes (id, rep, act, request, date, scope, kind, status, fecha_eliminado)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                fila[0], fila[1], fila[2], fila[3], fila[4], fila[5], fila[6], fila[7],
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))
            cur.execute("DELETE FROM reportes WHERE id = ?", (rid,))

    con.commit()
    con.close()
    return jsonify({"mensaje": "🗑️ Reportes eliminados correctamente"}), 200


# 📂 Guardar contenido del reporte
@reportes_bp.route('/reportes/contenido/<string:rep>', methods=['POST'])
def guardar_contenido_reporte(rep):
    data = request.get_json()
    contenido = data.get("contenido", "")

    con = conectar_db()
    cur = con.cursor()

    cur.execute("SELECT COUNT(*) FROM reporte_contenido WHERE rep = ?", (rep,))
    existe = cur.fetchone()[0]

    if existe:
        cur.execute("UPDATE reporte_contenido SET contenido = ? WHERE rep = ?", (contenido, rep))
    else:
        cur.execute("INSERT INTO reporte_contenido (rep, contenido) VALUES (?, ?)", (rep, contenido))

    con.commit()
    con.close()
    return jsonify({"mensaje": "✅ Contenido guardado"}), 200


# 📄 Obtener contenido por REP
@reportes_bp.route('/reportes/contenido/<string:rep>', methods=['GET'])
def obtener_contenido_por_rep(rep):
    con = conectar_db()
    cur = con.cursor()

    cur.execute("SELECT contenido FROM reporte_contenido WHERE rep = ?", (rep,))
    fila = cur.fetchone()
    con.close()

    if fila:
        return jsonify({"contenido": fila[0]}), 200
    else:
        return jsonify({"contenido": ""}), 200


# 🔍 Obtener HTML de previsualización por ID
@reportes_bp.route('/reportes/contenido/<int:reporte_id>', methods=['GET'])
def obtener_contenido_preview_html(reporte_id):
    con = conectar_db()
    cur = con.cursor()
    cur.execute("SELECT contenido FROM reportes_html WHERE id = ?", (reporte_id,))
    fila = cur.fetchone()
    con.close()

    if fila:
        return jsonify({"contenido": fila[0]}), 200
    else:
        return jsonify({"error": "Contenido no encontrado"}), 404





