document.addEventListener('DOMContentLoaded', () => {
    
  // --- Elements Selector ---
  const menuToggle = document.getElementById('menuToggle');
  const sidebarMenu = document.getElementById('sidebarMenu');
  const menuOverlay = document.getElementById('menuOverlay');
  const searchBar = document.getElementById('searchBar');
  const contentGrid = document.getElementById('contentGrid');
  const cards = contentGrid.getElementsByClassName('placeholder-card');
  
  const popularBtn = document.getElementById('popularBtn');
  const menuPopularBtn = document.getElementById('menuPopularBtn');
  const popularModal = document.getElementById('popularModal');
  const modalOverlay = document.getElementById('modalOverlay');
  const modalClose = document.getElementById('modalClose');

  // Create a single state-managed instance of a "No Results" message
  const noResultsMsg = document.createElement('div');
  noResultsMsg.className = 'no-results';
  noResultsMsg.textContent = 'No matching placeholders found.';
  noResultsMsg.style.display = 'none';
  contentGrid.appendChild(noResultsMsg);

  // --- Sidebar Menu Logic ---
  function toggleMenu() {
      const isOpen = sidebarMenu.classList.toggle('active');
      menuToggle.classList.toggle('active');
      menuOverlay.classList.toggle('active');
      document.body.style.overflow = isOpen ? 'hidden' : '';
  }

  function closeMenu() {
      sidebarMenu.classList.remove('active');
      menuToggle.classList.remove('active');
      menuOverlay.classList.remove('active');
      document.body.style.overflow = '';
  }

  menuToggle.addEventListener('click', toggleMenu);
  menuOverlay.addEventListener('click', closeMenu);

  // --- Modal Architecture ---
  function openModal(e) {
      e.preventDefault();
      closeMenu(); // Safety check if clicked from inside the sidebar
      popularModal.classList.add('active');
      modalOverlay.classList.add('active');
      document.body.style.overflow = 'hidden';
  }

  function closeModal() {
      popularModal.classList.remove('active');
      modalOverlay.classList.remove('active');
      if (!sidebarMenu.classList.contains('active')) {
          document.body.style.overflow = '';
      }
  }

  popularBtn.addEventListener('click', openModal);
  menuPopularBtn.addEventListener('click', openModal);
  modalClose.addEventListener('click', closeModal);
  modalOverlay.addEventListener('click', closeModal);

  // --- Functional Filter Engine ---
  searchBar.addEventListener('input', (e) => {
      const query = e.target.value.toLowerCase().trim();
      let matches = 0;

      Array.from(cards).forEach(card => {
          const searchableText = card.getAttribute('data-search') || '';
          
          if (searchableText.includes(query)) {
              card.style.display = 'block';
              matches++;
          } else {
              card.style.display = 'none';
          }
      });

      // Display text if even placeholders get filtered out completely
      if (matches === 0) {
          noResultsMsg.style.display = 'block';
      } else {
          noResultsMsg.style.display = 'none';
      }
  });

  // Escape Key Handler for Accessibility (Closes open layers)
  window.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
          closeModal();
          closeMenu();
      }
  });
});
const themeToggle = document.getElementById("themeToggle");

// Default = DARK MODE (no class needed)

if (localStorage.getItem("theme") === "light") {
    document.body.classList.add("light");
    themeToggle.innerText = "🌙";
} else {
    themeToggle.innerText = "☀️";
}

themeToggle.addEventListener("click", () => {
    document.body.classList.toggle("light");

    if (document.body.classList.contains("light")) {
        localStorage.setItem("theme", "light");
        themeToggle.innerText = "🌙";
    } else {
        localStorage.setItem("theme", "dark");
        themeToggle.innerText = "☀️";
    }
});