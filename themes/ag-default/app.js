const chat = document.getElementById('chat');
const EMOTES = {
    'like': 'emotes/like.svg',
    'fire': 'emotes/fire.svg',
    'heart': 'emotes/heart.svg',
    'star': 'emotes/star.svg',
    'cool': 'emotes/cool.svg'
};

function parseEmotes(text) {
    return text.replace(/\\[(\\w+)\\]/g, (match, emote) => {
        if (EMOTES[emote]) {
            return `<img src="${EMOTES[emote]}" class="emote" alt="${emote}" title="${emote}">`;
        }
        return match;
    });
}

function addMessage(data) {
    const msg = document.createElement('div');
    msg.className = data.system ? 'system-message' : 'message';

    const time = document.createElement('span');
    time.className = 'timestamp';
    time.textContent = new Date().toLocaleTimeString('ru-RU', {hour:'2-digit', minute:'2-digit'});
    msg.appendChild(time);

    if (!data.system) {
        const nick = document.createElement('span');
        nick.className = 'nickname';
        nick.textContent = data.username + ': ';
        msg.appendChild(nick);
    }

    const text = document.createElement('span');
    text.className = 'text';
    text.innerHTML = parseEmotes(data.message);
    msg.appendChild(text);

    chat.appendChild(msg);
    chat.scrollTop = chat.scrollHeight;

    setTimeout(() => {
        msg.style.animation = 'fadeOut 0.3s';
        setTimeout(() => msg.remove(), 300);
    }, 10000);
}

// Тестовые сообщения
setTimeout(() => addMessage({username: 'AuronGaming', message: 'Добро пожаловать в Chat AG! [like]'}), 500);
setTimeout(() => addMessage({username: 'Viewer1', message: 'Крутой стрим! [fire][fire]'}), 2000);
setTimeout(() => addMessage({username: 'Viewer2', message: 'Люблю этот чат [heart]'}), 4000);
setTimeout(() => addMessage({system: true, message: '🎮 Стрим начался!'}), 6000);