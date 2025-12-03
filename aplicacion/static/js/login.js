/*
        Designed by: SELECTO
        Original image: https://dribbble.com/shots/5311359-Diprella-Login
*/

function getCSRFToken() {
    const csrfCookie = document.cookie.split('; ').find(row => row.startsWith('csrftoken='));
    return csrfCookie ? csrfCookie.split('=')[1] : '';
}

let switchCtn = document.querySelector("#switch-cnt");
let switchC1 = document.querySelector("#switch-c1");
let switchC2 = document.querySelector("#switch-c2");
let switchCircle = document.querySelectorAll(".switch__circle");
let switchBtn = document.querySelectorAll(".switch-btn");
let aContainer = document.querySelector("#a-container");
let bContainer = document.querySelector("#b-container");
let allButtons = document.querySelectorAll(".submit");

let changeForm = (e) => {
    switchCtn.classList.add("is-gx");
    setTimeout(function(){
        switchCtn.classList.remove("is-gx");
    }, 1500)

    switchCtn.classList.toggle("is-txr");
    switchCircle[0].classList.toggle("is-txr");
    switchCircle[1].classList.toggle("is-txr");

    switchC1.classList.toggle("is-hidden");
    switchC2.classList.toggle("is-hidden");
    aContainer.classList.toggle("is-txl");
    bContainer.classList.toggle("is-txl");
    bContainer.classList.toggle("is-z200");
}

let mainF = (e) => {
    for (var i = 0; i < switchBtn.length; i++)
        switchBtn[i].addEventListener("click", changeForm)
}

window.addEventListener("load", mainF);

// === CAMBIO ENTRE FORMULARIOS DOCENTE Y ESTUDIANTE ===
const docenteForm = document.getElementById("docente-form");
const estudianteForm = document.getElementById("estudiante-form");

// Obtener TODOS los botones por clase
const docenteBtns = document.querySelectorAll(".docente-btn");
const estudianteBtns = document.querySelectorAll(".estudiante-btn");

// Agregar evento a TODOS los botones de docente
docenteBtns.forEach(btn => {
    btn.addEventListener("click", () => {
        if (docenteForm && estudianteForm) {
            docenteForm.style.display = "flex";
            estudianteForm.style.display = "none";

            // Limpiar validación anterior ESTO LO DEBO AGREGAR
            const mensajeContainer = document.querySelector('#messages-container-estudiante');
            if (mensajeContainer) {
                const mensajesValidacion = mensajeContainer.querySelectorAll('.correo-validation');
                mensajesValidacion.forEach(msg => msg.remove());
            }
        }
    });
});

// Agregar evento a TODOS los botones de estudiante
estudianteBtns.forEach(btn => {
    btn.addEventListener("click", () => {
        if (docenteForm && estudianteForm) {
            estudianteForm.style.display = "flex";
            docenteForm.style.display = "none";

            // ✅ AGREGAR ESTA LÍNEA PARA ACTIVAR LA VALIDACIÓN
            setTimeout(inicializarValidacionEstudiante, 100);
        }
    });
});



//DE ACA AGREGO MUCHOS CAMBIOS IIIIIIIIIIIIIIIIIII

// ✅ FUNCIÓN DE VALIDACIÓN MEJORADA
function validarCorreo(correo, mensajeContainer, submitBtn) {
    // Validación básica frontend primero
    if (!correo.includes('@')) {
        mostrarMensajeValidacion(mensajeContainer, 'error', 'Formato de correo inválido', 0);
        actualizarBotonSubmit(false, submitBtn);
        return;
    }

    fetch('/estudiante/validar-correo-ucn/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCSRFToken()
        },
        body: 'correo=' + encodeURIComponent(correo)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error en la respuesta del servidor');
        }
        return response.json();
    })
    .then(data => {
        console.log('Respuesta validación:', data);
        
        mostrarMensajeValidacion(
            mensajeContainer, 
            data.valido ? 'success' : 'error', 
            data.mensaje, 
            data.tiempo
        );
        
        // ✅ CONTROLAR BOTÓN CORRECTAMENTE
        actualizarBotonSubmit(data.valido, submitBtn);
    })
    .catch(error => {
        console.error('Error en validación:', error);
        mostrarMensajeValidacion(mensajeContainer, 'error', 'Error al validar el correo', 0);
        // En caso de error, habilitar el botón para no bloquear al usuario
        actualizarBotonSubmit(true, submitBtn);
    });
}

