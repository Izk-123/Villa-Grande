export function initNavbar() {
    const nav = document.getElementById('mainNav') || document.querySelector('.navbar-vg');
    if (!nav) return;
    const onScroll = () => {
        if (window.scrollY > 60) nav.classList.add('scrolled');
        else nav.classList.remove('scrolled');
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
}

export function initParallax() {
    if (window.innerWidth < 992) return;
    const heroSlides = document.querySelectorAll('.hero-slide');
    if (!heroSlides.length) return;
    window.addEventListener('scroll', () => {
        const y = window.scrollY * 0.3;
        heroSlides.forEach(slide => {
            slide.style.transform = `scale(${slide.classList.contains('active') ? 1 : 1.08}) translateY(${y}px)`;
        });
    }, { passive: true });
}

export function initDropdownHover() {
    if (window.innerWidth < 992) return;
    document.querySelectorAll('.navbar .dropdown').forEach(dropdown => {
        dropdown.addEventListener('mouseenter', () => {
            const menu = dropdown.querySelector('.dropdown-menu');
            const toggle = dropdown.querySelector('.dropdown-toggle');
            menu?.classList.add('show');
            toggle?.setAttribute('aria-expanded', 'true');
        });
        dropdown.addEventListener('mouseleave', () => {
            const menu = dropdown.querySelector('.dropdown-menu');
            const toggle = dropdown.querySelector('.dropdown-toggle');
            menu?.classList.remove('show');
            toggle?.setAttribute('aria-expanded', 'false');
        });
    });
}