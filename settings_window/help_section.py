"""Страница 'Как подключить' — справка по подключению платформ"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit
from PyQt6.QtCore import Qt

# Константы для справки (на уровне модуля)
THEME_HELP = """
<h3 style="color: #00BFFF;">Темы оформления</h3>
<p>1. Откройте <b>Настройки → Тема оформления → Каталог тем</b></p>
<p>2. Выберите тему из списка</p>
<p>3. Нажмите <b>✅ Выбрать эту тему</b></p>
<p>4. Для настройки параметров нажмите <b>⚙️ Настройка</b></p>
"""

CONNECTIONS_HELP = """
<h3 style="color: #00BFFF;">Соединения</h3>
<p><b>Twitch:</b> Введите ник канала и OAuth-токен → Подключить</p>
<p><b>YouTube:</b> Вставьте ссылку на трансляцию → Подключить</p>
<p><b>VK Play:</b> Введите ID канала → Подключить</p>
<p><b>Goodgame, Kick, Rutube, TikTok, Telegram:</b> Аналогично через OAuth-токены</p>
"""


class HelpSection(QWidget):
    def __init__(self, title: str = "Как подключить", icon: str = "📖", help_text: str = "", parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: transparent;")
        lay = QVBoxLayout(self)
        lay.setContentsMargins(20, 20, 20, 20)
        
        title_label = QLabel(f"{icon} {title}")
        title_label.setStyleSheet("color: #00BFFF; font-size: 18px; font-weight: bold;")
        lay.addWidget(title_label)
        
        text = QTextEdit()
        text.setReadOnly(True)
        text.setStyleSheet("""
            QTextEdit {
                background-color: #0D1117;
                color: #C9D1D9;
                border: 1px solid #30363D;
                border-radius: 6px;
                padding: 10px;
                font-size: 13px;
            }
        """)
        text.setHtml(help_text)
        lay.addWidget(text, stretch=1)
