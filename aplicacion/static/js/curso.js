document.addEventListener("DOMContentLoaded", () => {

    const botones = document.querySelectorAll(".cargar-contenido");
    const panel = document.getElementById("panel-dinamico");

    botones.forEach(boton => {
        boton.addEventListener("click", e => {
            e.preventDefault();

            const url = boton.getAttribute("data-url");

            fetch(url)
                .then(response => response.text())
                .then(html => {
                    panel.innerHTML = html;
                    panel.scrollTop = 0;
                });
        });
    });

});

document.addEventListener("DOMContentLoaded", () => {
    const panel = document.getElementById("panel-dinamico");
    const url = panel.dataset.inicialUrl;

    fetch(url)
        .then(r => r.text())
        .then(html => panel.innerHTML = html);
});

document.addEventListener("click", function (e) {
    if (e.target.classList.contains("cargar-contenido")) {

        // Quitar selección anterior
        document.querySelectorAll(".sidebar-link").forEach(link => {
            link.classList.remove("active-link");
        });

        // Marcar el nuevo como seleccionado
        e.target.classList.add("active-link");
    }
});

document.addEventListener("submit", function (e) {
    if (e.target.id === "cuestionarioForm") {
        e.preventDefault();

        let form = e.target;
        let url = form.dataset.url;
        let formData = new FormData(form);

        fetch(url, {
            method: "POST",
            headers: {
                "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
            },
            body: formData,
        })
        .then(r => r.json())
        .then(data => {

            if (data.success) {

                alert("Cuestionario enviado correctamente.");

                // marcar como completado en sidebar
                const sec = form.dataset.section;
                const estado = document.getElementById(`estado-${sec}`);
                if (estado) estado.classList.add("completado");
            }
        });
    }
});

// ===============================
//  ENVÍO AJAX DEL CUESTIONARIO
// ===============================
document.addEventListener("submit", function (e) {

    const form = e.target;
    if (form.id !== "cuestionarioForm") return; // no es el cuestionario

    e.preventDefault();

    const url = form.dataset.urlGuardar;
    const formData = new FormData(form);

    fetch(url, {
        method: "POST",
        body: formData
    })
        .then(res => res.json())
        .then(data => {

            // Ya respondido anteriormente
            if (data.ya_respondido) {
                mostrarMensaje("Ya habías respondido este cuestionario.", "warning");
                return;
            }

            if (data.success) {
                mostrarMensaje("✔ Respuestas guardadas correctamente", "success");

                // Marcar en el sidebar
                const section = form.dataset.section;
                const estadoSpan = document.getElementById(`estado-${section}`);
                if (estadoSpan) estadoSpan.classList.add("completado");
            }
        })
        .catch(() => {
            mostrarMensaje("Ocurrió un error al guardar.", "danger");
        });
});


// ===============================
//  SISTEMA DE MENSAJES
// ===============================
function mostrarMensaje(texto, tipo = "success") {
    const panel = document.getElementById("panel-dinamico");

    const box = document.createElement("div");
    box.className = `alert alert-${tipo}`;
    box.style.fontWeight = "600";
    box.style.borderRadius = "8px";
    box.style.marginBottom = "15px";
    box.innerText = texto;

    panel.prepend(box);

    setTimeout(() => box.remove(), 4000);
}

// --- GUARDAR CUESTIONARIO (AJAX) ---
document.addEventListener("submit", function (e) {
    const form = e.target;
    if (form.id !== "cuestionarioForm") return;

    e.preventDefault();

    const url = form.dataset.urlGuardar;
    const section = form.dataset.section;
    const btn = document.getElementById("btnEnviar");

    // Bloquear botón
    btn.disabled = true;
    btn.innerText = "Guardando...";

    const formData = new FormData(form);

    fetch(url, {
        method: "POST",
        body: formData,
        headers: {
            "X-Requested-With": "XMLHttpRequest"
        }
    })
    .then(res => res.json())
    .then(data => {

        // Ya había respondido
        if (data.ya_respondido) {
            mostrarMensaje("Ya respondiste este cuestionario.", "warning");
            btn.disabled = true;
            btn.innerText = "Enviado";
            return;
        }

        if (data.success) {
            mostrarMensaje("✔ Respuestas guardadas correctamente.", "success");

            // Mostrar el puntaje si quieres
            // mostrarMensaje(`Obtuviste ${data.puntaje} / ${data.total}`, "info");

            // marcar como completado en sidebar
            const estado = document.getElementById(`estado-${section}`);
            if (estado) estado.classList.add("completado");

            // bloquear el formulario para evitar cambios
            form.querySelectorAll("input").forEach(i => i.disabled = true);

            // cambiar botón
            btn.classList.remove("btn-success");
            btn.classList.add("btn-secondary");
            btn.innerText = "Respuestas enviadas";
            btn.disabled = true;
        }
    })
    .catch(err => {
        console.error("ERROR:", err);
        mostrarMensaje("Ocurrió un error al enviar.", "danger");
        btn.disabled = false;
        btn.innerText = "Enviar respuestas";
    });
});

function mostrarMensaje(texto, tipo = "info") {
    const div = document.createElement("div");
    div.className = `alert alert-${tipo}`;
    div.style.marginTop = "10px";
    div.innerHTML = texto;

    const contenedor = document.querySelector(".ajax-cuestionario");
    contenedor.prepend(div);

    setTimeout(() => div.remove(), 5000);
}


