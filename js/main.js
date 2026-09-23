document.getElementById('contact-form').addEventListener('submit', function(e) {
    e.preventDefault();
    alert('Thank you for your message! This is a demo portfolio, so no email was actually sent.');
    this.reset();
});

// Simple scroll animation for navigation
window.addEventListener('scroll', () => {
    const header = document.querySelector('header');
    header.style.background = window.scrollY > 50 ? '#0f172a' : '#1e293b';
});