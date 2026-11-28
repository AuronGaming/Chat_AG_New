"""Иконки и графика для UI"""

from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor, QPen, QFont, QPolygonF
from PyQt6.QtCore import Qt, QPointF


def create_update_icon(size=16) -> QIcon:
    """Зелёная стрелка вверх"""
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setPen(QPen(QColor("#2ea043"), max(1, size // 8), Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
    painter.setBrush(QColor("#2ea043"))
    painter.drawLine(int(size * 0.5), int(size * 0.8), int(size * 0.5), int(size * 0.35))
    arrow = QPolygonF([
        QPointF(size * 0.5, size * 0.15),
        QPointF(size * 0.25, size * 0.45),
        QPointF(size * 0.75, size * 0.45)
    ])
    painter.drawPolygon(arrow)
    painter.end()
    return QIcon(pixmap)


def create_check_icon(size=18) -> QIcon:
    """Иконка галочки ✓"""
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setBrush(QColor("#2ea043"))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawRoundedRect(0, 0, size, size, 3, 3)
    painter.setPen(QColor("white"))
    painter.setBrush(Qt.BrushStyle.NoBrush)
    pen = painter.pen()
    pen.setWidth(2)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    painter.setPen(pen)
    painter.drawLine(int(size * 0.25), int(size * 0.55), int(size * 0.45), int(size * 0.75))
    painter.drawLine(int(size * 0.45), int(size * 0.75), int(size * 0.75), int(size * 0.30))
    painter.end()
    return QIcon(pixmap)


def create_platform_icon(name: str, color: str, size: int = 20) -> QIcon:
    """Маленькая иконка платформы (для панели платформ)"""
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setBrush(QColor(color))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawRoundedRect(0, 0, size, size, 4, 4)
    painter.setPen(QColor("white"))
    painter.setFont(QFont("Segoe UI", size // 2, QFont.Weight.Bold))
    painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, name[0].upper())
    painter.end()
    return QIcon(pixmap)


def create_platform_icon_large(name: str, color: str, size: int = 32) -> QIcon:
    """Большая иконка платформы (для лога чата)"""
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setBrush(QColor(color))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawRoundedRect(0, 0, size, size, 6, 6)
    painter.setPen(QColor("white"))
    painter.setFont(QFont("Segoe UI", size // 3, QFont.Weight.Bold))
    painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, name[0].upper())
    painter.end()
    return QIcon(pixmap)