function syncSidebarHeight() {
    const main = document.getElementById("mainCursoContent");
    const sidebar = document.getElementById("sidebarCurso");
    
    if (main && sidebar && window.innerWidth >= 768) {
        // Resetear la altura primero
        sidebar.style.height = 'auto';
        
        // Esperar un momento para que el navegador calcule las alturas
        setTimeout(function() {
            const mainHeight = main.offsetHeight;
            sidebar.style.height = mainHeight + 'px';
            sidebar.style.minHeight = mainHeight + 'px';
        }, 100);
    } else if (sidebar && window.innerWidth < 768) {
        // En móvil, quitar la altura forzada
        sidebar.style.height = 'auto';
        sidebar.style.minHeight = 'auto';
    }
}

// Ejecutar múltiples veces para asegurar que funcione
document.addEventListener('DOMContentLoaded', function() {
    syncSidebarHeight();
    setTimeout(syncSidebarHeight, 200);
    setTimeout(syncSidebarHeight, 500);
    setTimeout(syncSidebarHeight, 1000);
});

window.addEventListener('load', function() {
    syncSidebarHeight();
    setTimeout(syncSidebarHeight, 200);
});

window.addEventListener('resize', function() {
    syncSidebarHeight();
});

// Si hay imágenes, esperar a que carguen
document.querySelectorAll('img').forEach(function(img) {
    img.addEventListener('load', syncSidebarHeight);
});

// Observar cambios en el DOM
if (typeof MutationObserver !== 'undefined') {
    const main = document.getElementById("mainCursoContent");
    if (main) {
        const observer = new MutationObserver(function() {
            syncSidebarHeight();
        });
        
        observer.observe(main, {
            childList: true,
            subtree: true
        });
    }
}