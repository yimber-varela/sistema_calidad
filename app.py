from flask import Flask, session
from flask import Flask, render_template
from flask_cors import CORS
import os

# Crear la instancia de la app Flask
app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

# Configurar la clave secreta para sesiones
app.secret_key = "clave_super_secreta_123"  # Cámbiala en producción

# Permitir CORS y habilitar credenciales (para que funcionen las cookies)
CORS(app, supports_credentials=True)

# Importar y registrar blueprints (rutas)
from routes.inspecciones import inspecciones_bp
from routes.login import login_bp
from routes.reportes import reportes_bp
from routes.solicitudes import solicitudes_bp
from routes.quality_issues import quality_issues_bp
from routes.papelera import papelera_bp
from routes.test_plan import test_plan_bp
from routes.reporte_editado import reporte_editado_bp

# Registro de Blueprints
app.register_blueprint(inspecciones_bp, url_prefix="/api")
app.register_blueprint(login_bp, url_prefix="/api")
app.register_blueprint(reportes_bp, url_prefix="/api")
app.register_blueprint(solicitudes_bp, url_prefix="/api")
app.register_blueprint(quality_issues_bp, url_prefix="/api")
app.register_blueprint(papelera_bp, url_prefix="/api")
app.register_blueprint(test_plan_bp, url_prefix="/api")
app.register_blueprint(reporte_editado_bp, url_prefix="/api")

# Punto de entrada principal
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)




