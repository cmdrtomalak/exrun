// Interactive Components - Add JavaScript for enhanced interactions

// TODO: Animate skill bars when they come into view
const observerOptions = {
    threshold: 0.5,
    rootMargin: '0px'
};

const skillObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const skillProgress = entry.target;
            const skillLevel = skillProgress.getAttribute('data-skill');
            skillProgress.style.transform = `scaleX(${parseInt(skillLevel) / 100})`;
        }
    });
}, observerOptions);

// Observe all skill progress bars
document.addEventListener('DOMContentLoaded', () => {
    const skillBars = document.querySelectorAll('.skill-progress');
    skillBars.forEach(bar => skillObserver.observe(bar));
    
    // TODO: Add form submission interaction
    const form = document.querySelector('.contact-form');
    const submitBtn = document.querySelector('.submit-btn');
    
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        
        // Add loading state
        submitBtn.classList.add('loading');
        submitBtn.disabled = true;
        
        // Simulate form submission
        setTimeout(() => {
            submitBtn.classList.remove('loading');
            submitBtn.disabled = false;
            
            // Show success message
            const successMessage = document.createElement('div');
            successMessage.textContent = 'Message sent successfully!';
            successMessage.style.cssText = `
                background: #28a745;
                color: white;
                padding: 1rem;
                border-radius: 4px;
                margin-top: 1rem;
                text-align: center;
                animation: fadeInUp 0.5s ease;
            `;
            
            form.appendChild(successMessage);
            form.reset();
            
            // Remove success message after 3 seconds
            setTimeout(() => {
                successMessage.style.animation = 'fadeOut 0.5s ease';
                setTimeout(() => successMessage.remove(), 500);
            }, 3000);
        }, 2000);
    });
    
    // TODO: Add smooth scroll for navigation links
    const navLinks = document.querySelectorAll('.nav-link, .project-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            const href = link.getAttribute('href');
            
            // Check if it's an internal link
            if (href.startsWith('#')) {
                e.preventDefault();
                const target = document.querySelector(href);
                
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
    
    // TODO: Add interactive card tilt effect on mouse move
    const cards = document.querySelectorAll('.interactive-card');
    
    cards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const rotateX = (y - centerY) / 10;
            const rotateY = (centerX - x) / 10;
            
            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateZ(10px)`;
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateZ(0)';
        });
    });
});

// TODO: Add parallax scrolling effect
window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const parallaxElements = document.querySelectorAll('.hero-content');
    
    parallaxElements.forEach(element => {
        const speed = 0.5;
        element.style.transform = `translateY(${scrolled * speed}px)`;
    });
});
