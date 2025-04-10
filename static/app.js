// 🔐 Verificación de sesión para páginas protegidas
document.addEventListener("DOMContentLoaded", async () => {
  const paginaActual = window.location.pathname;
  const paginasProtegidas = [
    "/home.html",
    "/inspecciones.html",
    "/reportes.html",
    "/request_summary.html",
    "/test_plan.html",
    "/preview_report.html",
    "/quality_issues.html",
    "/inspections_ongoing.html",
    "/quality_progress.html"
  ];

  if (paginasProtegidas.includes(paginaActual)) {
    try {
      const res = await fetch("/api/verificar_sesion", {
        credentials: "include"
      });
      const data = await res.json();

      if (!res.ok || !data.autenticado) {
        alert("Access denied. Please log in.");
        window.location.href = "login.html";
      }
    } catch (err) {
      console.error("Error verifying session:", err);
      alert("Error verifying session. Please log in.");
      window.location.href = "login.html";
    }
  }
});

// 🔐 LOGIN
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("form-login");

  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();

      const nombre = document.getElementById("nombre").value;
      const contraseña = document.getElementById("contraseña").value;

      const res = await fetch("/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ nombre, contraseña }),
      });

      const data = await res.json();

      if (res.ok) {
        window.location.href = "home.html";
      } else {
        document.getElementById("mensaje-error").innerText = data.error;
      }
    });
  }
});

// 📝 REGISTRO
document.addEventListener("DOMContentLoaded", () => {
  const formRegistro = document.getElementById("form-registro");

  if (formRegistro) {
    formRegistro.addEventListener("submit", async (e) => {
      e.preventDefault();

      const nombre = document.getElementById("nombre").value;
      const contraseña = document.getElementById("contraseña").value;
      const clave = document.getElementById("clave").value;

      const res = await fetch("/api/registro", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ nombre, contraseña, clave }),
      });

      const data = await res.json();

      if (res.ok) {
        document.getElementById("mensaje-registro").style.color = "green";
        document.getElementById("mensaje-registro").innerText = "Successful registration. You can now log in.";
      } else {
        document.getElementById("mensaje-registro").innerText = data.error;
      }
    });
  }
});




