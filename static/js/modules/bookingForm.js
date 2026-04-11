export function initBookingForm() {
    const checkin = document.getElementById('checkin');
    const checkout = document.getElementById('checkout');
    if (!checkin || !checkout) return;

    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(today.getDate() + 1);
    const fmt = d => d.toISOString().split('T')[0];

    checkin.value = fmt(today);
    checkout.value = fmt(tomorrow);
    checkin.min = fmt(today);
    checkout.min = fmt(tomorrow);

    checkin.addEventListener('change', () => {
        const ci = new Date(checkin.value);
        const co = new Date(ci);
        co.setDate(ci.getDate() + 1);
        checkout.min = fmt(co);
        if (new Date(checkout.value) <= ci) checkout.value = fmt(co);
    });

    // Handle form submission (optional, but keep existing alert)
    const bookingForm = document.getElementById('bookingForm');
    if (bookingForm) {
        bookingForm.addEventListener('submit', (e) => {
            if (!checkin.value || !checkout.value) {
                alert('Please select both check‑in and check‑out dates.');
                e.preventDefault();
            }
        });
    }
}