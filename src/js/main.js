const slides = document.querySelectorAll('.slide');
const dotsContainer = document.getElementById('navDots');

// Create dots
slides.forEach((slide, i) => {
  const dot = document.createElement('button');
  dot.className = 'nav-dot';
  dot.setAttribute('aria-label', `Go to slide ${i + 1}`);
  dot.addEventListener('click', () => {
    slide.scrollIntoView({ behavior: 'smooth' });
  });
  // Mark section starts (hero slides)
  if (slide.classList.contains('slide--hero') || slide.classList.contains('slide--cover')) {
    dot.classList.add('section-start');
  }
  dotsContainer.appendChild(dot);
});

// Update active dot on scroll
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const idx = [...slides].indexOf(entry.target);
      document.querySelectorAll('.nav-dot').forEach((d, i) => {
        d.classList.toggle('active', i === idx);
      });
    }
  });
}, { threshold: 0.5 });

slides.forEach(slide => observer.observe(slide));

// Keyboard navigation
document.addEventListener('keydown', (e) => {
  const current = [...slides].findIndex(s => {
    const rect = s.getBoundingClientRect();
    return rect.top >= -100 && rect.top < window.innerHeight / 2;
  });
  if ((e.key === 'ArrowDown' || e.key === 'ArrowRight') && current < slides.length - 1) {
    e.preventDefault();
    slides[current + 1].scrollIntoView({ behavior: 'smooth' });
  }
  if ((e.key === 'ArrowUp' || e.key === 'ArrowLeft') && current > 0) {
    e.preventDefault();
    slides[current - 1].scrollIntoView({ behavior: 'smooth' });
  }
});
