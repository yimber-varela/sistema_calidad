from flask import Blueprint, request, jsonify
from models import conectar_db
from datetime import datetime

test_plan_bp = Blueprint('test_plan', __name__)

# 🟩 Obtener todas las inspecciones del test plan
@test_plan_bp.route('/test_plan', methods=['GET'])
def obtener_test_plan():
    con = conectar_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM test_plan")
    filas = cur.fetchall()
    con.close()

    columnas = ['id', 'activity_nr', 'block', 'section', 'scope', 'responsible', 'kind', 'report', 'status']
    datos = [dict(zip(columnas, fila)) for fila in filas]
    return jsonify(datos), 200


# 🟨 Cargar inspecciones desde CSV u otro origen
@test_plan_bp.route('/test_plan', methods=['POST'])
def insertar_test_plan():
    data = request.get_json()
    con = conectar_db()
    cur = con.cursor()

    for item in data:
        cur.execute('''
            INSERT INTO test_plan (activity_nr, block, section, scope, responsible, kind, report, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            item.get("activity_nr"),
            item.get("block"),
            item.get("section"),
            item.get("scope"),
            item.get("responsible"),
            item.get("kind"),
            item.get("report"),
            item.get("status", "not defined")
        ))

    con.commit()
    con.close()
    return jsonify({"mensaje": "Inspecciones del test plan cargadas"}), 201


# 🗑️ Eliminar y mover a papelera
@test_plan_bp.route('/test_plan', methods=['DELETE'])
def eliminar_test_plan():
    data = request.get_json()
    ids = data.get("ids", [])
    if not ids:
        return jsonify({"error": "No se enviaron IDs"}), 400

    con = conectar_db()
    cur = con.cursor()

    for id in ids:
        cur.execute("SELECT * FROM test_plan WHERE id = ?", (id,))
        fila = cur.fetchone()
        if fila:
            cur.execute('''
                INSERT INTO papelera_inspecciones (id, titulo, descripcion, estado, fecha_eliminado)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                fila[0],
                f"Plan for {fila[1]}",
                f"{fila[5]} - {fila[6]}",
                fila[8],
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))
            cur.execute("DELETE FROM test_plan WHERE id = ?", (id,))

    con.commit()
    con.close()
    return jsonify({"mensaje": "Inspecciones movidas a la papelera"}), 200


# 🔄 Actualizar estado desde reportes.html por 'rep'
@test_plan_bp.route('/test_plan/status', methods=['PUT'])
def actualizar_estado_test_plan():
    data = request.get_json()
    rep = data.get("rep")
    status = data.get("status")

    if not rep or not status:
        return jsonify({"error": "Se requiere 'rep' y 'status'"}), 400

    con = conectar_db()
    cur = con.cursor()
    cur.execute("UPDATE test_plan SET status = ? WHERE report = ?", (status, rep))
    con.commit()
    con.close()

    return jsonify({"mensaje": "✅ Estado actualizado en test_plan"}), 200


# 🆕 🔁 Actualizar múltiples filas a 'not started' desde test_plan.html
@test_plan_bp.route('/test_plan/status/batch', methods=['PUT'])
def actualizar_estado_batch():
    data = request.get_json()
    if not isinstance(data, list):
        return jsonify({"error": "Se esperaba una lista de objetos con id y status"}), 400

    con = conectar_db()
    cur = con.cursor()

    for item in data:
        id_ = item.get("id")
        status = item.get("status", "not started")
        if id_:
            cur.execute("UPDATE test_plan SET status = ? WHERE id = ?", (status, id_))

    con.commit()
    con.close()
    return jsonify({"mensaje": "✅ Estados actualizados correctamente"}), 200

