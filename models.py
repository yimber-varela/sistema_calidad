import sqlite3

# 🔌 Conexión a la base de datos
def conectar_db():
    return sqlite3.connect("db.sqlite3")

# 🏗️ Crear tablas si no existen
def crear_tablas():
    con = conectar_db()
    cur = con.cursor()

    # Tabla de usuarios
    cur.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            contraseña TEXT NOT NULL
        )
    ''')

    # Tabla de inspecciones
    cur.execute('''
        CREATE TABLE IF NOT EXISTS inspecciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            estado TEXT DEFAULT 'pendiente'
        )
    ''')

    # 🗑️ Papelera de inspecciones
    cur.execute('''
        CREATE TABLE IF NOT EXISTS papelera_inspecciones (
            id INTEGER PRIMARY KEY,
            titulo TEXT,
            descripcion TEXT,
            estado TEXT,
            fecha_eliminado TEXT
        )
    ''')

    # Tabla de reportes
    cur.execute('''
        CREATE TABLE IF NOT EXISTS reportes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rep TEXT NOT NULL,
            act TEXT NOT NULL,
            request INTEGER DEFAULT 0,
            date TEXT NOT NULL,
            scope TEXT NOT NULL,
            kind TEXT NOT NULL,
            status TEXT DEFAULT 'In progress',
            issued INTEGER DEFAULT 0
        )
    ''')

    # 🗑️ Papelera de reportes
    cur.execute('''
        CREATE TABLE IF NOT EXISTS papelera_reportes (
            id INTEGER PRIMARY KEY,
            rep TEXT,
            act TEXT,
            request INTEGER,
            date TEXT,
            scope TEXT,
            kind TEXT,
            status TEXT,
            fecha_eliminado TEXT
        )
    ''')

    # Tabla del test plan
    cur.execute('''
        CREATE TABLE IF NOT EXISTS test_plan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            activity_nr TEXT NOT NULL,
            block TEXT NOT NULL,
            section TEXT NOT NULL,
            scope TEXT NOT NULL,
            responsible TEXT NOT NULL,
            kind TEXT NOT NULL,
            report TEXT,
            status TEXT
        )
    ''')


    # ✅ Tabla de grupos de envío
    cur.execute('''
        CREATE TABLE IF NOT EXISTS grupos_envio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_envio TEXT NOT NULL
        )
    ''')

    # ✅ Tabla de solicitudes
    cur.execute('''
        CREATE TABLE IF NOT EXISTS solicitudes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            act TEXT,
            rep TEXT,
            block TEXT,
            section TEXT,
            scope TEXT,
            email TEXT,
            kind TEXT,
            date TEXT,
            time TEXT,
            meeting TEXT,
            additional_info TEXT,
            status TEXT,
            grupo_envio INTEGER,
            FOREIGN KEY (grupo_envio) REFERENCES grupos_envio(id)
        )
    ''')

    # ✅ NUEVA: Tabla de inspecciones marcadas desde test_plan (pre-envío)
    cur.execute('''
        CREATE TABLE IF NOT EXISTS inspecciones_marcadas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            act TEXT,
            rep TEXT,
            block TEXT,
            section TEXT,
            scope TEXT,
            responsible TEXT,
            kind TEXT,
            status TEXT
        )
    ''')

    # Tabla de quality issues
    cur.execute('''
        CREATE TABLE IF NOT EXISTS quality_issues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            issue_nr TEXT NOT NULL,
            rep_nr TEXT NOT NULL,
            activity_nr TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT NOT NULL,
            system TEXT NOT NULL,
            email TEXT NOT NULL,
            status TEXT DEFAULT 'Open'
        )
    ''')

    # Tabla de contenido de reportes
    cur.execute('''
        CREATE TABLE IF NOT EXISTS reportes_editados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rep TEXT UNIQUE,
            contenido TEXT
        )
    ''')
    
    # 🧩 Tabla para inspecciones en curso (desde test_plan hacia inspecciones.html)
    cur.execute('''
        CREATE TABLE IF NOT EXISTS inspecciones_en_curso (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            act TEXT,
            rep TEXT,
            block TEXT,
            section TEXT,
            scope TEXT,
            kind TEXT,
            email TEXT,
            date TEXT,
            time TEXT,
            meeting TEXT,
            additional_info TEXT
        )
    ''')

    con.commit()
    con.close()
    print("✅ Tablas creadas o actualizadas correctamente")

# Ejecutar si este archivo es el principal
if __name__ == "__main__":
    crear_tablas()







