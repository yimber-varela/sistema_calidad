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
    "/inspections_ongoing.html"
  ];

  if (paginasProtegidas.includes(paginaActual)) {
    try {
      const res = await fetch("http://localhost:5000/api/verificar_sesion", {
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

      const res = await fetch("http://localhost:5000/api/login", {
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

      const res = await fetch("http://localhost:5000/api/registro", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
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

// 📋 INSPECCIONES
document.addEventListener("DOMContentLoaded", () => {
  const formInspeccion = document.getElementById("form-inspeccion");

  if (formInspeccion) {
    formInspeccion.addEventListener("submit", async (e) => {
      e.preventDefault();
      const titulo = document.getElementById("titulo").value;
      const descripcion = document.getElementById("descripcion").value;

      const res = await fetch("http://localhost:5000/api/inspecciones", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ titulo, descripcion }),
      });

      const data = await res.json();

      if (res.ok) {
        document.getElementById("mensaje").innerText = "✅ Inspection registered.";
        formInspeccion.reset();
        cargarInspecciones();
      } else {
        document.getElementById("mensaje").innerText = "❌ Error registering inspection.";
      }
    });
  }

  async function cargarInspecciones() {
    const res = await fetch("http://localhost:5000/api/inspecciones", {
      credentials: "include"
    });
    const inspecciones = await res.json();

    const tbody = document.querySelector("#tabla-inspecciones tbody");
    if (!tbody) return;

    tbody.innerHTML = "";

    inspecciones.forEach((item) => {
      const fila = document.createElement("tr");
      fila.innerHTML = `
        <td>${item.id}</td>
        <td>${item.titulo}</td>
        <td>${item.descripcion}</td>
        <td>
          <select onchange="actualizarEstado(${item.id}, this.value)">
            <option value="pendiente" ${item.estado === "pendiente" ? "selected" : ""}>Pending</option>
            <option value="en ejecucion" ${item.estado === "en ejecucion" ? "selected" : ""}>In Progress</option>
            <option value="finalizado" ${item.estado === "finalizado" ? "selected" : ""}>Done</option>
          </select>
        </td>
      `;
      tbody.appendChild(fila);
    });
  }

  cargarInspecciones();
});

// ✅ Actualizar estado inspección
async function actualizarEstado(id, nuevoEstado) {
  const res = await fetch(`http://localhost:5000/api/inspecciones/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    body: JSON.stringify({ estado: nuevoEstado }),
  });

  if (res.ok) {
    console.log(`✅ Inspection ${id} updated to ${nuevoEstado}`);
  } else {
    alert("❌ Error updating status.");
  }
}

// 🔚 Cerrar sesión (puedes llamar esto desde un botón de logout)
async function cerrarSesion() {
  const res = await fetch("http://localhost:5000/api/logout", {
    method: "POST",
    credentials: "include"
  });

  if (res.ok) {
    window.location.href = "login.html";
  } else {
    alert("Error al cerrar sesión.");
  }
}



