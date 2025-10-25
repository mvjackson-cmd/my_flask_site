document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("helloBtn");
  const nameInput = document.getElementById("nameInput");
  const result = document.getElementById("helloResult");
  if (!btn) return;

  btn.addEventListener("click", async () => {
    const name = (nameInput?.value || "friend").trim();
    const res = await fetch(`/api/hello?name=${encodeURIComponent(name)}`);
    const data = await res.json();

    result.classList.remove("d-none", "alert-secondary", "alert-danger");
    result.classList.add("alert-primary");
    result.textContent = data.message || "No message.";
  });
});

