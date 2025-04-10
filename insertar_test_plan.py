import sqlite3

def insertar_test_plan():
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()

    datos = [
        ("A001", "100", "101", "Doors", "JT Constr.", "Visual", "R001", "Not started"),
        ("A002", "200", "201", "Walls", "JT Constr.", "Dimensional", "R002", "In progress"),
        ("A003", "300", "301", "Ceilings", "JT Constr.", "Visual", "R003", "Not applicable"),
        ("A004", "400", "401", "Floors", "ACME Ltd.", "Load Test", "R004", "Done")
    ]

    for d in datos:
        cur.execute('''
            INSERT INTO test_plan (activity_nr, block, section, scope, responsible, kind, report, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', d)

    con.commit()
    con.close()
    print("✅ Datos de prueba insertados en test_plan")

if __name__ == "__main__":
    insertar_test_plan()
