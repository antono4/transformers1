document.getElementById('contact-form').addEventListener('submit', function(e) {
    e.preventDefault();
    alert('Thank you for your message! This is a demo portfolio, so no email was actually sent.');
    this.reset();
});

// Theme Toggle Logic
const themeToggle = document.getElementById('theme-toggle');
const body = document.body;
let isDark = localStorage.getItem('theme') === 'dark';

if (isDark) {
    body.setAttribute('data-theme', 'dark');
    themeToggle.textContent = '☀️';
}

themeToggle.addEventListener('click', () => {
    isDark = !isDark;
    body.setAttribute('data-theme', isDark ? 'dark' : 'light');
    themeToggle.textContent = isDark ? '☀️' : '🌙';
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
});

// Project Modal Logic
const projectsData = {
    one: {
        title: "Project One",
        desc: "This high-performance web application uses a microservices architecture to handle 10k+ requests per second. Built with React, Node.js, and Redis for caching.",
        tags: ["React", "Node.js", "Redis"]
    },
    two: {
        title: "Project Two",
        desc: "A full-scale e-commerce solution featuring a customized checkout flow, Stripe integration, and an administrative dashboard for inventory management.",
        tags: ["Next.js", "Stripe", "MongoDB"]
    },
    three: {
        title: "Project Three",
        desc: "Real-time data visualization tool that connects to public APIs to render complex data sets into intuitive charts and graphs using D3.js.",
        tags: ["D3.js", "TypeScript", "OpenWeather API"]
    }
};

const modal = document.getElementById('project-modal');
const modalTitle = document.getElementById('modal-title');
const modalDesc = document.getElementById('modal-desc');
const modalTags = document.getElementById('modal-tags');
const closeBtn = document.querySelector('.close-modal');

document.querySelectorAll('.project-card button').forEach(btn => {
    btn.addEventListener('click', (e) => {
        const projectKey = e.target.closest('.project-card').dataset.project;
        const data = projectsData[projectKey];
        
        modalTitle.textContent = data.title;
        modalDesc.textContent = data.desc;
        modalTags.innerHTML = data.tags.map(t => `<span class="tag">${t}</span>`).join(' ');
        
        modal.style.display = 'flex';
    });
});

closeBtn.addEventListener('click', () => {
    modal.style.display = 'none';
});

window.addEventListener('click', (e) => {
    if (e.target === modal) modal.style.display = 'none';
});

// Scroll Reveal Logic
function reveal() {
    const reveals = document.querySelectorAll('.reveal');
    reveals.forEach(el => {
        const windowHeight = window.innerHeight;
        const elementTop = el.getBoundingClientRect().top;
        const elementVisible = 150;
        if (elementTop < windowHeight - elementVisible) {
            el.classList.add('active');
        }
    });
}

window.addEventListener('scroll', reveal);
window.addEventListener('load', reveal);

// Header effect
window.addEventListener('scroll', () => {
    const header = document.querySelector('header');
    header.style.background = window.scrollY > 50 ? '#0f172a' : '#1e293b';
});
