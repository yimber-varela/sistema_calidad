from flask import Flask, render_template, session
from flask_cors import CORS
import os

# Crear instancia de la app
app = Flask(__name__)
app.secret_key = "clave_super_secreta_123"  # ¡Cambia esto en producción!

# Permitir cookies entre frontend y backend
CORS(app, supports_credentials=True)

# ========================
# 🔗 RUTAS PARA HTML (templates)
# ========================

@app.route('/')
def ruta_login():
    return render_template('login.html')

@app.route('/registro')
def ruta_registro():
    return render_template('registro.html')

@app.route('/home')
def ruta_home():
    return render_template('home.html')

@app.route('/test_plan')
def ruta_test_plan():
    return render_template('test_plan.html')

@app.route('/inspecciones')
def ruta_inspecciones():
    return render_template('inspecciones.html')

@app.route('/request_summary')
def ruta_request_summary():
    return render_template('request_summary.html')

@app.route('/reportes')
def ruta_reportes():
    return render_template('reportes.html')

@app.route('/quality_issues')
def ruta_quality_issues():
    return render_template('quality_issues.html')

@app.route('/papelera')
def ruta_papelera():
    return render_template('papelera.html')

@app.route('/editar_reporte')
def ruta_editar_reporte():
    return render_template('editar_reporte.html')

@app.route('/preview_report')
def ruta_preview_report():
    return render_template('preview_report.html')

@app.route('/inspections_ongoing')
def ruta_inspections_ongoing():
    return render_template('inspections_ongoing.html')

@app.route('/quality_progress')
def ruta_quality_progress():
    return render_template('quality_progress.html')


# ========================
# 📦 RUTAS BACKEND (API)
# ========================

from routes.inspecciones import inspecciones_bp
from routes.login import login_bp
from routes.reportes import reportes_bp
from routes.solicitudes import solicitudes_bp
from routes.quality_issues import quality_issues_bp
from routes.papelera import papelera_bp
from routes.test_plan import test_plan_bp
from routes.reporte_editado import reporte_editado_bp

# Registrar Blueprints API
app.register_blueprint(inspecciones_bp, url_prefix="/api")
app.register_blueprint(login_bp, url_prefix="/api")
app.register_blueprint(reportes_bp, url_prefix="/api")
app.register_blueprint(solicitudes_bp, url_prefix="/api")
app.register_blueprint(quality_issues_bp, url_prefix="/api")
app.register_blueprint(papelera_bp, url_prefix="/api")
app.register_blueprint(test_plan_bp, url_prefix="/api")
app.register_blueprint(reporte_editado_bp, url_prefix="/api")

# ========================
# 🚀 EJECUCIÓN PRINCIPAL
# ========================

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)






