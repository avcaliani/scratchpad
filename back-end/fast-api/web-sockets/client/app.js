const base = "ws://127.0.0.1:8000/ws";

const element = (tag, text, cls = "") => {
  const node = document.createElement(tag);
  node.textContent = text;
  node.className = cls;
  return node;
};

const append = (id, li) => {
  const log = document.getElementById(id);
  log.append(li);
  if (log.children.length > 100) log.firstElementChild.remove();
  log.scrollTop = log.scrollHeight;
};

const feedContent = (sender, time, kind, detail) => {
  const content = element("div", "");
  const header = element("div", "", "event-header");
  header.append(element("strong", sender), element("span", time, "event-time"));
  content.append(header, element("p", kind, "event-kind"), element("p", detail, "event-detail"));
  return content;
};

const addIntercomMessage = (sender, time, detail, sent = false) => {
  const row = element("li", "", "feed-entry");
  const icon = element("span", sent ? "send" : "campaign", `material-symbols-outlined message-icon${sent ? "" : " reply"}`);
  icon.setAttribute("aria-hidden", "true");
  row.append(feedContent(sender, time, sent ? "Sent" : "Reply", detail), icon);
  append("intercom-log", row);
};

const addTickerEvent = (event) => {
  const row = element("li", "", "feed-entry");
  const content = feedContent(event.employee, `${event.at} UTC`, event.type === "check-in" ? "Check-in" : "Redeemed", event.detail);
  const amount = `${event.schrute_bucks > 0 ? "+" : ""}${event.schrute_bucks} SB`;
  row.append(content, element("span", amount, `event-amount${event.schrute_bucks < 0 ? " spent" : ""}`));
  append("ticker-log", row);
};

function connect(path, onMessage, onConnection = () => {}) {
  const ws = new WebSocket(`${base}/${path}`);
  const setStatus = (connected) => {
    document.getElementById(`lamp-${path}`).classList.toggle("on", connected);
    document.getElementById(`status-${path}`).textContent = connected ? "Live" : "Reconnecting";
    onConnection(ws, connected);
  };
  ws.onopen = () => setStatus(true);
  ws.onmessage = (event) => onMessage(event.data);
  ws.onclose = () => {
    setStatus(false);
    setTimeout(() => connect(path, onMessage, onConnection), 2000);
  };
}

let intercom;
connect("intercom", (data) => {
  const reply = JSON.parse(data);
  addIntercomMessage(reply.employee, `${reply.at} UTC`, reply.catchphrase);
}, (ws, connected) => {
  intercom = ws;
  document.getElementById("send").disabled = !connected;
});

let total = 0, events = 0;
connect("ticker", (data) => {
  const e = JSON.parse(data);
  total += e.schrute_bucks;
  events += 1;
  document.getElementById("total").textContent = total;
  addTickerEvent(e);
  if (events % 7 === 0) {
    const drill = document.getElementById("drill");
    drill.classList.add("show");
    setTimeout(() => drill.classList.remove("show"), 3000);
  }
});

document.getElementById("intercom-form").onsubmit = (event) => {
  event.preventDefault();
  const input = document.getElementById("line");
  const text = input.value.trim();
  if (!text || !intercom || intercom.readyState !== WebSocket.OPEN) return;
  addIntercomMessage("You", `${new Date().toISOString().slice(11, 19)} UTC`, text, true);
  intercom.send(text);
  input.value = "";
  input.focus();
};
