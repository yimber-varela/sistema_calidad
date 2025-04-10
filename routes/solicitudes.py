from flask import Blueprint, request, jsonify
from models import conectar_db
from datetime import datetime

solicitudes_bp = Blueprint('solicitudes', __name__)

# 📥 GET: obtener todas | POST: insertar o agrupar solicitudes
@solicitudes_bp.route('/solicitudes', methods=['GET', 'POST'])
def gestionar_solicitudes():
    con = conectar_db()
    cur = con.cursor()

    if request.method == 'POST':
        data = request.get_json()
        if not data or not isinstance(data, list):
            return jsonify({"error": "Formato inválido. Se esperaba una lista de solicitudes."}), 400

        # Si ya contienen ID es porque solo se están agrupando
        es_actualizacion = all('id' in item for item in data)

        if es_actualizacion:
            grupo_id = datetime.now().timestamp()
            for item in data:
                cur.execute("UPDATE solicitudes SET grupo_envio = ? WHERE id = ?", (grupo_id, item['id']))
            con.commit()
            con.close()
            return jsonify({"mensaje": "Solicitudes agrupadas correctamente", "grupo_envio": grupo_id}), 200

        # Si vienen nuevas solicitudes
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cur.execute("INSERT INTO grupos_envio (fecha_envio) VALUES (?)", (timestamp,))
        grupo_id = cur.lastrowid

        for item in data:
            cur.execute('''
                INSERT INTO solicitudes (
                    act, rep, block, section, scope, email, kind, date, time, meeting, additional_info, grupo_envio
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                item.get('act'),
                item.get('rep'),
                item.get('block'),
                item.get('section'),
                item.get('scope'),
                item.get('email'),
                item.get('kind'),
                item.get('date'),
                item.get('time'),
                item.get('meeting'),
                item.get('additional_info'),
                grupo_id
            ))

            cur.execute('''
                INSERT INTO reportes (rep, act, request, date, scope, kind, status, issued)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                item.get('rep'),
                item.get('act'),
                1,
                item.get('date'),
                item.get('scope'),
                item.get('kind'),
                'not started',
                0
            ))

            cur.execute('''
                INSERT INTO quality_issues (issue_nr, rep_nr, activity_nr, date, description, system, email, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                f"ISSUE-{item.get('rep')}-{item.get('act')}",
                item.get('rep'),
                item.get('act'),
                item.get('date'),
                "Pending quality review",
                item.get('scope'),
                item.get('email'),
                "OPEN"
            ))

        con.commit()
        con.close()
        return jsonify({"mensaje": "Solicitudes, reportes e issues guardados correctamente", "grupo_envio": grupo_id}), 201

    elif request.method == 'GET':
        cur.execute('''
            SELECT id, act, rep, block, section, scope, email, kind, date, time, meeting, additional_info, grupo_envio
            FROM solicitudes
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
                "email": fila[6],
                "kind": fila[7],
                "date": fila[8],
                "time": fila[9],
                "meeting": fila[10],
                "additional_info": fila[11],
                "grupo_envio": fila[12]
            })

        return jsonify(resultado), 200


# ✅ NUEVO: guardar inspecciones marcadas desde test_plan.html
@solicitudes_bp.route('/solicitudes/marcadas', methods=['POST'])
def guardar_inspecciones_marcadas():
    data = request.get_json()
    if not data or not isinstance(data, list):
        return jsonify({"error": "Formato inválido"}), 400

    con = conectar_db()
    cur = con.cursor()

    # Limpiar tabla antes de agregar nuevas
    cur.execute("DELETE FROM inspecciones_marcadas")

    for item in data:
        cur.execute('''
            INSERT INTO inspecciones_marcadas (act, rep, block, section, scope, responsible, kind, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            item.get('act'),
            item.get('rep'),
            item.get('block'),
            item.get('section'),
            item.get('scope'),
            item.get('responsible'),
            item.get('kind'),
            'not started'  # 👈 Siempre establecer como punto de partida
        ))

        # 🔄 ACTUALIZAR también test_plan: status = 'not started'
        cur.execute("UPDATE test_plan SET status = 'not started' WHERE report = ?", (item.get('rep'),))

    con.commit()
    con.close()
    return jsonify({"mensaje": "Inspecciones marcadas guardadas correctamente"}), 201



# ✅ NUEVO: obtener inspecciones marcadas
@solicitudes_bp.route('/solicitudes/marcadas', methods=['GET'])
def obtener_inspecciones_marcadas():
    con = conectar_db()
    cur = con.cursor()
    cur.execute('SELECT * FROM inspecciones_marcadas')
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
            "responsible": fila[6],
            "kind": fila[7],
            "status": fila[8]
        })

    return jsonify(resultado), 200


# ✅ NUEVO: eliminar inspecciones marcadas (cuando se envían oficialmente)
@solicitudes_bp.route('/solicitudes/marcadas', methods=['DELETE'])
def eliminar_inspecciones_marcadas():
    con = conectar_db()
    cur = con.cursor()
    cur.execute("DELETE FROM inspecciones_marcadas")
    con.commit()
    con.close()
    return jsonify({"mensaje": "Inspecciones marcadas eliminadas"}), 200


# 🗑️ DELETE: Eliminar solicitudes seleccionadas y mover a papelera
@solicitudes_bp.route('/solicitudes', methods=['DELETE'])
def eliminar_solicitudes():
    data = request.get_json()
    ids = data.get("ids", [])

    if not ids:
        return jsonify({"error": "No se enviaron IDs para eliminar"}), 400

    con = conectar_db()
    cur = con.cursor()

    for id in ids:
        cur.execute("SELECT * FROM solicitudes WHERE id = ?", (id,))
        fila = cur.fetchone()
        if fila:
            cur.execute('''
                INSERT INTO papelera_inspecciones (id, titulo, descripcion, estado, fecha_eliminado)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                fila[0],
                f"Solicitud {fila[1]}",
                f"{fila[3]} - {fila[4]}",
                "pendiente",
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))
            cur.execute("DELETE FROM solicitudes WHERE id = ?", (id,))

    con.commit()
    con.close()
    return jsonify({"mensaje": "Inspecciones eliminadas correctamente"}), 200






