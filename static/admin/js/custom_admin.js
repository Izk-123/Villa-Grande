// Villa Grande Admin — Modern Dashboard Experience v3.0
// Features: Count-up animations, real-time updates, fullscreen mode, toast notifications

document.addEventListener('DOMContentLoaded', function () {
    
    // ===== 1. Initialize AOS (Animation on Scroll) =====
    if (typeof AOS !== 'undefined') {
        AOS.refresh();
    }
    
    // ===== 2. Real-time Clock Update =====
    function updateClock() {
        const now = new Date();
        const options = { hour: '2-digit', minute: '2-digit', hour12: true };
        const timeString = now.toLocaleTimeString('en-US', options);
        const clockElement = document.getElementById('currentTime');
        if (clockElement) {
            clockElement.textContent = timeString;
        }
        
        // Update greeting based on hour
        const hour = now.getHours();
        let greeting = '';
        if (hour < 12) greeting = 'Good Morning';
        else if (hour < 18) greeting = 'Good Afternoon';
        else greeting = 'Good Evening';
        
        const greetingElement = document.querySelector('.clock-widget');
        if (greetingElement && !greetingElement.querySelector('.greeting-text')) {
            const greetingSpan = document.createElement('span');
            greetingSpan.className = 'greeting-text d-none d-lg-inline';
            greetingSpan.textContent = greeting;
            greetingElement.appendChild(greetingSpan);
        } else if (greetingElement) {
            const greetingSpan = greetingElement.querySelector('.greeting-text');
            if (greetingSpan) greetingSpan.textContent = greeting;
        }
    }
    
    updateClock();
    setInterval(updateClock, 1000);
    
    // ===== 3. Enhanced Dark Mode with System Preference =====
    const darkModeToggle = document.getElementById('darkModeToggle');
    const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');
    
    function setDarkMode(isDark) {
        if (isDark) {
            document.body.classList.add('dark-mode');
            localStorage.setItem('darkMode', 'true');
            if (darkModeToggle) {
                darkModeToggle.querySelector('i').className = 'bi bi-sun-fill';
            }
            // Update theme-color meta
            const themeMeta = document.querySelector('meta[name="theme-color"]');
            if (themeMeta) themeMeta.setAttribute('content', '#1a1a2e');
        } else {
            document.body.classList.remove('dark-mode');
            localStorage.setItem('darkMode', 'false');
            if (darkModeToggle) {
                darkModeToggle.querySelector('i').className = 'bi bi-moon-stars';
            }
            const themeMeta = document.querySelector('meta[name="theme-color"]');
            if (themeMeta) themeMeta.setAttribute('content', '#0A2342');
        }
    }
    
    // Load saved theme or system preference
    const savedDarkMode = localStorage.getItem('darkMode');
    if (savedDarkMode !== null) {
        setDarkMode(savedDarkMode === 'true');
    } else {
        setDarkMode(prefersDarkScheme.matches);
    }
    
    // Listen for system theme changes
    prefersDarkScheme.addEventListener('change', (e) => {
        if (localStorage.getItem('darkMode') === null) {
            setDarkMode(e.matches);
        }
    });
    
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', () => {
            setDarkMode(!document.body.classList.contains('dark-mode'));
            showToast('Theme changed successfully!', 'success');
        });
    }
    
    // ===== 4. Fullscreen Mode =====
    const fullscreenToggle = document.getElementById('fullscreenToggle');
    if (fullscreenToggle) {
        fullscreenToggle.addEventListener('click', () => {
            if (!document.fullscreenElement) {
                document.documentElement.requestFullscreen().then(() => {
                    fullscreenToggle.querySelector('i').className = 'bi bi-fullscreen-exit';
                    showToast('Fullscreen mode activated', 'info');
                }).catch(err => {
                    console.error(`Error: ${err.message}`);
                });
            } else {
                document.exitFullscreen().then(() => {
                    fullscreenToggle.querySelector('i').className = 'bi bi-arrows-fullscreen';
                    showToast('Exited fullscreen mode', 'info');
                });
            }
        });
        
        // Update fullscreen button icon on change
        document.addEventListener('fullscreenchange', () => {
            if (document.fullscreenElement) {
                fullscreenToggle.querySelector('i').className = 'bi bi-fullscreen-exit';
            } else {
                fullscreenToggle.querySelector('i').className = 'bi bi-arrows-fullscreen';
            }
        });
    }
    
    // ===== 5. Count-up Animation for Statistics =====
    function animateNumbers() {
        const statNumbers = document.querySelectorAll('.stat-number');
        statNumbers.forEach(el => {
            const finalValue = parseFloat(el.getAttribute('data-target') || el.textContent.replace(/[^0-9.-]/g, ''));
            if (!finalValue || el.classList.contains('counted')) return;
            
            const isCurrency = el.textContent.includes('$');
            const duration = 1000;
            const stepTime = 20;
            const steps = duration / stepTime;
            const increment = finalValue / steps;
            let current = 0;
            let step = 0;
            
            const counter = setInterval(() => {
                step++;
                current += increment;
                if (step >= steps) {
                    current = finalValue;
                    clearInterval(counter);
                    el.classList.add('counted');
                }
                if (isCurrency) {
                    el.textContent = '$' + Math.round(current).toLocaleString();
                } else {
                    el.textContent = Math.round(current).toLocaleString();
                }
            }, stepTime);
        });
    }
    
    // Intersection Observer for count-up
    const statsObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateNumbers();
                statsObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });
    
    document.querySelectorAll('.stat-number').forEach(el => {
        // Store original value as data-target
        if (!el.getAttribute('data-target')) {
            const originalValue = el.textContent.replace(/[^0-9.-]/g, '');
            el.setAttribute('data-target', originalValue);
        }
        statsObserver.observe(el);
    });
    
    // ===== 6. Toast Notification System =====
    function showToast(message, type = 'info') {
        const toastElement = document.getElementById('liveToast');
        const toastBody = document.getElementById('toastMessage');
        const toastHeader = toastElement.querySelector('.toast-header');
        
        if (!toastElement || !toastBody) return;
        
        // Set icon based on type
        const iconMap = {
            success: 'bi-check-circle-fill',
            error: 'bi-x-circle-fill',
            warning: 'bi-exclamation-triangle-fill',
            info: 'bi-info-circle-fill'
        };
        
        const icon = iconMap[type] || iconMap.info;
        toastHeader.querySelector('i').className = `bi ${icon} me-2`;
        
        // Set header color
        const colorMap = {
            success: '#10B981',
            error: '#EF4444',
            warning: '#F59E0B',
            info: '#3B82F6'
        };
        toastHeader.style.color = colorMap[type] || colorMap.info;
        
        toastBody.textContent = message;
        
        const bsToast = new bootstrap.Toast(toastElement, {
            autohide: true,
            delay: 3000
        });
        bsToast.show();
    }
    
    // Make showToast globally available
    window.showToast = showToast;
    
    // ===== 7. Enhanced Stats Refresh with Loading Skeletons =====
    if (document.querySelector('.dashboard-container')) {
        function createSkeleton() {
            const skeletons = document.querySelectorAll('.stat-number');
            skeletons.forEach(el => {
                if (!el.classList.contains('skeleton')) {
                    const width = el.offsetWidth;
                    const height = el.offsetHeight;
                    el.classList.add('skeleton');
                    el.style.width = `${width}px`;
                    el.style.height = `${height}px`;
                }
            });
        }
        
        function removeSkeleton() {
            document.querySelectorAll('.stat-number').forEach(el => {
                el.classList.remove('skeleton');
                el.style.width = '';
                el.style.height = '';
            });
        }
        
        async function refreshStats() {
            try {
                createSkeleton();
                
                const response = await fetch('/admin/dashboard/stats/');
                if (!response.ok) throw new Error('Network response was not ok');
                
                const data = await response.json();
                
                // Update stat cards
                const statMap = {
                    total_rooms: data.total_rooms,
                    active_rooms: data.active_rooms,
                    pending_bookings: data.pending_bookings,
                    confirmed_bookings: data.confirmed_bookings,
                    total_customers: data.total_customers,
                    monthly_revenue: '$' + Math.round(data.monthly_revenue)
                };
                
                for (const [key, value] of Object.entries(statMap)) {
                    const el = document.querySelector(`[data-stat="${key}"]`);
                    if (el) {
                        el.setAttribute('data-target', value.toString().replace(/[^0-9.-]/g, ''));
                        el.textContent = value;
                        el.classList.remove('counted');
                        statsObserver.observe(el);
                    }
                }
                
                // Update recent bookings table
                const tbody = document.getElementById('recent-bookings-tbody');
                if (tbody && data.recent_bookings) {
                    tbody.innerHTML = data.recent_bookings.map(booking => `
                        <tr data-aos="fade-up" data-aos-delay="100">
                            <th scope="row"><a href="/admin/lodge/booking/${booking.id}/change/" class="fw-bold">#${booking.id}</a></th>
                            <td><i class="bi bi-person-circle me-2"></i>${booking.customer}</td>
                            <td><i class="bi bi-door-closed me-2"></i>${booking.room}</td>
                            <td><i class="bi bi-calendar me-2"></i>${booking.check_in}</td>
                            <td><i class="bi bi-calendar me-2"></i>${booking.check_out}</td>
                            <td><span class="badge bg-${booking.status === 'CONFIRMED' ? 'success' : (booking.status === 'PENDING' ? 'warning' : 'danger')}">${booking.status_display}</span></td>
                        </tr>
                    `).join('');
                }
                
                // Update charts if they exist
                if (window.bookingTrendsChart && data.booking_trends) {
                    window.bookingTrendsChart.data.datasets[0].data = data.booking_trends;
                    window.bookingTrendsChart.update();
                }
                if (window.roomTypeChart && data.room_type_counts) {
                    window.roomTypeChart.data.datasets[0].data = data.room_type_counts;
                    window.roomTypeChart.update();
                }
                
                showToast('Dashboard data refreshed successfully!', 'success');
            } catch (error) {
                console.error('Error refreshing stats:', error);
                showToast('Failed to refresh dashboard data', 'error');
            } finally {
                removeSkeleton();
                animateNumbers();
            }
        }
        
        // Refresh every 30 seconds
        setInterval(refreshStats, 30000);
        refreshStats();
    }
    
    // ===== 8. Button Ripple Effect =====
    function createRipple(event) {
        const button = event.currentTarget;
        const ripple = document.createElement('span');
        const diameter = Math.max(button.clientWidth, button.clientHeight);
        const radius = diameter / 2;
        
        ripple.classList.add('ripple');
        ripple.style.width = ripple.style.height = `${diameter}px`;
        ripple.style.left = `${event.clientX - button.offsetLeft - radius}px`;
        ripple.style.top = `${event.clientY - button.offsetTop - radius}px`;
        
        button.style.position = 'relative';
        button.style.overflow = 'hidden';
        
        const existingRipple = button.querySelector('.ripple');
        if (existingRipple) existingRipple.remove();
        
        button.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 600);
    }
    
    document.querySelectorAll('.btn').forEach(btn => {
        btn.addEventListener('click', createRipple);
    });
    
    // ===== 9. Enhanced Chart Styling =====
    function enhanceCharts() {
        // Find all canvas elements that might have charts
        const canvases = document.querySelectorAll('canvas');
        canvases.forEach(canvas => {
            // Try to get Chart.js instance
            const chartInstance = Chart.getChart(canvas);
            if (chartInstance) {
                // Apply gradient fills to existing charts
                const ctx = canvas.getContext('2d');
                const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
                gradient.addColorStop(0, 'rgba(201, 168, 76, 0.5)');
                gradient.addColorStop(1, 'rgba(201, 168, 76, 0.1)');
                
                if (chartInstance.config.type === 'line' || chartInstance.config.type === 'bar') {
                    chartInstance.data.datasets.forEach(dataset => {
                        if (!dataset.backgroundColor || dataset.backgroundColor === 'rgba(0,0,0,0.1)') {
                            dataset.backgroundColor = gradient;
                        }
                        if (!dataset.borderColor) {
                            dataset.borderColor = '#C9A84C';
                        }
                        dataset.borderWidth = 2;
                        dataset.pointBackgroundColor = '#C9A84C';
                        dataset.pointBorderColor = '#fff';
                        dataset.pointRadius = 4;
                        dataset.pointHoverRadius = 6;
                    });
                    chartInstance.update();
                }
            }
        });
    }
    
    // Run chart enhancement after a delay to ensure charts are initialized
    setTimeout(enhanceCharts, 1000);
    
    // ===== 10. Keyboard Shortcuts =====
    document.addEventListener('keydown', (e) => {
        // Alt + F for fullscreen
        if (e.altKey && e.key === 'f') {
            e.preventDefault();
            if (fullscreenToggle) fullscreenToggle.click();
        }
        // Alt + D for dark mode
        if (e.altKey && e.key === 'd') {
            e.preventDefault();
            if (darkModeToggle) darkModeToggle.click();
        }
        // Ctrl + / for search focus
        if ((e.ctrlKey || e.metaKey) && e.key === '/') {
            e.preventDefault();
            const searchInput = document.querySelector('.search-form input');
            if (searchInput) searchInput.focus();
        }
    });
    
    // ===== 11. Smooth Page Transitions (FIXED: exclude dropdowns and hash links) =====
    document.querySelectorAll('a').forEach(link => {
        // Skip any link that is a Bootstrap dropdown toggle, has href="#", javascript:void(0), or dropdown-toggle class
        if (link.hasAttribute('data-bs-toggle') || 
            link.classList.contains('dropdown-toggle') ||
            link.getAttribute('href') === '#' || 
            link.getAttribute('href') === 'javascript:void(0)' ||
            link.getAttribute('href') === 'javascript:void(0);') {
            return; // Do not attach smooth transition to these links
        }
        
        // Only apply to internal links that are not blank targets
        if (link.hostname === window.location.hostname && link.target !== '_blank') {
            link.addEventListener('click', (e) => {
                const destination = link.href;
                if (destination !== window.location.href) {
                    e.preventDefault();
                    document.body.style.opacity = '0';
                    setTimeout(() => {
                        window.location.href = destination;
                    }, 300);
                }
            });
        }
    });
    
    // ===== 12. Live Search Animation =====
    const searchInput = document.querySelector('.search-form input');
    if (searchInput) {
        searchInput.addEventListener('focus', () => {
            searchInput.parentElement.classList.add('focused');
        });
        searchInput.addEventListener('blur', () => {
            searchInput.parentElement.classList.remove('focused');
        });
    }
    
    // ===== 13. Initialize Tooltips =====
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    
    // ===== 14. Welcome Toast on First Visit =====
    if (!localStorage.getItem('welcomeShown')) {
        setTimeout(() => {
            const userName = document.querySelector('.nav-profile span')?.textContent || 'Admin';
            showToast(`Welcome back, ${userName}! 👋`, 'success');
            localStorage.setItem('welcomeShown', 'true');
        }, 1500);
    }
    
    console.log('✨ Villa Grande Admin Dashboard v3.0 — Modern features loaded!');
});