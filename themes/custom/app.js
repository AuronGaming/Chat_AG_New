const chat = document.getElementById('chat');
const EMOTES = {'like': 'emotes/like.svg', 'fire': 'emotes/fire.svg', 'heart': 'emotes/heart.svg', 'star': 'emotes/star.svg', 'cool': 'emotes/cool.svg'};
function parseEmotes(text) { return text.replace(/\\[(\\w+)\\]/g, (m, e) => EMOTES[e] ? `<img src="${EMOTES[e]}" class="emote">` : m); }
function addMessage(data) {
    const msg = document.createElement('div');
    msg.className = data.system ? 'message' : 'message';
    msg.style.borderLeftColor = '#00FF00';
    const time = document.createElement('span'); time.className = 'timestamp';
    time.textContent = new Date().toLocaleTimeString('ru-RU', {hour:'2-digit', minute:'2-digit'});
    msg.appendChild(time);
    if (!data.system) { const nick = document.createElement('span'); nick.className = 'nickname'; nick.textContent = data.username + ': '; msg.appendChild(nick); }
    const text = document.createElement('span'); text.className = 'text'; text.innerHTML = parseEmotes(data.message); msg.appendChild(text);
    chat.appendChild(msg);
    setTimeout(() => { msg.style.animation = 'fadeOut 0.3s'; setTimeout(() => msg.remove(), 300); }, 10000);
}
setTimeout(() => addMessage({username: 'User', message: 'Моя тема! [like]'}), 500);