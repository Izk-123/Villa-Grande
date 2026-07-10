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
    //  HERO SLIDER — FIXED with debug logs and content handling
    // ============================================================
    function initHeroSlider() {
        const slides = document.querySelectorAll(".hero-slide");
        const dots = document.querySelectorAll(".hero-dot");
        const contents = document.querySelectorAll(".hero-slide-content");

        if (!slides.length) {
            console.warn("No hero slides found");
            return;
        }

        console.log(`Found ${slides.length} hero slides`);

        let heroSlideIndex = 0;
        let heroTimer = null;

        function showSlide(n) {
            // Remove active from all slides and dots
            slides.forEach(function (s) { s.classList.remove("active"); });
            dots.forEach(function (d) { d.classList.remove("active"); });
            // Hide all content blocks
            contents.forEach(function (c) { c.style.display = "none"; });

            // Calculate new index
            heroSlideIndex = (n + slides.length) % slides.length;

            // Activate current slide and dot
            slides[heroSlideIndex].classList.add("active");
            if (dots[heroSlideIndex]) {
                dots[heroSlideIndex].classList.add("active");
            }

            // Show the matching content block (if it exists)
            var content = document.querySelector('.hero-slide-content[data-slide="' + heroSlideIndex + '"]');
            if (content) {
                content.style.display = "block";
            } else {
                // Fallback: if no content matches, show the first content (or none)
                // In your HTML, each content has data-slide attribute
                console.warn("No content block found for slide index", heroSlideIndex);
            }

            console.log("Showing slide", heroSlideIndex);
        }

        function startTimer() {
            if (heroTimer) clearInterval(heroTimer);
            heroTimer = setInterval(function () {
                console.log("Timer tick – moving to next slide");
                showSlide(heroSlideIndex + 1);
            }, 6000);
            console.log("Timer started");
        }

        // Initialise: show first slide
        showSlide(0);
        startTimer();

        // Dot clicks
        dots.forEach(function (dot, index) {
            dot.addEventListener("click", function () {
                clearInterval(heroTimer);
                showSlide(index);
                startTimer();
            });
        });

        // Keyboard arrows
        document.addEventListener("keydown", function (e) {
            if (e.key === "ArrowLeft") {
                clearInterval(heroTimer);
                showSlide(heroSlideIndex - 1);
                startTimer();
            } else if (e.key === "ArrowRight") {
                clearInterval(heroTimer);
                showSlide(heroSlideIndex + 1);
                startTimer();
            }
        });

        // Touch swipe
        var heroEl = document.querySelector(".hero-section");
        if (heroEl) {
            var touchStartX = 0;
            heroEl.addEventListener("touchstart", function (e) {
                touchStartX = e.changedTouches[0].screenX;
            }, { passive: true });
            heroEl.addEventListener("touchend", function (e) {
                var diff = touchStartX - e.changedTouches[0].screenX;
                if (Math.abs(diff) > 50) {
                    clearInterval(heroTimer);
                    showSlide(heroSlideIndex + (diff > 0 ? 1 : -1));
                    startTimer();
                }
            }, { passive: true });
        }

        // Pause on visibility change
        document.addEventListener("visibilitychange", function () {
            if (document.hidden) {
                clearInterval(heroTimer);
                console.log("Timer paused");
            } else {
                startTimer();
                console.log("Timer resumed");
            }
        });
    }

    // ============================================================
    //  COUNTER ANIMATION
    // ============================================================
    function initCounters() {
        if (!("IntersectionObserver" in window)) return;
        var counters = document.querySelectorAll("[data-target]");
        if (!counters.length) return;
        var observer = new IntersectionObserver(
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
        var target = parseInt(el.getAttribute("data-target"), 10);
        var duration = 2200;
        var frameRate = 16;
        var totalFrames = Math.round(duration / frameRate);
        var frame = 0;
        function easeOutCubic(t) { return 1 - Math.pow(1 - t, 3); }
        var timer = setInterval(function () {
            frame++;
            var progress = easeOutCubic(frame / totalFrames);
            var current = Math.round(progress * target);
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
        var btt = document.getElementById("backToTop") || document.querySelector(".back-to-top-vg, .back-to-top");
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
        var modalEl = document.getElementById("videoModal");
        if (!modalEl) return;
        modalEl.addEventListener("show.bs.modal", function (e) {
            var btn = e.relatedTarget;
            var src = btn.getAttribute("data-src") || "https://www.youtube.com/embed/DWRcNpR6Kdc";
            var iframe = document.getElementById("videoFrame");
            if (iframe) iframe.src = src + "?autoplay=1&modestbranding=1&showinfo=0";
        });
        modalEl.addEventListener("hide.bs.modal", function () {
            var iframe = document.getElementById("videoFrame");
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
                    var menu = this.querySelector(".dropdown-menu");
                    var toggle = this.querySelector(".dropdown-toggle");
                    if (menu) menu.classList.add("show");
                    if (toggle) toggle.setAttribute("aria-expanded", "true");
                });
                dropdown.addEventListener("mouseleave", function () {
                    var menu = this.querySelector(".dropdown-menu");
                    var toggle = this.querySelector(".dropdown-toggle");
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
        var checkin = document.getElementById("checkin");
        var checkout = document.getElementById("checkout");
        if (!checkin || !checkout) return;
        var today = new Date();
        var tomorrow = new Date(today);
        tomorrow.setDate(today.getDate() + 1);
        function fmt(d) { return d.toISOString().split("T")[0]; }
        checkin.value = fmt(today);
        checkout.value = fmt(tomorrow);
        checkin.min = fmt(today);
        checkout.min = fmt(tomorrow);
        checkin.addEventListener("change", function () {
            var ci = new Date(this.value);
            var co = new Date(ci);
            co.setDate(ci.getDate() + 1);
            checkout.min = fmt(co);
            if (new Date(checkout.value) <= ci) checkout.value = fmt(co);
        });
    }

    // ============================================================
    //  PARALLAX — with resize + rAF
    // ============================================================
    var parallaxEnabled = window.innerWidth >= 992;
    var parallaxTicking = false;

    function initParallax() {
        var heroSlides = document.querySelectorAll(".hero-slide");
        if (!heroSlides.length) return;

        function onResize() {
            parallaxEnabled = window.innerWidth >= 992;
        }

        function onScroll() {
            if (!parallaxTicking) {
                requestAnimationFrame(function () {
                    if (!parallaxEnabled) return;
                    var y = window.scrollY * 0.3;
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
        var path = window.location.pathname.split("/").pop() || "index.html";
        document.querySelectorAll(".navbar .nav-link").forEach(function (link) {
            var href = (link.getAttribute("href") || "").split("/").pop();
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
            var btn = e.target.closest(".btn-vg-primary, .btn-vg-outline, .btn-primary, .btn-secondary");
            if (!btn) return;
            var ripple = document.createElement("span");
            var rect = btn.getBoundingClientRect();
            var size = Math.max(rect.width, rect.height);
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
        var style = document.createElement("style");
        style.id = "ripple-style";
        style.textContent = "@keyframes rippleEffect{to{transform:scale(2.5);opacity:0;}}";
        document.head.appendChild(style);
    }
})();