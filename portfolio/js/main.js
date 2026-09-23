// New Dynamic Project Engine
async function loadProjects() {
    try {
        const response = await fetch('projects.json');
        const projects = await response.json();
        
        // Populate project cards
        const grid = document.querySelector('.project-grid');
        grid.innerHTML = ''; // Clear placeholders

        projects.forEach(proj => {
            const card = document.createElement('div');
            card.className = 'project-card reveal';
            card.dataset.project = proj.id;
            card.innerHTML = `
                <h3>${proj.title}</h3>
                <p>${proj.desc.substring(0, 80)}...</p>
                <button class="btn btn-small">Learn More</button>
            `;
            grid.appendChild(card);
        });

        // Update Modal Logic to use this data
        document.querySelectorAll('.project-card button').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const projectKey = e.target.closest('.project-card').dataset.project;
                const data = projects.find(p => p.id === projectKey);
                
                document.getElementById('modal-title').textContent = data.title;
                document.getElementById('modal-desc').textContent = data.desc;
                document.getElementById('modal-tags').innerHTML = data.tags.map(t => `<span class="tag">${t}</span>`).join(' ');
                
                document.getElementById('project-modal').style.display = 'flex';
            });
        });

        // Run reveal again for newly added elements
        reveal();

    } catch (error) {
        console.error("Error loading projects:", error);
    }
}

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

// Modal Close Logic
const modal = document.getElementById('project-modal');
const closeBtn = document.querySelector('.close-modal');

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
window.addEventListener('load', () => {
    reveal();
    loadProjects();
});

// Header effect
window.addEventListener('scroll', () => {
    const header = document.querySelector('header');
    header.style.background = window.scrollY > 50 ? '#0f172a' : '#1e293b';
});
