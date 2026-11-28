const chat = document.getElementById('chat');
const EMOTES = {
    'exalted': 'emotes/exalted.svg',
    'chaos': 'emotes/chaos.svg',
    'divine': 'emotes/divine.svg',
    'regal': 'emotes/regal.svg',
    'mirror': 'emotes/mirror.svg'
};

function parseEmotes(text) {
    return text.replace(/\[(\w+)\]/g, (match, emote) => {
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
    }, 12000);
}

// Тестовые сообщения
setTimeout(() => addMessage({username: 'ExileMaster', message: 'Добро пожаловать в лигу! [exalted]'}), 500);
setTimeout(() => addMessage({username: 'ChaosRunner', message: 'Нашёл [chaos] и [divine]!'}), 2000);
setTimeout(() => addMessage({username: 'MirrorHunter', message: 'Кто-trade [mirror]? [regal]'}), 4000);
setTimeout(() => addMessage({system: true, message: '⚔️ Новая лига началась!'}), 6000);