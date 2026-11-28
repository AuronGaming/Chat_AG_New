"""Генерация PNG иконок платформ и декоративных силуэтов"""

import os
import random
from PyQt6.QtGui import QPixmap, QPainter, QColor, QFont, QImage
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel

ICONS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets', 'platforms'))
os.makedirs(ICONS_DIR, exist_ok=True)

PLATFORM_COLORS = {
    "twitch": "#9146FF",
    "youtube": "#FF0000",
    "vk_play": "#0077FF",
    "goodgame": "#FF6600",
    "kick": "#53FC19",
    "rutube": "#00BFFF",
    "tiktok": "#000000",
    "telegram": "#0088CC",
    "donation_alerts": "#FF5500",
    "система": "#888888",
}

DECO_SYMBOLS = ["🎸", "🎮", "📷", "🎤", "🎧", "🎲", "🎯", "🎺", "🎬", "🕹️"]


def get_platform_icon_path(platform: str, size: int = 16) -> str:
    """Вернуть путь к PNG иконке платформы"""
    filename = f"{platform.lower()}_{size}px.png"
    path = os.path.join(ICONS_DIR, filename)
    if os.path.exists(path):
        return path

    color = PLATFORM_COLORS.get(platform.lower(), "#888888")
    letter = platform[0].upper() if platform else "?"

    pm = QPixmap(size, size)
    pm.fill(Qt.GlobalColor.transparent)
    p = QPainter(pm)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.setBrush(QColor(color))
    p.setPen(Qt.PenStyle.NoPen)
    p.drawRoundedRect(0, 0, size, size, 2, 2)
    p.setPen(QColor("white"))
    p.setFont(QFont("Segoe UI", max(8, size // 2), QFont.Weight.Bold))
    p.drawText(pm.rect(), Qt.AlignmentFlag.AlignCenter, letter)
    p.end()
    pm.save(path, "PNG")
    return path


def get_platform_icon_url(platform: str, size: int = 16) -> str:
    """Вернуть URL для вставки в HTML"""
    path = get_platform_icon_path(platform, size)
    return f"file:///{path.replace(os.sep, '/')}"


def get_deco_icon_path(symbol: str, size: int = 28) -> str:
    """Создать СЕРЫЙ силуэт через конвертацию эмодзи в grayscale"""
    filename = f"deco_gray_{hash(symbol) % 100000}_{size}px.png"
    path = os.path.join(ICONS_DIR, filename)
    if os.path.exists(path):
        return path

    # Сначала рисуем цветной эмодзи
    pm = QPixmap(size, size)
    pm.fill(Qt.GlobalColor.transparent)
    p = QPainter(pm)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.setFont(QFont("Segoe UI Emoji", size - 4))
    p.drawText(pm.rect(), Qt.AlignmentFlag.AlignCenter, symbol)
    p.end()

    # Конвертируем в grayscale через QImage
    img = pm.toImage()
    img = img.convertToFormat(QImage.Format.Format_Grayscale8)

    # Добавляем прозрачность
    alpha_img = img.convertToFormat(QImage.Format.Format_ARGB32)
    p2 = QPainter(alpha_img)
    p2.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
    p2.fillRect(alpha_img.rect(), QColor(120, 120, 120, 80))
    p2.end()

    alpha_img.save(path, "PNG")
    return path


def get_deco_block_html(count: int = 12, size: int = 28) -> str:
    """Вернуть HTML с блоком декоративных иконок"""
    icons = random.sample(DECO_SYMBOLS, min(count, len(DECO_SYMBOLS)))
    random.shuffle(icons)

    parts = []
    for symbol in icons:
        path = get_deco_icon_path(symbol, size)
        url = f"file:///{path.replace(os.sep, '/')}"
        parts.append(f'<img src="{url}" width="{size}" height="{size}" style="margin: 2px;">')

    return ' '.join(parts)


def get_deco_icons_widget(count: int = 12, size: int = 28) -> QWidget:
    """Вернуть QWidget с сеткой декоративных иконок"""
    widget = QWidget()
    widget.setFixedSize(200, 60)

    grid = QGridLayout(widget)
    grid.setContentsMargins(0, 0, 0, 0)
    grid.setSpacing(2)

    icons = random.sample(DECO_SYMBOLS, min(count, len(DECO_SYMBOLS)))
    random.shuffle(icons)

    cols = 6
    for i, symbol in enumerate(icons):
        path = get_deco_icon_path(symbol, size)
        label = QLabel()
        label.setPixmap(QPixmap(path))
        label.setFixedSize(size, size)
        grid.addWidget(label, i // cols, i % cols)

    return widget