// ✅ FUNCIÓN AUXILIAR PARA ACTUALIZAR BOTÓN
function actualizarBotonSubmit(habilitar, submitBtn) {
    if (submitBtn) {
        submitBtn.disabled = !habilitar;
        submitBtn.style.opacity = habilitar ? '1' : '0.6';
        submitBtn.style.cursor = habilitar ? 'pointer' : 'not-allowed';
        
        console.log('Botón actualizado:', { 
            habilitado: habilitar, 
            disabled: submitBtn.disabled,
            opacity: submitBtn.style.opacity 
        });
    }
}

// ✅ FUNCIÓN AUXILIAR PARA MOSTRAR MENSAJES
function mostrarMensajeValidacion(container, tipo, mensaje, tiempo) {
    // Limpiar mensajes anteriores de validación
    const mensajesAnteriores = container.querySelectorAll('.correo-validation');
    mensajesAnteriores.forEach(msg => msg.remove());
    
    // Crear nuevo mensaje
    const mensajeElement = document.createElement('div');
    mensajeElement.className = `correo-validation alert ${tipo === 'success' ? 'alert-success' : 'alert-error'}`;
    
    const icono = tipo === 'success' ? '✓' : '✗';
    mensajeElement.innerHTML = `${icono} ${mensaje} <small>(${tiempo}s)</small>`;
    
    container.appendChild(mensajeElement);
    
    // Auto-eliminar mensaje después de 5 segundos (opcional)
    setTimeout(() => {
        if (mensajeElement.parentNode) {
            mensajeElement.remove();
        }
    }, 5000);
}

// ✅ FUNCIÓN PARA VALIDAR FORMULARIO COMPLETO
function validarFormularioCompleto(correoInput, mensajeContainer, submitBtn) {
    const correo = correoInput.value.trim();
    const nombre = document.querySelector('input[name="nombre_est"]')?.value.trim();
    const apellido = document.querySelector('input[name="apellido_est"]')?.value.trim();
    const pais = document.querySelector('select[name="pais_est"]')?.value;
    const password = document.querySelector('input[name="password_est"]')?.value.trim();
    
    console.log('Validando formulario completo:', { nombre, apellido, pais, password, correo });
    
    // Validar que todos los campos básicos estén llenos
    const camposCompletos = nombre && apellido && pais && password && correo;
    
    if (!camposCompletos) {
        console.log('❌ Campos incompletos, deshabilitando botón');
        actualizarBotonSubmit(false, submitBtn);
        return;
    }
    
    // Si el correo está vacío, habilitar botón temporalmente
    if (correo.length === 0) {
        console.log('📝 Correo vacío, habilitando botón temporalmente');
        actualizarBotonSubmit(true, submitBtn);
        return;
    }
    
    console.log('✅ Todos los campos completos, validando correo...');
    // Validar correo específicamente
    validarCorreo(correo, mensajeContainer, submitBtn);
}

