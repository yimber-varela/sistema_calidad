import sqlite3

con = sqlite3.connect("db.sqlite3")
cur = con.cursor()

cur.execute("DELETE FROM solicitudes")
con.commit()
con.close()

print("✅ Tabla 'solicitudes' vaciada.")
