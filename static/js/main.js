/**
 * Villa Grande Lodge — Main JavaScript
 * Responsive fixes: mobile-menu close, parallax resize, passive touch
 */
(function () {
    "use strict";

    document.addEventListener("DOMContentLoaded", function () {
        initLoader();
        initScrollReveal();
        initNavbar();
        initHeroSlider();
        initCounters();
        initBackToTop();
        initVideoModal();
        initDropdownHover();
        initBookingDateDefaults();
        initParallax();
        setActiveNavLink();
        initRippleEffect();
        initMobileMenuClose();
    });

    // ============================================================
    //  LOADER
    // ============================================================
    function initLoader() {
        const loader = document.getElementById("vg-loader");
        if (!loader) return;
        window.addEventListener("load", function () {
            setTimeout(function () {
                loader.classList.add("fade-out");
                loader.addEventListener("transitionend", function () {
                    loader.style.display = "none";
                }, { once: true });
            }, 3400);
        });
    }

    // ============================================================
    //  SCROLL REVEAL
    // ============================================================
    function initScrollReveal() {
        if (!("IntersectionObserver" in window)) {
            document.querySelectorAll(".reveal, .reveal-left, .reveal-right, .reveal-scale")
                .forEach(function (el) { el.classList.add("visible"); });
            return;
        }
        const observer = new IntersectionObserver(
            function (entries) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        entry.target.classList.add("visible");
                    }
                });
            },
            { threshold: 0.1, rootMargin: "0px 0px -40px 0px" }
        );
        document.querySelectorAll(".reveal, .reveal-left, .reveal-right, .reveal-scale")
            .forEach(function (el) { observer.observe(el); });
    }

    // ============================================================
    //  NAVBAR — sticky + scroll class
    // ============================================================
    function initNavbar() {
        const nav = document.getElementById("mainNav") || document.querySelector(".navbar-vg");
        if (!nav) return;
        function onScroll() {
            if (window.scrollY > 60) {
                nav.classList.add("scrolled");
            } else {
                nav.classList.remove("scrolled");
            }
        }
        window.addEventListener("scroll", onScroll, { passive: true });
        onScroll();
    }

    // ============================================================
    //  MOBILE MENU — close on link click
    // ============================================================
    function initMobileMenuClose() {
        const navLinks = document.querySelectorAll(".navbar-vg .nav-link");
        const navbarCollapse = document.querySelector(".navbar-collapse");
        const toggler = document.querySelector(".navbar-toggler");

        if (!navbarCollapse || !toggler) return;

        navLinks.forEach(function (link) {
            link.addEventListener("click", function () {
                if (window.innerWidth < 992 && navbarCollapse.classList.contains("show")) {
                    // Use Bootstrap collapse API if available, else manual toggle
                    if (window.bootstrap && window.bootstrap.Collapse) {
                        const bsCollapse = window.bootstrap.Collapse.getInstance(navbarCollapse);
                        if (bsCollapse) bsCollapse.hide();
                    } else {
                        toggler.click();
                    }
                }
            });
        });
    }

    // ============================================================
    //  HERO SLIDER
    // ============================================================
    let heroSlideIndex = 0;
    let heroTimer = null;
    const slides = document.querySelectorAll(".hero-slide");
    const dots = document.querySelectorAll(".hero-dot");

    function initHeroSlider() {
        if (!slides.length) return;

        function showSlide(n) {
            slides[heroSlideIndex].classList.remove("active");
            if (dots[heroSlideIndex]) dots[heroSlideIndex].classList.remove("active");
            heroSlideIndex = (n + slides.length) % slides.length;
            slides[heroSlideIndex].classList.add("active");
            if (dots[heroSlideIndex]) dots[heroSlideIndex].classList.add("active");
        }

        window.goToSlide = function (n) {
            clearInterval(heroTimer);
            showSlide(n);
            startTimer();
        };

        function startTimer() {
            heroTimer = setInterval(function () { showSlide(heroSlideIndex + 1); }, 6000);
        }
        startTimer();

        dots.forEach((dot, index) => {
            dot.addEventListener("click", () => window.goToSlide(index));
        });

        document.addEventListener("keydown", (e) => {
            if (e.key === "ArrowLeft") window.goToSlide(heroSlideIndex - 1);
            else if (e.key === "ArrowRight") window.goToSlide(heroSlideIndex + 1);
        });

        // Touch swipe — improved with passive listeners
        const heroEl = document.querySelector(".hero-section");
        if (heroEl) {
            let touchStartX = 0;
            heroEl.addEventListener("touchstart", (e) => {
                touchStartX = e.changedTouches[0].screenX;
            }, { passive: true });
            heroEl.addEventListener("touchend", (e) => {
                const diff = touchStartX - e.changedTouches[0].screenX;
                if (Math.abs(diff) > 50) {
                    window.goToSlide(heroSlideIndex + (diff > 0 ? 1 : -1));
                }
            }, { passive: true });
        }

        document.addEventListener("visibilitychange", () => {
            if (document.hidden) clearInterval(heroTimer);
            else startTimer();
        });
    }

    // ============================================================
    //  COUNTER ANIMATION
    // ============================================================
    function initCounters() {
        if (!("IntersectionObserver" in window)) return;
        const counters = document.querySelectorAll("[data-target]");
        if (!counters.length) return;
        const observer = new IntersectionObserver(
            function (entries) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        animateCounter(entry.target);
                        observer.unobserve(entry.target);
                    }
                });
            },
            { threshold: 0.4 }
        );
        counters.forEach(function (el) { observer.observe(el); });
    }

    function animateCounter(el) {
        const target = parseInt(el.getAttribute("data-target"), 10);
        const duration = 2200;
        const frameRate = 16;
        const totalFrames = Math.round(duration / frameRate);
        let frame = 0;
        function easeOutCubic(t) { return 1 - Math.pow(1 - t, 3); }
        const timer = setInterval(function () {
            frame++;
            const progress = easeOutCubic(frame / totalFrames);
            const current = Math.round(progress * target);
            el.textContent = current.toLocaleString() + "+";
            if (frame >= totalFrames) {
                el.textContent = target.toLocaleString() + "+";
                clearInterval(timer);
            }
        }, frameRate);
    }

    // ============================================================
    //  BACK TO TOP
    // ============================================================
    function initBackToTop() {
        const btt = document.getElementById("backToTop") || document.querySelector(".back-to-top-vg, .back-to-top");
        if (!btt) return;
        window.addEventListener("scroll", function () {
            if (window.scrollY > 400) btt.classList.add("visible");
            else btt.classList.remove("visible");
        }, { passive: true });
        btt.addEventListener("click", function (e) {
            e.preventDefault();
            window.scrollTo({ top: 0, behavior: "smooth" });
        });
    }

    // ============================================================
    //  VIDEO MODAL
    // ============================================================
    function initVideoModal() {
        const modalEl = document.getElementById("videoModal");
        if (!modalEl) return;
        modalEl.addEventListener("show.bs.modal", function (e) {
            const btn = e.relatedTarget;
            const src = btn.getAttribute("data-src") || "https://www.youtube.com/embed/DWRcNpR6Kdc";
            const iframe = document.getElementById("videoFrame");
            if (iframe) iframe.src = src + "?autoplay=1&modestbranding=1&showinfo=0";
        });
        modalEl.addEventListener("hide.bs.modal", function () {
            const iframe = document.getElementById("videoFrame");
            if (iframe) iframe.src = "";
        });
    }

    // ============================================================
    //  DROPDOWN HOVER (desktop only)
    // ============================================================
    function initDropdownHover() {
        function applyHover() {
            if (window.innerWidth < 992) return;
            document.querySelectorAll(".navbar .dropdown").forEach(function (dropdown) {
                dropdown.addEventListener("mouseenter", function () {
                    const menu = this.querySelector(".dropdown-menu");
                    const toggle = this.querySelector(".dropdown-toggle");
                    if (menu) menu.classList.add("show");
                    if (toggle) toggle.setAttribute("aria-expanded", "true");
                });
                dropdown.addEventListener("mouseleave", function () {
                    const menu = this.querySelector(".dropdown-menu");
                    const toggle = this.querySelector(".dropdown-toggle");
                    if (menu) menu.classList.remove("show");
                    if (toggle) toggle.setAttribute("aria-expanded", "false");
                });
            });
        }
        window.addEventListener("load", applyHover);
        window.addEventListener("resize", applyHover);
    }

    // ============================================================
    //  BOOKING BAR — smart date defaults
    // ============================================================
    function initBookingDateDefaults() {
        const checkin = document.getElementById("checkin");
        const checkout = document.getElementById("checkout");
        if (!checkin || !checkout) return;
        const today = new Date();
        const tomorrow = new Date(today);
        tomorrow.setDate(today.getDate() + 1);
        function fmt(d) { return d.toISOString().split("T")[0]; }
        checkin.value = fmt(today);
        checkout.value = fmt(tomorrow);
        checkin.min = fmt(today);
        checkout.min = fmt(tomorrow);
        checkin.addEventListener("change", function () {
            const ci = new Date(this.value);
            const co = new Date(ci);
            co.setDate(ci.getDate() + 1);
            checkout.min = fmt(co);
            if (new Date(checkout.value) <= ci) checkout.value = fmt(co);
        });
    }

    // ============================================================
    //  PARALLAX — now with resize + rAF
    // ============================================================
    let parallaxEnabled = window.innerWidth >= 992;
    let parallaxTicking = false;

    function initParallax() {
        const heroSlides = document.querySelectorAll(".hero-slide");
        if (!heroSlides.length) return;

        function onResize() {
            parallaxEnabled = window.innerWidth >= 992;
        }

        function onScroll() {
            if (!parallaxTicking) {
                requestAnimationFrame(function () {
                    if (!parallaxEnabled) return;
                    const y = window.scrollY * 0.3;
                    heroSlides.forEach(function (slide) {
                        slide.style.transform =
                            "scale(" +
                            (slide.classList.contains("active") ? 1 : 1.08) +
                            ") translateY(" + y + "px)";
                    });
                    parallaxTicking = false;
                });
                parallaxTicking = true;
            }
        }

        window.addEventListener("resize", onResize, { passive: true });
        window.addEventListener("scroll", onScroll, { passive: true });
    }

    // ============================================================
    //  ACTIVE NAV LINK
    // ============================================================
    function setActiveNavLink() {
        const path = window.location.pathname.split("/").pop() || "index.html";
        document.querySelectorAll(".navbar .nav-link").forEach(function (link) {
            const href = (link.getAttribute("href") || "").split("/").pop();
            if (href === path || (path === "" && href === "index.html")) {
                link.classList.add("active");
            }
        });
    }

    // ============================================================
    //  RIPPLE EFFECT
    // ============================================================
    function initRippleEffect() {
        document.addEventListener("click", function (e) {
            const btn = e.target.closest(".btn-vg-primary, .btn-vg-outline, .btn-primary, .btn-secondary");
            if (!btn) return;
            const ripple = document.createElement("span");
            const rect = btn.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            ripple.style.cssText =
                "position:absolute;border-radius:50%;pointer-events:none;" +
                "width:" + size + "px;height:" + size + "px;" +
                "left:" + (e.clientX - rect.left - size / 2) + "px;" +
                "top:" + (e.clientY - rect.top - size / 2) + "px;" +
                "background:rgba(255,255,255,0.2);transform:scale(0);" +
                "animation:rippleEffect 0.5s ease;";
            if (getComputedStyle(btn).position === "static") {
                btn.style.position = "relative";
            }
            btn.style.overflow = "hidden";
            btn.appendChild(ripple);
            setTimeout(function () { ripple.remove(); }, 500);
        });
    }

    if (!document.getElementById("ripple-style")) {
        const style = document.createElement("style");
        style.id = "ripple-style";
        style.textContent = "@keyframes rippleEffect{to{transform:scale(2.5);opacity:0;}}";
        document.head.appendChild(style);
    }
})();