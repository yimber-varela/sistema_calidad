from flask import Blueprint, request, jsonify
from models import conectar_db
from datetime import datetime

quality_issues_bp = Blueprint('quality_issues', __name__)

# 🧾 Listar o crear quality issues
@quality_issues_bp.route('/issues', methods=['GET', 'POST'])
def gestionar_issues():
    con = conectar_db()
    cur = con.cursor()

    if request.method == 'POST':
        data = request.get_json()

        for item in data:
            # Obtener un número único para issue_nr
            cur.execute("SELECT COUNT(*) FROM quality_issues")
            total = cur.fetchone()[0] + 1
            issue_nr = f"Issue-{total:04d}"

            cur.execute('''
                INSERT INTO quality_issues (
                    issue_nr, rep_nr, activity_nr, date, description, system, email, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                issue_nr,
                item.get("rep_nr"),
                item.get("activity_nr"),
                item.get("date"),
                item.get("description"),
                item.get("system"),
                item.get("email"),
                item.get("status", "OPEN")
            ))

        con.commit()
        con.close()
        return jsonify({"mensaje": "✅ Issues registrados correctamente"}), 201

    elif request.method == 'GET':
        cur.execute('''
            SELECT id, issue_nr, rep_nr, activity_nr, date, description, system, email, status
            FROM quality_issues
        ''')
        filas = cur.fetchall()
        con.close()

        resultado = []
        for fila in filas:
            resultado.append({
                "id": fila[0],
                "issue_nr": fila[1],
                "rep_nr": fila[2],
                "activity_nr": fila[3],
                "date": fila[4],
                "description": fila[5],
                "system": fila[6],
                "email": fila[7],
                "status": fila[8]
            })

        return jsonify(resultado), 200


# 🔄 Actualizar estado del issue (OPEN/CLOSE)
@quality_issues_bp.route('/issues/<int:issue_id>', methods=['PUT'])
def actualizar_estado_issue(issue_id):
    data = request.get_json()
    nuevo_estado = data.get("status")

    if nuevo_estado not in ["OPEN", "CLOSE"]:
        return jsonify({"error": "Estado inválido. Debe ser 'OPEN' o 'CLOSE'"}), 400

    con = conectar_db()
    cur = con.cursor()

    cur.execute("UPDATE quality_issues SET status = ? WHERE id = ?", (nuevo_estado, issue_id))

    con.commit()
    con.close()
    return jsonify({"mensaje": f"Estado del issue actualizado a {nuevo_estado}"}), 200

