/* ============================================================
   MODIFYA — script.js
   ============================================================ */

// ── Header scroll shadow ──────────────────────────────────────
const header = document.getElementById('header');
const onScroll = () => {
  header.classList.toggle('scrolled', window.scrollY > 10);
};
window.addEventListener('scroll', onScroll, { passive: true });

// ── Mobile burger menu ────────────────────────────────────────
const burger    = document.getElementById('burger');
const mobileNav = document.getElementById('mobileNav');

burger.addEventListener('click', () => {
  const open = mobileNav.classList.toggle('open');
  burger.setAttribute('aria-expanded', open);
  // Animate burger → X
  const spans = burger.querySelectorAll('span');
  if (open) {
    spans[0].style.transform = 'translateY(7px) rotate(45deg)';
    spans[1].style.opacity   = '0';
    spans[2].style.transform = 'translateY(-7px) rotate(-45deg)';
  } else {
    spans.forEach(s => { s.style.transform = ''; s.style.opacity = ''; });
  }
});

// Close mobile nav when a link is clicked
mobileNav.querySelectorAll('.mobile-nav__link').forEach(link => {
  link.addEventListener('click', () => {
    mobileNav.classList.remove('open');
    burger.setAttribute('aria-expanded', false);
    burger.querySelectorAll('span').forEach(s => { s.style.transform = ''; s.style.opacity = ''; });
  });
});

// ── Real-time search ──────────────────────────────────────────
const searchInput      = document.getElementById('searchInput');
const searchClear      = document.getElementById('searchClear');
const booksGrid        = document.getElementById('booksGrid');
const noResults        = document.getElementById('noResults');
const noResultsQuery   = document.getElementById('noResultsQuery');
const searchResultsBar = document.getElementById('searchResultsBar');
const searchResultsTxt = document.getElementById('searchResultsText');
const clearSearchBtn   = document.getElementById('clearSearchBtn');
const noResultsClear   = document.getElementById('noResultsClear');

// Gather all book cards (excluding the no-results placeholder)
const allBookCards = () => [...booksGrid.querySelectorAll('.book-card')];

function runSearch(query) {
  const q = query.trim().toLowerCase();
  const cards = allBookCards();

  // Show/hide clear button
  searchClear.classList.toggle('visible', q.length > 0);

  if (!q) {
    // Show everything
    cards.forEach(c => { c.style.display = ''; });
    noResults.style.display = 'none';
    searchResultsBar.style.display = 'none';
    return;
  }

  let visible = 0;
  cards.forEach(card => {
    const title = card.dataset.title.toLowerCase();
    const match = title.includes(q);
    card.style.display = match ? '' : 'none';
    if (match) visible++;
  });

  // Show results bar
  searchResultsBar.style.display = 'flex';
  searchResultsTxt.innerHTML = `Showing <strong>${visible}</strong> result${visible !== 1 ? 's' : ''} for "<strong>${escapeHtml(query.trim())}</strong>"`;

  // No results
  if (visible === 0) {
    noResults.style.display = 'flex';
    noResultsQuery.textContent = query.trim();
  } else {
    noResults.style.display = 'none';
  }

  // Scroll to book section
  if (q.length >= 2) {
    document.getElementById('books').scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
}

function clearSearch() {
  searchInput.value = '';
  runSearch('');
  searchInput.focus();
}

searchInput.addEventListener('input', (e) => runSearch(e.target.value));
searchClear.addEventListener('click', clearSearch);
clearSearchBtn.addEventListener('click', clearSearch);
noResultsClear.addEventListener('click', clearSearch);

// ── Escape HTML helper ────────────────────────────────────────
function escapeHtml(str) {
  return str.replace(/[&<>"']/g, m => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  })[m]);
}

// ── Smooth scroll for nav links ───────────────────────────────
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      e.preventDefault();
      const offset = 80; // header height
      const top = target.getBoundingClientRect().top + window.scrollY - offset;
      window.scrollTo({ top, behavior: 'smooth' });
    }
  });
});

// ── Intersection Observer: fade-in on scroll ──────────────────
const fadeObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.style.opacity = '1';
      entry.target.style.transform = 'translateY(0)';
      fadeObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.1, rootMargin: '0px 0px -30px 0px' });

document.querySelectorAll('.book-card, .featured-card').forEach(card => {
  // Start hidden for scroll reveal (CSS animation handles above-fold)
  // Only apply to cards that are below the fold on load
  if (card.getBoundingClientRect().top > window.innerHeight) {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'opacity 0.45s ease, transform 0.45s ease';
    fadeObserver.observe(card);
  }
});

// ── Active nav link on scroll ─────────────────────────────────
const sections = document.querySelectorAll('section[id]');
const navLinks  = document.querySelectorAll('.nav__link');

const navObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const id = entry.target.id;
      navLinks.forEach(link => {
        const href = link.getAttribute('href').replace('#', '');
        link.style.color = (href === id) ? 'var(--clr-accent)' : '';
        link.style.background = (href === id) ? 'var(--clr-accent-lt)' : '';
      });
    }
  });
}, { rootMargin: '-40% 0px -55% 0px' });

sections.forEach(s => navObserver.observe(s));

// ── Book card "Read Free" click tracking (console log) ────────
document.querySelectorAll('.book-card').forEach(card => {
  const readBtn = card.querySelector('a[href="unlock.html"]');
  if (readBtn) {
    readBtn.addEventListener('click', () => {
      const title = card.dataset.title;
      console.log(`[Modifya] Read Free clicked: "${title}"`);
      // Replace console.log with your analytics/CPA tracking pixel here
    });
  }
});