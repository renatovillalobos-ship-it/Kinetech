document.addEventListener("DOMContentLoaded", () => {
    inicializarAplicacion();
});

function inicializarAplicacion() {
    inicializarCargaContenido();
    inicializarCuestionario();
    inicializarNavegacion();
}

function inicializarCargaContenido() {
    const botones = document.querySelectorAll(".cargar-contenido");
    const panel = document.getElementById("panel-dinamico");

    if (!panel) return;

    // Cargar contenido inicial
    const urlInicial = panel.dataset.inicialUrl;
    if (urlInicial) {
        cargarContenido(urlInicial, panel);
    }

    botones.forEach(boton => {
        boton.addEventListener("click", e => {
            e.preventDefault();
            const url = boton.getAttribute("data-url");
            cargarContenido(url, panel);
            marcarActivo(boton);
        });
    });
}

function cargarContenido(url, panel) {
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error HTTP: ${response.status}`);
            }
            return response.text();
        })
        .then(html => {
            panel.innerHTML = html;
            panel.scrollTop = 0;
            
            if (html.includes('ajax-cuestionario')) {
                inicializarCuestionarioForm();
            }
        })
        .catch(error => {
            console.error("Error al cargar contenido:", error);
            mostrarMensaje("Error al cargar el contenido", "danger");
        });
}

function inicializarNavegacion() {
    document.addEventListener("click", function (e) {
        if (e.target.classList.contains("cargar-contenido")) {
            marcarActivo(e.target);
        }
    });
}

function marcarActivo(elemento) {
    document.querySelectorAll(".sidebar-link").forEach(link => {
        link.classList.remove("active-link");
    });

    elemento.classList.add("active-link");
}


function inicializarCuestionario() {
}

function inicializarCuestionarioForm() {
    const form = document.getElementById("cuestionarioForm");
    if (!form) return;

    const nuevoForm = form.cloneNode(true);
    form.parentNode.replaceChild(nuevoForm, form);

    document.getElementById("cuestionarioForm").addEventListener("submit", manejarEnvioCuestionario);
}

function manejarEnvioCuestionario(e) {
    e.preventDefault();
    
    const form = e.target;
    const urlGuardar = form.dataset.urlGuardar;
    const sectionId = form.dataset.section;
    const btn = document.getElementById("btnEnviar");

    // Validar que todas las preguntas estén respondidas
    if (!validarCuestionarioCompleto()) {
        mostrarMensajeCuestionario("⚠ Por favor responde todas las preguntas antes de enviar.", "warning");
        return;
    }

    // Bloquear botón durante el envío
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span> Enviando...';

    const formData = new FormData(form);

    fetch(urlGuardar, {
        method: "POST",
        body: formData,
        headers: {
            "X-Requested-With": "XMLHttpRequest"
        }
    })
    .then(res => {
        if (!res.ok) {
            throw new Error(`Error HTTP: ${res.status}`);
        }
        return res.json();
    })
    .then(data => {
        // Ya había respondido
        if (data.ya_respondido) {
            mostrarMensajeCuestionario("Ya respondiste este cuestionario", "warning");
            bloquearCuestionario(form, btn, "Enviado anteriormente");
            marcarComoCompletado(sectionId);
            return;
        }

        // Éxito al guardar
        if (data.success) {
            let mensajeHTML = `
                <div class="mb-2">
                    <h4 class="fw-bold mb-1">
                        Nivel de diagnóstico: ${data.texto_nivel}
                    </h4>
                    <p class="mb-0">
                        ${data.texto_recomendacion}
                    </p>
                </div>
                <hr>
                Puntaje: <strong>${data.puntaje}</strong> puntos<br>
                Porcentaje: <strong>${data.porcentaje ? data.porcentaje.toFixed(1) : 0}%</strong>
            `;
            mostrarMensajeCuestionario(
                mensajeHTML, 
                "success"
            );
            
            revisarVisualmenteCuestionario(form, btn, data.detalle_respuestas);
            marcarComoCompletado(sectionId);
            
            // Actualizar el estado en el sidebar si existe
            actualizarEstadoSidebar(sectionId);
        } else {
            mostrarMensajeCuestionario("Error al guardar las respuestas.", "danger");
            btn.disabled = false;
            btn.textContent = "Enviar respuestas";
        }
    })
    .catch(error => {
        console.error("Error:", error);
        mostrarMensajeCuestionario("Error de conexión. Intenta nuevamente.", "danger");
        btn.disabled = false;
        btn.textContent = "Enviar respuestas";
    });
}

function validarCuestionarioCompleto() {
    let todasRespondidas = true;
    
    document.querySelectorAll('.pregunta-card').forEach(card => {
        const tieneRespuesta = card.querySelector('input[type="radio"]:checked');
        if (!tieneRespuesta) {
            todasRespondidas = false;
            card.style.backgroundColor = "#fff5f5";
            setTimeout(() => {
                card.style.backgroundColor = "";
            }, 2000);
        }
    });
    
    return todasRespondidas;
}


function revisarVisualmenteCuestionario(form, btn, detalle_respuestas) {
    // 1. Deshabilitar todos los radio buttons
    form.querySelectorAll('input[type="radio"]').forEach(input => {
        input.disabled = true;
    });

    // 2. Aplicar las marcas visuales
    if (detalle_respuestas && Array.isArray(detalle_respuestas)) {
        detalle_respuestas.forEach(detalle => {
            const respuestaCorrectaId = detalle.respuesta_correcta_id;
            const respuestaEnviadaId = detalle.respuesta_enviada_id;
            const esCorrecta = detalle.es_correcta;

            const inputsPregunta = form.querySelectorAll(`input[name="pregunta_${detalle.pregunta_id}"]`);
            
            inputsPregunta.forEach(input => {
                const label = input.nextElementSibling;
                if (!label) return;

                // Si fue la respuesta seleccionada, la marcamos como "checked"
                if (input.value == respuestaEnviadaId) {
                    input.checked = true;
                }

                if (input.value == respuestaCorrectaId) {
                    label.innerHTML += ' <span class="badge bg-success ms-2">✓ Correcta</span>';
                } 
                else if (input.value == respuestaEnviadaId && !esCorrecta) {
                    label.innerHTML += ' <span class="badge bg-danger ms-2">✗ Tu respuesta</span>';
                }
            });
        });
    }
    
    btn.classList.remove("btn-success");
    btn.classList.add("btn-secondary");
    btn.innerHTML = "Cuestionario completado";
    btn.disabled = true;
}

function marcarComoCompletado(sectionId) {
    const estadoElement = document.getElementById(`estado-${sectionId}`);
    if (estadoElement) {
        estadoElement.classList.add("completado");
        estadoElement.innerHTML = "✓";
    }
}

function actualizarEstadoSidebar(sectionId) {
    const sidebarLink = document.querySelector(`.sidebar-link[data-section="${sectionId}"] .estado-item`);
    if (sidebarLink) {
        sidebarLink.classList.add("completado");
        sidebarLink.innerHTML = "✓";
    }
}


function mostrarMensaje(texto, tipo = "info") {
    const panel = document.getElementById("panel-dinamico");
    if (!panel) return;

    const mensaje = document.createElement("div");
    mensaje.className = `alert alert-${tipo} alert-dismissible fade show`;
    mensaje.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    `;
    
    mensaje.innerHTML = `
        ${texto}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    panel.appendChild(mensaje);
    
    setTimeout(() => {
        if (mensaje.parentNode) {
            mensaje.remove();
        }
    }, 5000);
}

function mostrarMensajeCuestionario(texto, tipo = "info") {
    const cuestionarioDiv = document.querySelector(".ajax-cuestionario");
    if (!cuestionarioDiv) return;

    const mensajesAnteriores = cuestionarioDiv.querySelectorAll(".mensaje-cuestionario");
    mensajesAnteriores.forEach(msg => msg.remove());

    const mensaje = document.createElement("div");
    mensaje.className = `mensaje-cuestionario alert alert-${tipo}`;
    mensaje.style.cssText = `
        margin: 15px auto;
        max-width: 680px;
        text-align: center;
        font-weight: 500;
    `;
    
    mensaje.innerHTML = texto;

    const encabezado = cuestionarioDiv.querySelector(".text-center");
    if (encabezado) {
        encabezado.parentNode.insertBefore(mensaje, encabezado.nextSibling);
    } else {
        cuestionarioDiv.prepend(mensaje);
    }

    if (tipo !== "success") {
        setTimeout(() => {
            if (mensaje.parentNode) {
                mensaje.remove();
            }
        }, 7000);
    }
}

function syncSidebarHeight() {
    const main = document.getElementById("mainCursoContent");
    const sidebar = document.getElementById("sidebarCurso");
    
    if (main && sidebar && window.innerWidth >= 768) {
        sidebar.style.height = 'auto';
        
        setTimeout(function() {
            const mainHeight = main.offsetHeight;
            sidebar.style.height = mainHeight + 'px';
            sidebar.style.minHeight = mainHeight + 'px';
        }, 100);
    } else if (sidebar && window.innerWidth < 768) {
        sidebar.style.height = 'auto';
        sidebar.style.minHeight = 'auto';
    }
}

if (document.getElementById("sidebarCurso")) {
    document.addEventListener('DOMContentLoaded', syncSidebarHeight);
    window.addEventListener('resize', syncSidebarHeight);
    window.addEventListener('load', syncSidebarHeight);
    
    if (typeof MutationObserver !== 'undefined') {
        const main = document.getElementById("mainCursoContent");
        if (main) {
            const observer = new MutationObserver(syncSidebarHeight);
            observer.observe(main, {
                childList: true,
                subtree: true
            });
        }
    }
}