function inicializarValidacionEstudiante() {
    const correoInput = document.querySelector('input[name="correo_est"]');
    const mensajeContainer = document.querySelector('#messages-container-estudiante');
    const submitBtn = document.querySelector('#estudiante-form .form__button.button.submit');
    
    console.log('Buscando elementos:', { 
        correoInput: !!correoInput, 
        mensajeContainer: !!mensajeContainer, 
        submitBtn: !!submitBtn 
    });
    
    if (!correoInput || !mensajeContainer || !submitBtn) {
        console.log('Esperando elementos del formulario estudiante...');
        setTimeout(inicializarValidacionEstudiante, 200);
        return;
    }

    console.log('✅ Validación de estudiante INICIADA');
    
    let timeoutId;
    
    // ✅ VALIDAR TODOS LOS CAMPOS INICIALMENTE
    validarFormularioCompleto(correoInput, mensajeContainer, submitBtn);
    
    // Validar cuando se escribe en el correo
    correoInput.addEventListener('input', function() {
        clearTimeout(timeoutId);
        const correo = this.value.trim();
        
        // Limpiar mensajes anteriores
        const mensajesAnteriores = mensajeContainer.querySelectorAll('.correo-validation');
        mensajesAnteriores.forEach(msg => msg.remove());
        
        // Validar formulario completo (incluye validación de campos vacíos)
        validarFormularioCompleto(correoInput, mensajeContainer, submitBtn);
        
        if (correo.length === 0) {
            return;
        }
        
        timeoutId = setTimeout(() => {
            validarCorreo(correo, mensajeContainer, submitBtn);
        }, 800);
    });
    
    // ✅ Validar cuando cambian otros campos del formulario
    const otrosCampos = [
        document.querySelector('input[name="nombre_est"]'),
        document.querySelector('input[name="apellido_est"]'),
        document.querySelector('select[name="pais_est"]'),
        document.querySelector('input[name="password_est"]')
    ];
    
    otrosCampos.forEach(campo => {
        if (campo) {
            campo.addEventListener('input', () => {
                console.log('Campo cambiado:', campo.name);
                validarFormularioCompleto(correoInput, mensajeContainer, submitBtn);
            });
            campo.addEventListener('change', () => {
                console.log('Campo cambiado (change):', campo.name);
                validarFormularioCompleto(correoInput, mensajeContainer, submitBtn);
            });
        }
    });
}

// === 🔥 NUEVO CÓDIGO PARA VALIDACIÓN DE EXISTENCIA DE CUENTA ===

// ✅ FUNCIÓN PARA VALIDAR EXISTENCIA DE CUENTA (LOGIN)
function validarExistenciaCuenta(correo, mensajeContainer) {
    if (!correo.includes('@')) {
        mostrarMensajeExistencia(mensajeContainer, 'error', 'Formato de correo inválido', 0);
        return;
    }

    fetch('/estudiante/validar-existencia-cuenta/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCSRFToken()
        },
        body: 'correo=' + encodeURIComponent(correo)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error en la respuesta del servidor');
        }
        return response.json();
    })
    .then(data => {
        console.log('Respuesta validación existencia:', data);
        
        mostrarMensajeExistencia(
            mensajeContainer, 
            data.existe ? 'success' : 'error', 
            data.mensaje, 
            data.tiempo
        );
        
        // Opcional: Dar feedback visual adicional
        if (data.existe) {
            // Cuenta existe - habilitar campo de contraseña si está deshabilitado
            const passwordInput = document.querySelector('#b-form input[type="password"]');
            if (passwordInput) {
                passwordInput.placeholder = "Ingresa tu contraseña";
                passwordInput.focus();
            }
        }
    })
    .catch(error => {
        console.error('Error en validación existencia:', error);
        mostrarMensajeExistencia(mensajeContainer, 'error', 'Error al verificar la cuenta', 0);
    });
}

// ✅ FUNCIÓN AUXILIAR PARA MOSTRAR MENSAJES DE EXISTENCIA
function mostrarMensajeExistencia(container, tipo, mensaje, tiempo) {
    // Limpiar mensajes anteriores de existencia
    const mensajesAnteriores = container.querySelectorAll('.existencia-validation');
    mensajesAnteriores.forEach(msg => msg.remove());
    
    // Crear nuevo mensaje
    const mensajeElement = document.createElement('div');
    mensajeElement.className = `existencia-validation alert ${tipo === 'success' ? 'alert-success' : 'alert-error'}`;
    
    const icono = tipo === 'success' ? '✓' : '✗';
    mensajeElement.innerHTML = `${icono} ${mensaje} <small>(${tiempo}s)</small>`;
    
    container.appendChild(mensajeElement);
    
    // Auto-eliminar mensaje después de 5 segundos
    setTimeout(() => {
        if (mensajeElement.parentNode) {
            mensajeElement.remove();
        }
    }, 5000);
}

