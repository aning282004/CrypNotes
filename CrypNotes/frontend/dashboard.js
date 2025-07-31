document.addEventListener("DOMContentLoaded", () => {
  const token = localStorage.getItem("token");
  const username = localStorage.getItem("username");

  if (token && username) {
    document.getElementById("loginForm").classList.add("hidden");
    document.getElementById("noteForm").classList.remove("hidden");
    document.getElementById("logoutArea").classList.remove("hidden");
    document.getElementById("userLabel").innerText = `Logged in as ${username}`;
    loadNotes();
  }
});

async function login() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  const res = await fetch("/auth/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password })
  });

  if (!res.ok) {
    alert("Login failed");
    return;
  }

  const data = await res.json();
  localStorage.setItem("token", data.access_token);
  localStorage.setItem("username", username);

  document.getElementById("loginForm").classList.add("hidden");
  document.getElementById("noteForm").classList.remove("hidden");
  document.getElementById("logoutArea").classList.remove("hidden");
  document.getElementById("userLabel").innerText = `Logged in as ${username}`;
  loadNotes();
}

function logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("username");

  document.getElementById("loginForm").classList.remove("hidden");
  document.getElementById("noteForm").classList.add("hidden");
  document.getElementById("logoutArea").classList.add("hidden");
  document.getElementById("userLabel").innerText = "";
  document.getElementById("myNotes").innerHTML = "";
}

async function createNote() {
  const title = document.getElementById("title").value;
  const content = document.getElementById("content").value;
  const encrypt = document.getElementById("encrypt").checked;
  const token = localStorage.getItem("token");

  const res = await fetch("/notes", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({ title, content, encrypt })
  });

  if (res.ok) {
    alert("Note saved");
    loadNotes();
  } else {
    alert("Failed to save note");
  }
}

async function loadNotes() {
  const token = localStorage.getItem("token");
  const res = await fetch("/notes", {
    headers: {
      Authorization: `Bearer ${token}`
    }
  });

  const notes = await res.json();
  const container = document.getElementById("myNotes");
  container.innerHTML = "";

  notes.forEach(note => {
    const div = document.createElement("div");
    div.className = "p-3 bg-white shadow rounded";
    div.innerHTML = `<strong>${note.title}</strong><p>${note.content}</p>`;
    container.appendChild(div);
  });
}
