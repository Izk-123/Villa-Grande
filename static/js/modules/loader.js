export function initLoader() {
    const loader = document.getElementById('vg-loader');
    if (!loader) return;

    window.addEventListener('load', () => {
        setTimeout(() => {
            loader.classList.add('fade-out');
            loader.addEventListener('transitionend', () => {
                loader.style.display = 'none';
            }, { once: true });
        }, 1800); // shorter duration
    });
}