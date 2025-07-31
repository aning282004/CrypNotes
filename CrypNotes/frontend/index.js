document.addEventListener("DOMContentLoaded", async () => {
  const res = await fetch("http://localhost:8000/notes");
  const notes = await res.json();
  const container = document.getElementById("notes");

  notes.forEach(note => {
    const card = document.createElement("div");
    card.className = "bg-white shadow-md p-4 rounded";

    const encryptedBadge = note.is_encrypted
      ? "<span class='text-sm text-red-500'>(encrypted)</span>"
      : "";

    card.innerHTML = `
      <h2 class="text-xl font-semibold">${note.title} ${encryptedBadge}</h2>
      <p class="text-gray-700">by ${note.author}</p>
      <p class="mt-2">${note.is_encrypted ? "<i>Encrypted content hidden</i>" : note.content}</p>
    `;
    container.appendChild(card);
  });
});