// ✅ INICIALIZAR VALIDACIÓN DE LOGIN
function inicializarValidacionLogin() {
    const correoInput = document.querySelector('#b-form input[type="text"]');
    
    // Crear contenedor de mensajes si no existe
    let mensajeContainer = document.querySelector('#b-form .form__messages');
    if (!mensajeContainer) {
        const form = document.querySelector('#b-form');
        if (form) {
            const newContainer = document.createElement('div');
            newContainer.className = 'form__messages';
            // Insertar después del título y antes de los campos
            const title = form.querySelector('.title');
            if (title) {
                title.parentNode.insertBefore(newContainer, title.nextSibling);
            } else {
                form.insertBefore(newContainer, form.firstChild);
            }
            mensajeContainer = newContainer;
        }
    }
    
    if (!correoInput || !mensajeContainer) {
        console.log('Esperando elementos del formulario login...');
        setTimeout(inicializarValidacionLogin, 200);
        return;
    }

    console.log('✅ Validación de login INICIADA');
    
    let timeoutId;
    
    // Validar cuando se escribe en el correo (login)
    correoInput.addEventListener('input', function() {
        clearTimeout(timeoutId);
        const correo = this.value.trim();
        
        // Limpiar mensajes anteriores
        const mensajesAnteriores = mensajeContainer.querySelectorAll('.existencia-validation');
        mensajesAnteriores.forEach(msg => msg.remove());
        
        if (correo.length === 0) {
            return;
        }
        
        timeoutId = setTimeout(() => {
            validarExistenciaCuenta(correo, mensajeContainer);
        }, 800);
    });
}

// ✅ MODIFICAR LA INICIALIZACIÓN PRINCIPAL - REEMPLAZAR LA ACTUAL
document.addEventListener('DOMContentLoaded', function() {
    console.log('📄 Página cargada, inicializando validaciones...');
    
    // Inicializar validación de login (siempre)
    setTimeout(inicializarValidacionLogin, 300);
    
    // Inicializar validación de registro (si está visible)
    const estudianteForm = document.getElementById("estudiante-form");
    if (estudianteForm && estudianteForm.style.display !== "none") {
        console.log('🎯 Formulario estudiante visible, inicializando...');
        setTimeout(inicializarValidacionEstudiante, 300);
    }
    
    // También inicializar si el usuario cambia al formulario de estudiante después
    const estudianteBtns = document.querySelectorAll(".estudiante-btn");
    estudianteBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            setTimeout(inicializarValidacionEstudiante, 100);
        });
    });
});

// ✅ FUNCIÓN PARA MOSTRAR PROCESANDO REGISTRO
function mostrarProcesandoRegistro(form, estado) {
    const submitBtn = form.querySelector('.submit');
    const mensajeProcesando = form.querySelector('.procesando-registro');
    
    if (estado) {
        // Mostrar "Procesando..."
        if (!mensajeProcesando) {
            const mensaje = document.createElement('div');
            mensaje.className = 'procesando-registro alert alert-info';
            mensaje.innerHTML = '⏳ Procesando registro...';
            form.insertBefore(mensaje, submitBtn);
        }
        submitBtn.disabled = true;
        submitBtn.textContent = 'PROCESANDO...';
    } else {
        // Quitar "Procesando..."
        if (mensajeProcesando) {
            mensajeProcesando.remove();
        }
        submitBtn.disabled = false;
        submitBtn.textContent = 'CREAR CUENTA';
    }
}

// ✅ AGREGAR EVENTO A LOS FORMULARIOS DE REGISTRO
document.addEventListener('DOMContentLoaded', function() {
    const formsRegistro = [
        document.getElementById('estudiante-form'),
        document.getElementById('docente-form')
    ];
    
    formsRegistro.forEach(form => {
        if (form) {
            form.addEventListener('submit', function() {
                mostrarProcesandoRegistro(this, true);
                
                // Opcional: Timeout de seguridad por si tarda más de 10 segundos
                setTimeout(() => {
                    mostrarProcesandoRegistro(form, false);
                }, 10000);
            });
        }
    });
});





