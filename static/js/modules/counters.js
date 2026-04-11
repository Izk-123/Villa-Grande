export function initCounters() {
    if (!('IntersectionObserver' in window)) return;
    const counters = document.querySelectorAll('[data-target]');
    if (!counters.length) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.4 });

    counters.forEach(el => observer.observe(el));
}

function animateCounter(el) {
    const target = parseInt(el.getAttribute('data-target'), 10);
    const duration = 2200;
    const frameRate = 16;
    const totalFrames = Math.round(duration / frameRate);
    let frame = 0;
    const easeOutCubic = t => 1 - Math.pow(1 - t, 3);

    const timer = setInterval(() => {
        frame++;
        const progress = easeOutCubic(frame / totalFrames);
        const current = Math.round(progress * target);
        el.textContent = current.toLocaleString() + '+';
        if (frame >= totalFrames) {
            el.textContent = target.toLocaleString() + '+';
            clearInterval(timer);
        }
    }, frameRate);
}