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

document.querySelectorAll('img').forEach(function(img) {
    img.addEventListener('load', syncSidebarHeight);
});

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