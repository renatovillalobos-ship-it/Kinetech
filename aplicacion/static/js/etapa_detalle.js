// Funciones específicas para etapa_detalle.html


// Inicialización cuando el DOM está listo
document.addEventListener('DOMContentLoaded', function() {
    const itemsInteractivos = document.querySelectorAll('.item-interactivo');
    const descripcionBox = document.getElementById('descripcion-resultado');
    const resultadoTitulo = document.getElementById('resultado-titulo');
    const resultadoDescripcion = document.getElementById('resultado-descripcion');
    
    // Función para manejar el clic en Diagnósticos/Tratamientos
    itemsInteractivos.forEach(item => {
        item.addEventListener('click', function() {
            // 1. Obtener datos del botón (vienen del data-attributes del HTML)
            const titulo = this.getAttribute('data-titulo');
            const descripcion = this.getAttribute('data-descripcion');
            
            // 2. Limpiar la selección previa y marcar el botón actual
            itemsInteractivos.forEach(i => i.classList.remove('activo'));
            this.classList.add('activo');
            
            // 3. Llenar el área de descripción
            resultadoTitulo.textContent = titulo;
            // Usamos innerHTML porque la descripción (TextField) puede contener formato HTML
            resultadoDescripcion.innerHTML = descripcion; 
            
            // 4. Mostrar la caja y desplazar la vista
            descripcionBox.style.display = 'block';
            descripcionBox.scrollIntoView({ behavior: 'smooth', block: 'center' });
        });
    });
    // Configurar botón siguiente
    const btnSiguiente = document.getElementById('btnSiguiente');
    if (btnSiguiente && btnSiguiente.dataset.nextUrl) {
        btnSiguiente.addEventListener('click', function() {
            window.location.href = this.dataset.nextUrl;
        });
    }
    
    // Configurar para videos (si no hay script inline)
    const tieneVideo = document.querySelector('.video-container iframe');
    if (tieneVideo && !document.querySelector('script[data-video-managed]')) {
        manejarVideoAutomatico();
    }
});

// Función para manejar videos automáticamente
function manejarVideoAutomatico() {
    setTimeout(function() {
        const btnSiguiente = document.getElementById('btnSiguiente');
        if (btnSiguiente) {
            btnSiguiente.classList.add('habilitado');
            btnSiguiente.disabled = false;
            
            // Mostrar mensaje de video visto
            const videoId = document.querySelector('.video-section h3 i.fa-video') ? 
                           'video-completado' : 'video-respuesta-completado';
            const videoCompletado = document.getElementById(videoId);
            if (videoCompletado) {
                videoCompletado.style.display = 'block';
            }
        }
    }, 5000); // 5 segundos
}
