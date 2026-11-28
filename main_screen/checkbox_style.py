"""Стиль чекбоксов с галочкой (PNG создаётся после старта QApplication)"""

import os
from PyQt6.QtGui import QPixmap, QPainter, QColor, QPen
from PyQt6.QtCore import Qt

_CHECK_PNG = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets', 'check.png'))
_created = False


def _ensure_check_png():
    """Создать PNG галочки. Вызывается лениво, когда QApplication уже есть."""
    global _created
    if _created:
        return
    if os.path.exists(_CHECK_PNG):
        _created = True
        return

    # QPixmap требует активный QApplication
    from PyQt6.QtWidgets import QApplication
    if QApplication.instance() is None:
        return  # слишком рано, попробуем позже

    os.makedirs(os.path.dirname(_CHECK_PNG), exist_ok=True)

    pm = QPixmap(18, 18)
    pm.fill(Qt.GlobalColor.transparent)
    p = QPainter(pm)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)
    p.setBrush(QColor("#2ea043"))
    p.setPen(Qt.PenStyle.NoPen)
    p.drawRoundedRect(0, 0, 18, 18, 3, 3)
    pen = QPen(QColor("white"))
    pen.setWidth(2)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
    p.setPen(pen)
    p.setBrush(Qt.BrushStyle.NoBrush)
    p.drawLine(4, 9, 8, 13)
    p.drawLine(8, 13, 14, 5)
    p.end()

    if pm.save(_CHECK_PNG, "PNG"):
        _created = True
        print(f"✅ Галочка создана: {_CHECK_PNG}")
    else:
        print(f"❌ Не удалось сохранить PNG: {_CHECK_PNG}")


def checkbox_style(text_color="#c9d1d9", border_color="#30363d",
                   bg_color="#161b22", accent_color="#2ea043") -> str:
    _ensure_check_png()
    url = _CHECK_PNG.replace(os.sep, '/')
    return f"""
        QCheckBox {{ color: {text_color}; font-size: 13px; spacing: 8px; }}
        QCheckBox::indicator {{
            width: 18px; height: 18px;
            border: 2px solid {border_color};
            border-radius: 3px;
            background-color: {bg_color};
        }}
        QCheckBox::indicator:hover {{ border-color: {accent_color}; }}
        QCheckBox::indicator:checked {{
            background-color: {accent_color};
            border-color: {accent_color};
            image: url({url});
        }}
    """