from flask import Flask, render_template, session
from flask_cors import CORS
import os

app = Flask(__name__)
app.secret_key = "clave_super_secreta_123"

app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True

CORS(app, supports_credentials=True)

# 🧩 RUTAS PARA SERVIR TUS PÁGINAS HTML
@app.route("/")
def ir_login():
    return render_template("login.html")

@app.route("/login.html")
def login_html():
    return render_template("login.html")

@app.route("/registro.html")
def registro_html():
    return render_template("registro.html")

@app.route("/home.html")
def home_html():
    return render_template("home.html")

@app.route("/test_plan.html")
def test_plan_html():
    return render_template("test_plan.html")

@app.route("/inspecciones.html")
def inspecciones_html():
    return render_template("inspecciones.html")

@app.route("/request_summary.html")
def request_summary_html():
    return render_template("request_summary.html")

@app.route("/reportes.html")
def reportes_html():
    return render_template("reportes.html")

@app.route("/quality_issues.html")
def quality_issues_html():
    return render_template("quality_issues.html")

@app.route("/papelera.html")
def papelera_html():
    return render_template("papelera.html")

@app.route("/editar_reporte.html")
def editar_reporte_html():
    return render_template("editar_reporte.html")

@app.route("/preview_report.html")
def preview_report_html():
    return render_template("preview_report.html")

@app.route("/inspections_ongoing.html")
def ongoing_html():
    return render_template("inspections_ongoing.html")

@app.route("/quality_progress.html")
def quality_progress_html():
    return render_template("quality_progress.html")

# ✅ RUTAS BACKEND
from routes.inspecciones import inspecciones_bp
from routes.login import login_bp
from routes.reportes import reportes_bp
from routes.solicitudes import solicitudes_bp
from routes.quality_issues import quality_issues_bp
from routes.papelera import papelera_bp
from routes.test_plan import test_plan_bp
from routes.reporte_editado import reporte_editado_bp

app.register_blueprint(inspecciones_bp, url_prefix="/api")
app.register_blueprint(login_bp, url_prefix="/api")
app.register_blueprint(reportes_bp, url_prefix="/api")
app.register_blueprint(solicitudes_bp, url_prefix="/api")
app.register_blueprint(quality_issues_bp, url_prefix="/api")
app.register_blueprint(papelera_bp, url_prefix="/api")
app.register_blueprint(test_plan_bp, url_prefix="/api")
app.register_blueprint(reporte_editado_bp, url_prefix="/api")

# 🟢 Ejecutar en entorno local o Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)







