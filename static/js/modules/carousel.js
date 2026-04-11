let heroSlideIndex = 0;
let heroTimer = null;
const slides = document.querySelectorAll('.hero-slide');
const dots = document.querySelectorAll('.hero-dot');

function showSlide(n) {
    if (!slides.length) return;
    slides[heroSlideIndex]?.classList.remove('active');
    dots[heroSlideIndex]?.classList.remove('active');
    heroSlideIndex = (n + slides.length) % slides.length;
    slides[heroSlideIndex]?.classList.add('active');
    dots[heroSlideIndex]?.classList.add('active');
}

function startTimer() {
    if (heroTimer) clearInterval(heroTimer);
    heroTimer = setInterval(() => showSlide(heroSlideIndex + 1), 6000);
}

export function initCarousel() {
    if (!slides.length) return;

    startTimer();

    dots.forEach((dot, i) => {
        dot.addEventListener('click', () => {
            clearInterval(heroTimer);
            showSlide(i);
            startTimer();
        });
    });

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowLeft') {
            clearInterval(heroTimer);
            showSlide(heroSlideIndex - 1);
            startTimer();
        } else if (e.key === 'ArrowRight') {
            clearInterval(heroTimer);
            showSlide(heroSlideIndex + 1);
            startTimer();
        }
    });

    // Touch swipe
    const heroEl = document.querySelector('.hero-section');
    if (heroEl) {
        let touchStartX = 0;
        heroEl.addEventListener('touchstart', (e) => {
            touchStartX = e.changedTouches[0].screenX;
        }, { passive: true });
        heroEl.addEventListener('touchend', (e) => {
            const diff = touchStartX - e.changedTouches[0].screenX;
            if (Math.abs(diff) > 50) {
                clearInterval(heroTimer);
                showSlide(heroSlideIndex + (diff > 0 ? 1 : -1));
                startTimer();
            }
        });
    }

    // Pause on visibility change
    document.addEventListener('visibilitychange', () => {
        if (document.hidden) clearInterval(heroTimer);
        else startTimer();
    });
}