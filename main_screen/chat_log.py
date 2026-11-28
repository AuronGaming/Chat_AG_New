"""Лог чата v1.0.3 — сообщения слева + фоновые декоративные иконки по всей области"""

import os
import random

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextBrowser, QLabel
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QTextCursor, QPixmap, QPainter, QColor, QFont
from main_screen.theme_config import COLORS

# ---------------------------------------------------------------------------
# Иконки платформ (PNG генерируются один раз)
# ---------------------------------------------------------------------------
_ICONS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets', 'platforms'))
os.makedirs(_ICONS_DIR, exist_ok=True)

PLATFORM_COLORS = {
    "twitch": "#9146FF",
    "youtube": "#FF0000",
    "vk_play": "#0077FF",
    "goodgame": "#FF6600",
    "kick": "#53FC19",
    "rutube": "#00BFFF",
    "tiktok": "#111111",
    "telegram": "#0088CC",
    "donation_alerts": "#FF5500",
    "система": "#000000",
    "vk": "#0077FF",
    "trovo": "#7b2cbf",
}

PLATFORM_SYMBOLS = {
    "twitch": "T",
    "youtube": "▶",
    "vk_play": "VK",
    "goodgame": "GG",
    "kick": "K",
    "rutube": "R",
    "tiktok": "T",
    "telegram": "TG",
    "donation_alerts": "?",
    "система": "⚙",
    "vk": "VK",
    "trovo": "T",
}


def _platform_icon_path(platform: str, size: int = 16) -> str:
    key = platform.lower()
    path = os.path.join(_ICONS_DIR, f"{key}_{size}px.png")
    if os.path.exists(path):
        return path
    color = PLATFORM_COLORS.get(key, "#888888")
    symbol = PLATFORM_SYMBOLS.get(key, "?")
    pm = QPixmap(size, size)
    pm.fill(Qt.GlobalColor.transparent)
    p = QPainter(pm)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.setBrush(QColor(color))
    p.setPen(Qt.PenStyle.NoPen)
    p.drawRoundedRect(0, 0, size, size, 3, 3)
    p.setPen(QColor("white"))
    fs = 10 if len(symbol) == 1 else 7
    p.setFont(QFont("Segoe UI", fs, QFont.Weight.Bold))
    p.drawText(pm.rect(), Qt.AlignmentFlag.AlignCenter, symbol)
    p.end()
    pm.save(path, "PNG")
    return path


def _platform_icon_url(platform: str, size: int = 16) -> str:
    return f"file:///{_platform_icon_path(platform, size).replace(os.sep, '/')}"


# ---------------------------------------------------------------------------
# Фоновый слой с декоративными иконками (как на образце)
# ---------------------------------------------------------------------------
DECO_SYMBOLS = ["🎮", "📷", "🎸", "🎬", "🎺", "🎤", "🎯", "🕹️", "🎧", "🎲", "🏰", "🔒"]


class _DecoLayer(QWidget):
    """Полупрозрачная сетка цветных иконок по всей области чата"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self._symbols = []
        rnd = random.Random(42)  # фиксированный seed — не мигает при перерисовке
        for _ in range(200):
            self._symbols.append(rnd.choice(DECO_SYMBOLS))

    def paintEvent(self, event):
        p = QPainter(self)
        p.setOpacity(0.35)
        p.setFont(QFont("Segoe UI Emoji", 13))
        row = 0
        y = 15
        while y < self.height():
            x = 40 + (row % 2) * 45
            col = 0
            while x < self.width() - 30:
                sym = self._symbols[(row * 9 + col) % len(self._symbols)]
                p.drawText(QRect(x, y, 30, 30), Qt.AlignmentFlag.AlignCenter, sym)
                x += 95
                col += 1
            y += 95
            row += 1
        p.end()


# ---------------------------------------------------------------------------
# Основной виджет лога
# ---------------------------------------------------------------------------
class ChatLogWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"background-color: {COLORS['bg_main']};")

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        self.container = QWidget(self)
        self.container.setStyleSheet(f"background-color: {COLORS['bg_main']};")
        outer.addWidget(self.container)

        # Фоновый слой с иконками
        self.deco = _DecoLayer(self.container)
        self.deco.setGeometry(self.container.rect())
        self.deco.lower()

        # Прозрачный QTextBrowser поверх
        self.log = QTextBrowser(self.container)
        self.log.setStyleSheet(f"""
            QTextBrowser {{
                background: transparent;
                color: {COLORS['text_primary']};
                border: none;
                font-size: 13px;
                padding: 10px;
            }}
        """)
        self.log.viewport().setAutoFillBackground(False)
        self.log.setOpenExternalLinks(False)
        self.log.setReadOnly(True)

        inner = QVBoxLayout(self.container)
        inner.setContentsMargins(0, 0, 0, 0)
        inner.addWidget(self.log)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.deco.setGeometry(self.container.rect())

    # ------------------------------------------------------------------
    def _line_html(self, time_str, platform, name, name_color, text, text_color):
        icon_url = _platform_icon_url(platform, 16)
        return (
            f'<span style="color: {COLORS["text_secondary"]}; font-size: 11px;">{time_str}</span>'
            f'&nbsp;&nbsp;'
            f'<img src="{icon_url}" width="16" height="16" style="vertical-align: middle;">'
            f'&nbsp;&nbsp;'
            f'<b style="color: {name_color}; font-size: 13px;">{name}:</b> '
            f'<span style="color: {text_color};">{text}</span><br>'
        )

    def add_chat_message(self, platform: str, username: str, message: str,
                         color: str = "#ffffff", emotes: dict = None, gifs: list = None):
        from datetime import datetime
        time_str = datetime.now().strftime("[%H:%M]")
        html = self._line_html(time_str, platform, username, color, message, COLORS['text_primary'])
        self.log.insertHtml(html)
        self.log.moveCursor(QTextCursor.MoveOperation.End)

    def add_system_message(self, platform: str, message: str, level: str = "INFO"):
        from datetime import datetime
        time_str = datetime.now().strftime("[%H:%M]")
        level_colors = {
            "INFO": COLORS['text_primary'],
            "WARNING": "#FFA500",
            "ERROR": "#FF4444",
            "SUCCESS": "#2ea043",
        }
        c = level_colors.get(level, COLORS['text_primary'])
        html = self._line_html(time_str, platform, platform, c, message, c)
        self.log.insertHtml(html)
        self.log.moveCursor(QTextCursor.MoveOperation.End)