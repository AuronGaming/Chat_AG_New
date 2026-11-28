"""Анимированные карточки тем — подключается опционально"""
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QPixmap, QPainter, QColor, QFont


def apply_animation(card):
    """Добавляет вращение к карточке AG и POE"""
    card._angle = 0
    badge = str(card.badge).upper()

    if badge not in ("AG", "POE"):
        return  # остальные темы без анимации

    card._timer = QTimer(card)
    card._timer.timeout.connect(lambda: _rotate(card))
    card._timer.start(80)  # медленнее = меньше нагрузка


def _rotate(card):
    card._angle = (card._angle + 4) % 360
    pm = QPixmap(162, 112)
    badge = str(card.badge).upper()

    if badge == "AG":
        pm.fill(QColor("#000000"))
        p = QPainter(pm)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.translate(81, 56)
        p.rotate(card._angle)
        p.setPen(QColor("#00FF00"))
        p.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        p.drawText(-35, 12, "AG")
        p.end()
    elif badge == "POE":
        pm.fill(QColor("#000000"))
        p = QPainter(pm)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.translate(81, 56)
        p.rotate(card._angle)
        p.setBrush(QColor("#C4A000"))
        p.setPen(QColor("#8B6914"))
        p.drawEllipse(-22, -22, 44, 44)
        p.setPen(QColor("#FFE44D"))
        p.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        p.drawText(-10, 5, "POE")
        p.end()

    card.preview.setPixmap(pm)