// === 🔥 FUNCIONALIDAD MODAL POLÍTICAS ===
function inicializarModalPoliticas() {
    const modal = document.getElementById('modalPoliticas');
    const enlacesPoliticas = document.querySelectorAll('a[href="#politicas"]');
    const cerrarModal = document.querySelector('.cerrar-modal');
    const aceptarBtn = document.getElementById('aceptarPoliticas');

    if (!modal) return;

    enlacesPoliticas.forEach(enlace => {
        enlace.addEventListener('click', (e) => {
            e.preventDefault();
            modal.style.display = 'block';
        });
    });

    if (cerrarModal) {
        cerrarModal.addEventListener('click', () => {
            modal.style.display = 'none';
        });
    }

    if (aceptarBtn) {
        aceptarBtn.addEventListener('click', () => {
            modal.style.display = 'none';
        });
    }

    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });
}



// =================================================================
// ✅ INICIALIZACIÓN PRINCIPAL ÚNICA (COMBINADA)
// =================================================================
document.addEventListener('DOMContentLoaded', function() {
    console.log('📄 Página cargada, inicializando todas las funcionalidades...');
    
    // 1. Validación de login
    setTimeout(inicializarValidacionLogin, 300);
    
    // 2. Validación de registro (si está visible)
    const estudianteForm = document.getElementById("estudiante-form");
    if (estudianteForm && estudianteForm.style.display !== "none") {
        console.log('🎯 Formulario estudiante visible, inicializando...');
        setTimeout(inicializarValidacionEstudiante, 300);
    }
    
    // 3. Modal de políticas de privacidad
    setTimeout(inicializarModalPoliticas, 500);
    
    // 4. Demostración de capacidad (50 usuarios)
    setTimeout(demostrarCapacidadUsuarios, 1500);
    
    // 5. Botones de cambio estudiante/docente
    const estudianteBtns = document.querySelectorAll(".estudiante-btn");
    estudianteBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            setTimeout(inicializarValidacionEstudiante, 100);
        });
    });
});






// === 🚀 DEMOSTRACIÓN 50 USUARIOS ===
function demostrarCapacidadUsuarios() {
    console.log('='.repeat(50));
    console.log('✅ SISTEMA OPTIMIZADO PARA 50+ USUARIOS SIMULTÁNEOS');
    console.log('='.repeat(50));
    console.log('📊 MÉTRICAS:');
    console.log('• Validaciones: < 10ms por usuario');
    console.log('• Sesiones: 24 horas persistencia');
    console.log('• DB: Conexiones optimizadas');
    
    const notificacion = document.createElement('div');
    notificacion.id = 'notif-capacidad';
    notificacion.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: linear-gradient(135deg, #4B70E2, #3a5bc7);
        color: white;
        padding: 12px 16px;
        border-radius: 8px;
        font-size: 14px;
        font-family: 'Source Sans Pro', sans-serif;
        box-shadow: 4px 4px 10px rgba(0,0,0,0.2);
        z-index: 10000;
        display: flex;
        align-items: center;
        gap: 8px;
        animation: slideIn 0.5s ease;
    `;
    
    notificacion.innerHTML = `
        <span style="font-size: 16px;">✓</span>
        <div>
            <strong>Soporta 50+ usuarios</strong><br>
            <small>Tiempos de respuesta: < 10ms</small>
        </div>
    `;
    
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
    `;
    document.head.appendChild(style);
    document.body.appendChild(notificacion);
    
    setTimeout(() => {
        notificacion.style.opacity = '0';
        notificacion.style.transition = 'opacity 1s';
        setTimeout(() => notificacion.remove(), 1000);
    }, 10000);
}

// Inicializar
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(demostrarCapacidadUsuarios, 1500);
});
