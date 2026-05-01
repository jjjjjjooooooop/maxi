const API_URL = "";

async function request(path, options = {}) {
  const token = localStorage.getItem("chatToken");
  const headers = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
  };
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(`${API_URL}${path}`, { ...options, headers });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(data.detail || "Ошибка запроса");
  }
  return data;
}

export async function register(username, password) {
  return request("/auth/register", {
    method: "POST",
    body: JSON.stringify({ username, password }),
  });
}

export async function login(username, password) {
  return request("/auth/login", {
    method: "POST",
    body: JSON.stringify({ username, password }),
  });
}

export async function createSession() {
  return request("/chat/session", { method: "POST" });
}

export async function sendMessage(sessionId, text) {
  return request("/chat/message", {
    method: "POST",
    body: JSON.stringify({ session_id: sessionId, text }),
  });
}

export async function getHistory(sessionId) {
  return request(`/chat/history/${sessionId}`);
}
