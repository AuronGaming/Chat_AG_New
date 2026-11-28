const chat = document.getElementById('chat');

function addMessage(m) {
  const el = document.createElement('div');
  el.className = 'message';
  const badge = document.createElement('span');
  badge.className = 'badge';
  badge.textContent = m.platform || '';
  const user = document.createElement('span');
  user.className = 'user';
  user.style.color = m.color || '#ffffff';
  user.textContent = (m.user || '') + ': ';
  const text = document.createElement('span');
  text.className = 'text';
  text.textContent = m.text || '';
  el.append(badge, user, text);
  chat.appendChild(el);
  while (chat.children.length > 30) chat.removeChild(chat.firstChild);
}

function connect() {
  const ws = new WebSocket(`ws://${location.hostname}:${location.port || 8383}/ws`);
  ws.onmessage = (e) => { try { addMessage(JSON.parse(e.data)); } catch (_) {} };
  ws.onclose = () => setTimeout(connect, 2000);
}
connect();

// Демо-сообщения для предпросмотра в OBS
[['twitch','#9146FF'],['youtube','#FF0000'],['vk_play','#0077FF']].forEach(([p,c],i) => {
  setTimeout(() => addMessage({platform:p, user:'demo_user', color:c, text:'Тестовое сообщение '+(i+1)}), 400*i);
});