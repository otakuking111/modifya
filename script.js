/* ============================================================
   MODIFYA — script.js
   Interactions: theme toggle, nav scroll, animations,
   star rating, review form, FAQ, footer year
   ============================================================ */

   (function () {
    'use strict';
  
    /* ──────────────────────────────────────────
       1. THEME TOGGLE
    ────────────────────────────────────────── */
    const html = document.documentElement;
    const themeToggle = document.getElementById('themeToggle');
    const STORAGE_KEY = 'modifya-theme';
  
    const savedTheme = localStorage.getItem(STORAGE_KEY);
    if (savedTheme) {
      html.setAttribute('data-theme', savedTheme);
    }
  
    if (themeToggle) {
      themeToggle.addEventListener('click', () => {
        const current = html.getAttribute('data-theme') || 'dark';
        const next = current === 'dark' ? 'light' : 'dark';
        html.setAttribute('data-theme', next);
        localStorage.setItem(STORAGE_KEY, next);
      });
    }
  
  
    /* ──────────────────────────────────────────
       2. NAV — SCROLL EFFECT
    ────────────────────────────────────────── */
    const nav = document.getElementById('nav');
  
    function updateNav() {
      if (!nav) return;
      if (window.scrollY > 40) {
        nav.classList.add('nav--scrolled');
      } else {
        nav.classList.remove('nav--scrolled');
      }
    }
  
    window.addEventListener('scroll', updateNav, { passive: true });
    updateNav();
  
  
    /* ──────────────────────────────────────────
       3. SCROLL ANIMATIONS
    ────────────────────────────────────────── */
    const animatedEls = document.querySelectorAll('[data-animate]');
  
    if ('IntersectionObserver' in window) {
      const observer = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              entry.target.classList.add('is-visible');
              observer.unobserve(entry.target);
            }
          });
        },
        { threshold: 0.1, rootMargin: '0px 0px -40px 0px' }
      );
      animatedEls.forEach((el) => observer.observe(el));
    } else {
      animatedEls.forEach((el) => el.classList.add('is-visible'));
    }
  
  
    /* ──────────────────────────────────────────
       4. STAR RATING (kept for when reviews activate)
    ────────────────────────────────────────── */
    const starContainer = document.getElementById('starRating');
    const ratingInput   = document.getElementById('ratingValue');
  
    if (starContainer && ratingInput) {
      const stars = starContainer.querySelectorAll('.star');
      let selectedRating = 0;
  
      function setStars(value, isHover) {
        stars.forEach((star) => {
          const v = parseInt(star.dataset.value, 10);
          star.classList.remove('active', 'hover');
          if (v <= value) star.classList.add(isHover ? 'hover' : 'active');
        });
      }
  
      stars.forEach((star) => {
        star.addEventListener('mouseenter', () => setStars(parseInt(star.dataset.value, 10), true));
        star.addEventListener('mouseleave', () => setStars(selectedRating, false));
        star.addEventListener('click', () => {
          selectedRating = parseInt(star.dataset.value, 10);
          ratingInput.value = selectedRating;
          setStars(selectedRating, false);
        });
      });
    }
  
  
    /* ──────────────────────────────────────────
       5. REVIEW FORM (kept for when reviews activate)
    ────────────────────────────────────────── */
    const reviewForm   = document.getElementById('reviewForm');
    const reviewNotice = document.getElementById('reviewNotice');
  
    if (reviewForm) {
      reviewForm.addEventListener('submit', (e) => {
        e.preventDefault();
        if (reviewNotice) {
          reviewNotice.textContent = 'Review submissions will be available soon.';
          reviewNotice.style.opacity = '0';
          reviewNotice.style.transform = 'translateY(6px)';
          reviewNotice.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
          void reviewNotice.offsetWidth;
          reviewNotice.style.opacity = '1';
          reviewNotice.style.transform = 'translateY(0)';
        }
      });
    }
  
  
    /* ──────────────────────────────────────────
       6. FREE BUTTON — connect to your Content Locker
    ────────────────────────────────────────── */
    const freeBtn = document.getElementById('freeBtn');
    if (freeBtn) {
      freeBtn.addEventListener('click', () => {
        // TODO: Connect to your Content Locker here
        // e.g. window.location.href = 'YOUR_CONTENT_LOCKER_URL';
      });
    }
  
  
    /* ──────────────────────────────────────────
       7. FOOTER YEAR
    ────────────────────────────────────────── */
    const yearEl = document.getElementById('footerYear');
    if (yearEl) yearEl.textContent = new Date().getFullYear();
  
  
    /* ──────────────────────────────────────────
       8. SMOOTH ANCHOR SCROLLING (offset for fixed nav)
    ────────────────────────────────────────── */
    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
      anchor.addEventListener('click', function (e) {
        const target = document.querySelector(this.getAttribute('href'));
        if (!target) return;
        e.preventDefault();
        const navHeight = nav ? nav.offsetHeight : 64;
        const top = target.getBoundingClientRect().top + window.scrollY - navHeight - 16;
        window.scrollTo({ top, behavior: 'smooth' });
      });
    });
  
  })();