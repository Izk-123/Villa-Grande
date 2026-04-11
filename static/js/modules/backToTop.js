export function initBackToTop() {
    const btt = document.getElementById('backToTop');
    if (!btt) return;

    window.addEventListener('scroll', () => {
        if (window.scrollY > 400) btt.classList.add('visible');
        else btt.classList.remove('visible');
    }, { passive: true });

    btt.addEventListener('click', (e) => {
        e.preventDefault();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}