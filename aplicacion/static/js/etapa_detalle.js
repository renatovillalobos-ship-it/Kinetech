// Funciones específicas para etapa_detalle.html

// Inicialización cuando el DOM está listo
document.addEventListener('DOMContentLoaded', function() {
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

