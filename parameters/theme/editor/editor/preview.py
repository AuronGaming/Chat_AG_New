"""Превью темы — рисует имитацию сообщений"""
from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPixmap, QPainter, QColor, QFont
from PyQt6.QtCore import Qt
from main_screen.theme_config import COLORS


class ThemePreview(QLabel):
    """Виджет превью темы (265x500)"""

    def __init__(self, theme_name: str, settings: dict, parent=None):
        super().__init__(parent)
        self.theme_name = theme_name
        self.settings = settings
        self.setFixedSize(265, 500)
        self.setMinimumHeight(500)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet(f"""
            QLabel {{
                background-color: {COLORS['bg_input']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
            }}
        """)
        self._draw()

    def update_settings(self, settings: dict):
        self.settings = settings
        self._draw()

    def _draw(self):
        s = self.settings
        bg_color = QColor("#1a1208")  # цвет фона темы (из theme.json)
        pm = QPixmap(265, 500)
        pm.fill(bg_color)
        p = QPainter(pm)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Рисуем 3 сообщения
        messages = [
            ("Player123", "Привет всем!"),
            ("Gamer456", "Как дела?"),
            ("Streamer", "Го рейд!"),
        ]
        y = 20
        nick_font = QFont(s.get("nickname_font", "Cuprum"), s.get("nickname_font_size", 15))
        text_font = QFont(s.get("text_font", "Cuprum"), s.get("text_font_size", 15))
        nick_color = QColor(s.get("nickname_color", "#FF9900"))
        text_color = QColor(s.get("text_color", "#C1B078"))

        for nick, text in messages:
            # Фон сообщения
            p.fillRect(8, y, 249, 60, QColor(20, 14, 8, 220))
            p.setPen(QColor(107, 84, 38))
            p.drawRect(8, y, 249, 60)
            # Полоска слева
            p.fillRect(8, y, 4, 60, nick_color)
            # Ник
            p.setPen(nick_color)
            p.setFont(nick_font)
            p.drawText(20, y + 22, nick + ":")
            # Текст
            p.setPen(text_color)
            p.setFont(text_font)
            p.drawText(20, y + 45, text)
            y += 75

        p.end()
        self.setPixmap(pm)