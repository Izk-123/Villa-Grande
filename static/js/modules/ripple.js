export function initRipple() {
    document.addEventListener('click', (e) => {
        const btn = e.target.closest('.btn-vg-primary, .btn-vg-outline, .btn-primary, .btn-secondary');
        if (!btn) return;

        const ripple = document.createElement('span');
        const rect = btn.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        ripple.style.cssText = `
            position: absolute;
            border-radius: 50%;
            pointer-events: none;
            width: ${size}px;
            height: ${size}px;
            left: ${e.clientX - rect.left - size / 2}px;
            top: ${e.clientY - rect.top - size / 2}px;
            background: rgba(255,255,255,0.2);
            transform: scale(0);
            animation: rippleEffect 0.5s ease;
        `;
        if (getComputedStyle(btn).position === 'static') btn.style.position = 'relative';
        btn.style.overflow = 'hidden';
        btn.appendChild(ripple);
        setTimeout(() => ripple.remove(), 500);
    });
}