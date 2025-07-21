// static/app.js

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("searchForm");
  const loader = document.getElementById("loader");

  form.addEventListener("submit", () => {
    loader.classList.remove("hidden");
  });
});
