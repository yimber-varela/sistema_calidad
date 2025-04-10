from flask import Blueprint, request, jsonify
from models import conectar_db
from datetime import datetime

inspecciones_bp = Blueprint('inspecciones', __name__)

# 📋 Crear o listar inspecciones antiguas
@inspecciones_bp.route('/inspecciones', methods=['GET', 'POST'])
def gestionar_inspecciones():
    con = conectar_db()
    cur = con.cursor()

    if request.method == 'POST':
        data = request.get_json()
        titulo = data.get('titulo')
        descripcion = data.get('descripcion')
        estado = data.get('estado', 'pendiente')

        if not titulo:
            return jsonify({"error": "El título es obligatorio"}), 400

        cur.execute('''
            INSERT INTO inspecciones (titulo, descripcion, estado)
            VALUES (?, ?, ?)
        ''', (titulo, descripcion, estado))

        con.commit()
        con.close()
        return jsonify({"mensaje": "Inspección registrada correctamente"}), 201

    elif request.method == 'GET':
        cur.execute("SELECT id, titulo, descripcion, estado FROM inspecciones")
        filas = cur.fetchall()
        con.close()

        inspecciones = []
        for fila in filas:
            inspecciones.append({
                "id": fila[0],
                "titulo": fila[1],
                "descripcion": fila[2],
                "estado": fila[3]
            })

        return jsonify(inspecciones), 200


# 🧩 Obtener datos del test plan (usado por test_plan.html)
@inspecciones_bp.route('/test_plan', methods=['GET'])
def obtener_test_plan():
    con = conectar_db()
    cur = con.cursor()
    cur.execute('''
        SELECT id, activity_nr, block, section, scope, responsible, kind, report, status
        FROM test_plan
    ''')
    filas = cur.fetchall()
    con.close()

    resultado = []
    for fila in filas:
        resultado.append({
            "id": fila[0],
            "activity_nr": fila[1],
            "block": fila[2],
            "section": fila[3],
            "scope": fila[4],
            "responsible": fila[5],
            "kind": fila[6],
            "report": fila[7],
            "status": fila[8]
        })

    return jsonify(resultado), 200

# ✅ Guardar inspecciones en curso (para inspecciones.html)
@inspecciones_bp.route('/inspecciones_en_curso', methods=['POST'])
def guardar_inspecciones_en_curso():
    data = request.get_json()
    if not data or not isinstance(data, list):
        return jsonify({"error": "Se esperaba una lista de inspecciones"}), 400

    con = conectar_db()
    cur = con.cursor()

    cur.execute("DELETE FROM inspecciones_en_curso")

    for item in data:
        cur.execute('''
            INSERT INTO inspecciones_en_curso (
                act, rep, block, section, scope, kind,
                email, date, time, meeting, additional_info
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            item.get('act'),
            item.get('rep'),
            item.get('block'),
            item.get('section'),
            item.get('scope'),
            item.get('kind'),
            item.get('email') or 'pending@qa.com',
            item.get('date') or datetime.now().strftime("%Y-%m-%d"),
            item.get('time') or datetime.now().strftime("%H:%M"),
            item.get('meeting') or '',
            item.get('additional_info') or ''
        ))

    con.commit()
    con.close()
    return jsonify({"mensaje": "Inspecciones en curso guardadas correctamente"}), 201

# ✅ Obtener inspecciones en curso
@inspecciones_bp.route('/inspecciones_en_curso', methods=['GET'])
def listar_inspecciones_en_curso():
    con = conectar_db()
    cur = con.cursor()
    cur.execute('''
        SELECT id, act, rep, block, section, scope, kind, email, date, time, meeting, additional_info
        FROM inspecciones_en_curso
    ''')
    filas = cur.fetchall()
    con.close()

    resultado = []
    for fila in filas:
        resultado.append({
            "id": fila[0],
            "act": fila[1],
            "rep": fila[2],
            "block": fila[3],
            "section": fila[4],
            "scope": fila[5],
            "kind": fila[6],
            "email": fila[7],
            "date": fila[8],
            "time": fila[9],
            "meeting": fila[10],
            "additional_info": fila[11]
        })

    return jsonify(resultado), 200

# ✅ Borrar inspecciones en curso
@inspecciones_bp.route('/inspecciones_en_curso', methods=['DELETE'])
def eliminar_inspecciones_en_curso():
    con = conectar_db()
    cur = con.cursor()
    cur.execute("DELETE FROM inspecciones_en_curso")
    con.commit()
    con.close()
    return jsonify({"mensaje": "Inspecciones en curso eliminadas correctamente"}), 200









