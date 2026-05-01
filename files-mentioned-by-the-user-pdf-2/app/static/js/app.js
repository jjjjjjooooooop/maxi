import { createSession, getHistory, login, register, sendMessage } from "./api.js";

const authForm = document.querySelector("#authForm");
const registerBtn = document.querySelector("#registerBtn");
const usernameInput = document.querySelector("#username");
const passwordInput = document.querySelector("#password");
const authStatus = document.querySelector("#authStatus");
const chatWindow = document.querySelector("#chatWindow");
const messageForm = document.querySelector("#messageForm");
const messageInput = document.querySelector("#messageInput");
const sendBtn = document.querySelector("#sendBtn");
const clearBtn = document.querySelector("#clearBtn");
const typingIndicator = document.querySelector("#typingIndicator");

let sessionId = Number(localStorage.getItem("chatSessionId")) || null;

function setStatus(text, isError = false) {
  authStatus.textContent = text;
  authStatus.classList.toggle("error", isError);
}

function addMessage(sender, text) {
  const element = document.createElement("div");
  element.className = `message ${sender}`;
  element.textContent = text;
  chatWindow.append(element);
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

function setSending(isSending) {
  sendBtn.disabled = isSending;
  messageInput.disabled = isSending;
  typingIndicator.classList.toggle("hidden", !isSending);
}

async function ensureSession() {
  if (sessionId) {
    return sessionId;
  }
  const session = await createSession();
  sessionId = session.id;
  localStorage.setItem("chatSessionId", String(sessionId));
  return sessionId;
}

async function restoreHistory() {
  if (!sessionId || !localStorage.getItem("chatToken")) {
    return;
  }
  try {
    const history = await getHistory(sessionId);
    chatWindow.replaceChildren();
    history.messages.forEach((message) => addMessage(message.sender, message.text));
  } catch {
    localStorage.removeItem("chatSessionId");
    sessionId = null;
  }
}

async function handleAuth(mode) {
  const username = usernameInput.value.trim();
  const password = passwordInput.value;
  if (!username || !password) {
    setStatus("Заполните логин и пароль.", true);
    return;
  }

  try {
    if (mode === "register") {
      await register(username, password);
      setStatus("Регистрация успешна. Теперь можно войти.");
      return;
    }
    const token = await login(username, password);
    localStorage.setItem("chatToken", token.access_token);
    localStorage.removeItem("chatSessionId");
    sessionId = null;
    await ensureSession();
    chatWindow.replaceChildren();
    addMessage("bot", "Здравствуйте! Я помогу с HTML, CSS, JavaScript, API и базой данных.");
    setStatus("Вы вошли в систему.");
  } catch (error) {
    setStatus(error.message, true);
  }
}

authForm.addEventListener("submit", (event) => {
  event.preventDefault();
  handleAuth("login");
});

registerBtn.addEventListener("click", () => handleAuth("register"));

messageForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const text = messageInput.value.trim();
  if (!text) {
    return;
  }

  try {
    await ensureSession();
    addMessage("user", text);
    messageInput.value = "";
    setSending(true);
    const response = await sendMessage(sessionId, text);
    setTimeout(() => {
      addMessage("bot", response.bot_message.text);
      setSending(false);
      messageInput.focus();
    }, 700);
  } catch (error) {
    setSending(false);
    setStatus(error.message, true);
  }
});

clearBtn.addEventListener("click", () => {
  chatWindow.replaceChildren();
});

restoreHistory();
