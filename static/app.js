// static/app.js

document.addEventListener("DOMContentLoaded", () => {
  // Remember theme choice
document.addEventListener("DOMContentLoaded", () => {
  if (localStorage.getItem("theme") === "dark") {
    document.body.classList.add("dark-mode");
    document.getElementById("themeSwitch").checked = true;
  }

  document.getElementById("themeSwitch").addEventListener("change", function () {
    if (this.checked) {
      document.body.classList.add("dark-mode");
      localStorage.setItem("theme", "dark");
    } else {
      document.body.classList.remove("dark-mode");
      localStorage.setItem("theme", "matrix");
    }
  });
});

  // === GitHub Form Logic ===
  const form = document.getElementById("searchForm");
  const loading = document.getElementById("loading");

  form?.addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = form.username.value.trim();
    if (!username) return;

    loading.style.display = "block";

    try {
      const response = await fetch("/", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `username=${encodeURIComponent(username)}`,
      });

      const html = await response.text();
      document.open();
      document.write(html);
      document.close();
    } catch (err) {
      console.error("Fetch error:", err);
    } finally {
      loading.style.display = "none";
    }
  });

  // === Matrix Rain Effect ===
  const canvas = document.getElementById("matrix");
  const ctx = canvas.getContext("2d");

  // === Theme Toggle Script ===
document.getElementById("themeSwitch").addEventListener("change", function () {
  if (this.checked) {
    document.body.classList.add("dark-mode");
    this.nextSibling.textContent = " Switch to Matrix Mode";
  } else {
    document.body.classList.remove("dark-mode");
    this.nextSibling.textContent = " Switch to Dark Mode";
  }
});


  // Set canvas full screen
  const resizeCanvas = () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  };

  resizeCanvas();

  const letters = "アァイィウヴエェオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂッヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモヤユヨラリルレロワヲンABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
  const fontSize = 14;
  let columns = Math.floor(canvas.width / fontSize);
  const drops = new Array(columns).fill(1);

  const drawMatrixRain = () => {
    ctx.fillStyle = "rgba(0, 0, 0, 0.05)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = "#0F0";
    ctx.font = fontSize + "px monospace";

    for (let i = 0; i < drops.length; i++) {
      const char = letters[Math.floor(Math.random() * letters.length)];
      ctx.fillText(char, i * fontSize, drops[i] * fontSize);

      if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
        drops[i] = 0;
      }

      drops[i]++;
    }
  };

  setInterval(drawMatrixRain, 33);

  // Handle screen resize
  window.addEventListener("resize", () => {
    resizeCanvas();
    columns = Math.floor(canvas.width / fontSize);
    drops.length = columns;
    drops.fill(1);
  });
});
