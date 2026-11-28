"""Каталог тем — галерея с вращающимися логотипами (глобус-эффект)"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QGridLayout,
    QPushButton, QLineEdit, QComboBox, QFrame
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QPainter, QColor, QFont, QLinearGradient, QRadialGradient, QPolygonF, QPainterPath
from PyQt6.QtCore import QPointF, QRectF
from main_screen.theme_config import COLORS
from core.settings_manager import SettingsManager
import os
import json
import math

THEMES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'themes'))


def _load_own_themes():
    found = []
    if os.path.isdir(THEMES_DIR):
        for folder in sorted(os.listdir(THEMES_DIR)):
            tdir = os.path.join(THEMES_DIR, folder)
            tjson = os.path.join(tdir, 'theme.json')
            if os.path.isdir(tdir) and os.path.isfile(tjson):
                try:
                    with open(tjson, encoding='utf-8') as f:
                        meta = json.load(f)
                    found.append({
                        'id': folder,
                        'color': meta.get('color', '#238636'),
                        'badge': meta.get('badge', 'AG'),
                        'order': meta.get('order', 99),
                    })
                except Exception:
                    pass
    found.sort(key=lambda t: t['order'])
    return found


_OWN = _load_own_themes()
DEFAULT_THEMES = [(t['id'], t['color'], t['badge']) for t in _OWN] if _OWN else [
    ("default", "#0D1117", "AG"),
]

# Темы с вращающимся логотипом-глобусом
GLOBE_THEMES = {"AG", "POE", "МОЯ"}


def draw_globe_poe(p, cx, cy, s, angle):
    """Логотип Path of Exile 1: щит с крыльями, вращение как глобус"""
    # Глобус-эффект: сжатие по X по cos(angle)
    scale = math.cos(math.radians(angle))
    mirror = scale < 0
    w = abs(scale)
    if w < 0.05:
        w = 0.05  # минимальная ширина чтобы не исчезало

    p.save()
    p.translate(cx, cy)
    p.scale(w, 1.0)
    if mirror:
        p.scale(-1.0, 1.0)

    # Задняя тень (сфера)
    p.setPen(Qt.PenStyle.NoPen)
    p.setBrush(QColor(60, 10, 10, 120))
    p.drawEllipse(int(-s*0.9), int(-s*0.9), int(s*1.8), int(s*1.8))

    # Крылья (серые, по бокам щита)
    wing_col = QColor(150, 140, 130)
    p.setBrush(wing_col)
    p.setPen(QColor(60, 55, 50))
    # Левое крыло
    lw = QPolygonF([
        QPointF(-s*0.95, -s*0.1), QPointF(-s*0.7, -s*0.35),
        QPointF(-s*0.45, -s*0.2), QPointF(-s*0.55, s*0.05),
        QPointF(-s*0.85, s*0.2)
    ])
    p.drawPolygon(lw)
    # Правое крыло
    rw = QPolygonF([
        QPointF(s*0.95, -s*0.1), QPointF(s*0.7, -s*0.35),
        QPointF(s*0.45, -s*0.2), QPointF(s*0.55, s*0.05),
        QPointF(s*0.85, s*0.2)
    ])
    p.drawPolygon(rw)

    # Центральный щит (тёмно-красный ромб)
    grad = QLinearGradient(0, -s*0.5, 0, s*0.6)
    grad.setColorAt(0, QColor(120, 20, 25))
    grad.setColorAt(1, QColor(50, 8, 10))
    p.setBrush(grad)
    p.setPen(QColor(20, 5, 5))
    shield = QPolygonF([
        QPointF(0, -s*0.55), QPointF(s*0.45, -s*0.1),
        QPointF(s*0.3, s*0.45), QPointF(0, s*0.65),
        QPointF(-s*0.3, s*0.45), QPointF(-s*0.45, -s*0.1)
    ])
    p.drawPolygon(shield)

    # Верхняя арка с шипами
    p.setBrush(QColor(40, 15, 15))
    p.setPen(QColor(20, 5, 5))
    arc = QPolygonF([
        QPointF(-s*0.5, -s*0.4), QPointF(-s*0.2, -s*0.7),
        QPointF(0, -s*0.55), QPointF(s*0.2, -s*0.7),
        QPointF(s*0.5, -s*0.4), QPointF(0, -s*0.3)
    ])
    p.drawPolygon(arc)

    # Надпись PATH OF EXILE (белая, по центру щита)
    p.setPen(QColor(230, 225, 220))
    p.setFont(QFont("Georgia", max(6, int(s*0.13)), QFont.Weight.Bold))
    p.drawText(QRectF(-s*0.4, -s*0.25, s*0.8, s*0.2), Qt.AlignmentFlag.AlignCenter, "PATH OF")
    p.setFont(QFont("Georgia", max(8, int(s*0.2)), QFont.Weight.Bold))
    p.drawText(QRectF(-s*0.45, -s*0.05, s*0.9, s*0.3), Qt.AlignmentFlag.AlignCenter, "EXILE")

    # Нижние шипы
    p.setBrush(QColor(90, 20, 25))
    p.setPen(QColor(20, 5, 5))
    spike1 = QPolygonF([QPointF(-s*0.25, s*0.45), QPointF(-s*0.15, s*0.75), QPointF(-s*0.05, s*0.5)])
    spike2 = QPolygonF([QPointF(s*0.25, s*0.45), QPointF(s*0.15, s*0.75), QPointF(s*0.05, s*0.5)])
    p.drawPolygon(spike1)
    p.drawPolygon(spike2)

    p.restore()


def draw_globe_ag(p, cx, cy, s, angle):
    """Логотип Chat AG: круг с буквами AG, вращение как глобус"""
    scale = math.cos(math.radians(angle))
    mirror = scale < 0
    w = abs(scale)
    if w < 0.05:
        w = 0.05

    p.save()
    p.translate(cx, cy)
    p.scale(w, 1.0)
    if mirror:
        p.scale(-1.0, 1.0)

    # Внешнее кольцо (зелёное свечение)
    glow = QRadialGradient(0, 0, s)
    glow.setColorAt(0.7, QColor(0, 255, 0, 0))
    glow.setColorAt(0.9, QColor(0, 255, 0, 120))
    glow.setColorAt(1.0, QColor(0, 255, 0, 0))
    p.setBrush(glow)
    p.setPen(Qt.PenStyle.NoPen)
    p.drawEllipse(int(-s*1.1), int(-s*1.1), int(s*2.2), int(s*2.2))

    # Основной круг (тёмный градиент)
    circ = QRadialGradient(0, -s*0.3, s*1.3)
    circ.setColorAt(0, QColor(20, 40, 20))
    circ.setColorAt(1, QColor(5, 12, 5))
    p.setBrush(circ)
    p.setPen(QColor(0, 255, 0))
    p.drawEllipse(int(-s*0.85), int(-s*0.85), int(s*1.7), int(s*1.7))

    # Буквы AG (зелёные)
    p.setPen(QColor(0, 255, 100))
    p.setFont(QFont("Segoe UI", max(10, int(s*0.7)), QFont.Weight.Bold))
    p.drawText(QRectF(-s, -s*0.4, s*2, s*0.8), Qt.AlignmentFlag.AlignCenter, "AG")

    p.restore()


def draw_globe_mya(p, cx, cy, s, angle):
    """Пользовательская тема: чёрный фон, зелёные буквы МОЯ вращаются"""
    scale = math.cos(math.radians(angle))
    mirror = scale < 0
    w = abs(scale)
    if w < 0.05:
        w = 0.05
    p.save()
    p.translate(cx, cy)
    p.scale(w, 1.0)
    if mirror:
        p.scale(-1.0, 1.0)
    # Зелёное свечение
    glow = QRadialGradient(0, 0, s)
    glow.setColorAt(0.7, QColor(0, 255, 0, 0))
    glow.setColorAt(0.9, QColor(0, 255, 0, 120))
    glow.setColorAt(1.0, QColor(0, 255, 0, 0))
    p.setBrush(glow)
    p.setPen(Qt.PenStyle.NoPen)
    p.drawEllipse(int(-s*1.1), int(-s*1.1), int(s*2.2), int(s*2.2))
    # Круг
    circ = QRadialGradient(0, -s*0.3, s*1.3)
    circ.setColorAt(0, QColor(10, 30, 10))
    circ.setColorAt(1, QColor(5, 12, 5))
    p.setBrush(circ)
    p.setPen(QColor(0, 255, 0))
    p.drawEllipse(int(-s*0.85), int(-s*0.85), int(s*1.7), int(s*1.7))
    # Надпись МОЯ
    p.setPen(QColor(0, 255, 100))
    p.setFont(QFont('Segoe UI', max(8, int(s*0.5)), QFont.Weight.Bold))
    p.drawText(QRectF(-s, -s*0.3, s*2, s*0.6), Qt.AlignmentFlag.AlignCenter, 'МОЯ')
    p.restore()

def draw_globe(painter, cx, cy, s, angle, badge):
    """Диспетчер: рисует глобус-логотип для AG/POE/МОЯ"""
    b = str(badge).upper()
    if b == "POE":
        draw_globe_poe(painter, cx, cy, s, angle)
    elif b == "AG":
        draw_globe_ag(painter, cx, cy, s, angle)
    elif b == "МОЯ":
        draw_globe_mya(painter, cx, cy, s, angle)


class ThemeCard(QFrame):

    def __init__(self, name, color, badge, on_click, parent=None):
        super().__init__(parent)
        self.name = name
        self.color = color
        self.badge = badge
        self._on_click = on_click
        self.setFixedSize(170, 150)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(4, 4, 4, 4)
        lay.setSpacing(4)

        self.preview = QLabel()
        self.preview.setFixedSize(162, 112)
        self.preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(self.preview)

        self.lbl = QLabel(f"{name} · {badge}")
        self.lbl.setFixedHeight(24)
        self.lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl.setStyleSheet(f"""
            background-color: {COLORS['bg_input']};
            color: {COLORS['text_primary']};
            font-size: 10px;
            font-weight: bold;
            border-radius: 3px;
        """)
        lay.addWidget(self.lbl)

        badge_upper = str(badge).upper()
        self._globe = badge_upper in GLOBE_THEMES
        self._angle = 0
        if self._globe:
            self._timer = QTimer(self)
            self._timer.timeout.connect(self._rotate)
            self._timer.start(40)
        else:
            self._timer = None

        self._redraw()
        self.set_selected(False)

    def _rotate(self):
        self._angle = (self._angle + 3) % 360
        self._redraw()

    def _redraw(self):
        pm = QPixmap(162, 112)
        badge_upper = str(self.badge).upper()
        p = QPainter(pm)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self._globe:
            pm.fill(QColor("#000000"))
            draw_globe(p, 81, 56, 38, self._angle, badge_upper)
        else:
            pm.fill(QColor(self.color))
            p.setPen(QColor(255, 255, 255, 200))
            p.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
            p.drawText(pm.rect(), Qt.AlignmentFlag.AlignCenter, self.name)

        p.end()
        self.preview.setPixmap(pm)

    def set_selected(self, sel: bool):
        border = COLORS['accent'] if sel else COLORS['border']
        self.setStyleSheet(f"""
            ThemeCard {{
                background-color: {COLORS['bg_input']};
                border: 2px solid {border};
                border-radius: 6px;
            }}
        """)

    def mousePressEvent(self, ev):
        self._on_click(self.name, self.color, self.badge)
        super().mousePressEvent(ev)


class ThemeGallerySettings(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: transparent;")
        self.cards = {}
        self.selected_name = None
        self.selected_color = None
        self.selected_badge = None
        self.stretch_full = True
        self._preview_angle = 0
        self._preview_timer = QTimer(self)
        self._preview_timer.timeout.connect(self._preview_rotate)
        self._build_ui()
        self._load_current()

    def _preview_rotate(self):
        self._preview_angle = (self._preview_angle + 3) % 360
        if self.selected_badge and str(self.selected_badge).upper() in GLOBE_THEMES:
            self._draw_preview(self.selected_name, self.selected_color, self.selected_badge)

    def _build_ui(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(15, 15, 15, 15)
        root.setSpacing(15)

        left_frame = QFrame()
        left_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['bg_main']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
            }}
        """)
        lf_lay = QVBoxLayout(left_frame)
        lf_lay.setContentsMargins(12, 10, 12, 12)
        lf_lay.setSpacing(8)

        title = QLabel("ВСЕ ТЕМЫ")
        title.setStyleSheet("color: #00BFFF; font-size: 13px; font-weight: bold; border: none;")
        lf_lay.addWidget(title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scroll.setStyleSheet(f"""
            QScrollArea {{ background: transparent; border: none; }}
            QScrollBar:vertical {{
                background-color: {COLORS['bg_main']};
                width: 10px; border-radius: 5px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {COLORS['accent']};
                border-radius: 5px; min-height: 20px;
            }}
        """)

        grid_holder = QWidget()
        grid_holder.setStyleSheet("background: transparent; border: none;")
        gh_lay = QVBoxLayout(grid_holder)
        gh_lay.setContentsMargins(0, 0, 0, 0)
        gh_lay.setSpacing(0)

        grid_widget = QWidget()
        grid_widget.setStyleSheet("background: transparent; border: none;")
        self.grid = QGridLayout(grid_widget)
        self.grid.setSpacing(12)
        self.grid.setContentsMargins(0, 0, 0, 0)

        row, col = 0, 0
        for name, color, badge in DEFAULT_THEMES:
            card = ThemeCard(name, color, badge, self._on_click)
            self.grid.addWidget(card, row, col)
            self.cards[name] = card
            col += 1
            if col >= 6:
                col = 0
                row += 1

        self.grid.setColumnStretch(6, 1)
        gh_lay.addWidget(grid_widget)
        gh_lay.addStretch(1)

        scroll.setWidget(grid_holder)
        lf_lay.addWidget(scroll)
        root.addWidget(left_frame, stretch=1)

        right = QWidget()
        right.setFixedWidth(280)
        rl = QVBoxLayout(right)
        rl.setSpacing(10)

        self.preview = QLabel()
        self.preview.setFixedSize(260, 170)
        self.preview.setMinimumHeight(170)
        self.preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview.setStyleSheet(f"""
            background-color: {COLORS['bg_input']};
            border: 1px solid {COLORS['border']};
            border-radius: 6px;
        """)
        rl.addWidget(self.preview)

        self.lbl_name = QLabel("—")
        self.lbl_name.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 16px; font-weight: bold;")
        rl.addWidget(self.lbl_name)

        self.lbl_badge = QLabel("")
        self.lbl_badge.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 11px;")
        rl.addWidget(self.lbl_badge)

        lbl_style = QLabel("СТИЛЬ")
        lbl_style.setStyleSheet(f"color: {COLORS['accent']}; font-size: 11px; font-weight: bold;")
        rl.addWidget(lbl_style)
        self.combo_style = QComboBox()
        self.combo_style.addItems(["Default", "Compact", "Wide"])
        self.combo_style.setStyleSheet(f"""
            QComboBox {{
                background-color: {COLORS['bg_input']}; color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border']}; border-radius: 4px;
                padding: 4px 8px; min-height: 24px; max-height: 28px;
            }}
        """)
        rl.addWidget(self.combo_style)

        lbl_obs = QLabel("OBS")
        lbl_obs.setStyleSheet(f"color: {COLORS['accent']}; font-size: 11px; font-weight: bold;")
        rl.addWidget(lbl_obs)
        self.line_obs = QLineEdit()
        self.line_obs.setReadOnly(True)
        self.line_obs.setStyleSheet(f"""
            QLineEdit {{
                background-color: {COLORS['bg_input']}; color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border']}; border-radius: 4px;
                padding: 6px 8px; font-size: 11px;
            }}
        """)
        rl.addWidget(self.line_obs)

        btn_row = QWidget()
        br_lay = QHBoxLayout(btn_row)
        br_lay.setContentsMargins(0, 5, 0, 0)
        br_lay.setSpacing(8)

        self.btn_settings = QPushButton("⚙️ Редактор")
        self.btn_settings.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['bg_input']}; color: {COLORS['accent']};
                border: 2px solid {COLORS['accent']}; border-radius: 4px;
                padding: 8px 12px; font-size: 12px; font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {COLORS['accent']}; color: white;
            }}
            QPushButton:disabled {{
                color: {COLORS['border']};
                border-color: {COLORS['border']};
            }}
        """)
        self.btn_settings.clicked.connect(self._on_settings)
        self.btn_settings.setEnabled(False)
        br_lay.addWidget(self.btn_settings)

        btn_select = QPushButton("✅ Выбрать эту тему")
        btn_select.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['accent']}; color: white;
                border: none; border-radius: 4px;
                padding: 8px 12px; font-size: 12px; font-weight: bold;
            }}
            QPushButton:hover {{ background-color: #238636; }}
        """)
        btn_select.clicked.connect(self._on_select)
        br_lay.addWidget(btn_select)

        rl.addWidget(btn_row)
        rl.addStretch()
        root.addWidget(right)

    def _draw_preview(self, name, color, badge):
        pm = QPixmap(260, 170)
        badge_upper = str(badge).upper()
        p = QPainter(pm)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        if badge_upper in GLOBE_THEMES:
            pm.fill(QColor("#000000"))
            draw_globe(p, 130, 85, 62, self._preview_angle, badge_upper)
        elif badge_upper == "МОЯ":
            pm.fill(QColor("#1a1a2e"))
            p.setPen(QColor(255, 255, 255, 200))
            p.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
            p.drawText(pm.rect(), Qt.AlignmentFlag.AlignCenter, name)
        else:
            pm.fill(QColor(color))
            p.setPen(QColor(255, 255, 255, 200))
            p.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
            p.drawText(pm.rect(), Qt.AlignmentFlag.AlignCenter, name)

        p.end()
        self.preview.setPixmap(pm)

    def _on_click(self, name, color, badge):
        self.selected_name = name
        self.selected_color = color
        self.selected_badge = badge
        for n, card in self.cards.items():
            card.set_selected(n == name)
        self._draw_preview(name, color, badge)
        self.lbl_name.setText(name)
        self.lbl_badge.setText(badge)
        self.line_obs.setText(f"http://localhost:8383/themes/{name}/")
        self.btn_settings.setEnabled(True)
        # Запускаем таймер превью только для глобус-тем
        if str(badge).upper() in GLOBE_THEMES:
            self._preview_timer.start(40)
        else:
            self._preview_timer.stop()

    def _on_settings(self):
        if not self.selected_name:
            return
        from parameters.theme.editor import ThemeEditorDialog
        dlg = ThemeEditorDialog(self.selected_name, self.window())
        dlg.settings_saved.connect(self._on_settings_saved)
        dlg.exec()

    def _on_settings_saved(self, settings):
        print(f"⚙️ Настройки темы '{self.selected_name}' сохранены")

    def _on_select(self):
        if not self.selected_name:
            return
        s = SettingsManager()
        s.settings.setdefault("theme", {})["current"] = self.selected_name
        s.save()
        print(f"🎨 Тема выбрана: {self.selected_name}")

    def _load_current(self):
        s = SettingsManager()
        current = s.settings.get("theme", {}).get("current", "default")
        for name, color, badge in DEFAULT_THEMES:
            if name == current:
                self._on_click(name, color, badge)
                break

    def save_data(self):
        if self.selected_name:
            s = SettingsManager()
            s.settings.setdefault("theme", {})["current"] = self.selected_name
            s.save()
            print(f"💾 Тема сохранена: {self.selected_name}")
