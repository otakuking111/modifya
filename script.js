// THEME
const themeToggle = document.getElementById("themeToggle");

if (localStorage.getItem("theme") === "light") {
  document.body.classList.add("light");
  themeToggle.innerText = "🌙";
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

// MENU
const menuToggle = document.getElementById("menuToggle");
const sidebar = document.getElementById("sidebar");
const overlay = document.getElementById("overlay");

menuToggle.onclick = () => {
  sidebar.classList.toggle("active");
  overlay.classList.toggle("active");
};

overlay.onclick = () => {
  sidebar.classList.remove("active");
  overlay.classList.remove("active");
};

// MODAL
const modal = document.getElementById("modal");

document.getElementById("openModal").onclick = () => {
  modal.classList.add("active");
};

document.getElementById("closeModal").onclick = () => {
  modal.classList.remove("active");
};