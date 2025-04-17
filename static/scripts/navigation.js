document.addEventListener('DOMContentLoaded', function() {
    // Highlight current page in sidebar
    const currentPage = window.location.pathname.split('/').pop();
    const navLinks = {
        'index.html': 'dashboard-link',
        'top-movers.html': 'movers-link',
        'news.html': 'news-link',
        'ai-assistant.html': 'assistant-link'
    };

    // Remove active class from all links
    document.querySelectorAll('.sidebar-nav a').forEach(link => {
        link.classList.remove('active');
    });

    // Add active class to current page link
    if (navLinks[currentPage]) {
        document.getElementById(navLinks[currentPage]).classList.add('active');
    }
});