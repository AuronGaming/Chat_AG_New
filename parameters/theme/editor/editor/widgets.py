"""Кастомные виджеты для редактора тем"""
from PyQt6.QtWidgets import QPushButton, QColorDialog
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QColor
from main_screen.theme_config import COLORS


class ColorButton(QPushButton):
    """Кнопка выбора цвета с превью"""
    color_changed = pyqtSignal(str)

    def __init__(self, color="#FF9900", parent=None):
        super().__init__(parent)
        self._color = color
        self.setFixedSize(36, 28)
        self.clicked.connect(self._pick)
        self._repaint()

    def _repaint(self):
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {self._color};
                border: 2px solid {COLORS['border']};
                border-radius: 4px;
            }}
            QPushButton:hover {{ border-color: {COLORS['accent']}; }}
        """)

    def _pick(self):
        c = QColorDialog.getColor(QColor(self._color), self, "Выберите цвет")
        if c.isValid():
            self._color = c.name()
            self._repaint()
            self.color_changed.emit(self._color)

    def set_color(self, color):
        self._color = color
        self._repaint()

    def get_color(self):
        return self._color


class EffectButtons:
    """Группа кнопок эффектов (только одна активна)"""

    def __init__(self, effects: list, default: str):
        self.buttons = {}
        self.effects = effects
        self.default = default

    def create(self, parent_layout, on_change=None):
        """Создать кнопки в layout (QGridLayout)"""
        for i, eff in enumerate(self.effects):
            b = QPushButton(eff)
            b.setCheckable(True)
            b.setChecked(eff == self.default)
            b.setStyleSheet(self._style(eff == self.default))
            if on_change:
                b.clicked.connect(lambda _, e=eff: self._select(e, on_change))
            self.buttons[eff] = b
            parent_layout.addWidget(b, i // 5, i % 5)

    def _select(self, selected, on_change):
        for name, btn in self.buttons.items():
            is_sel = (name == selected)
            btn.setChecked(is_sel)
            btn.setStyleSheet(self._style(is_sel))
        if on_change:
            on_change(selected)

    def _style(self, checked):
        if checked:
            return f"""
                QPushButton {{
                    background-color: {COLORS['accent']}; color: white;
                    border: 1px solid {COLORS['accent']}; border-radius: 4px;
                    padding: 4px 10px; font-size: 11px; min-width: 80px;
                }}
            """
        return f"""
            QPushButton {{
                background-color: {COLORS['bg_input']}; color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border']}; border-radius: 4px;
                padding: 4px 10px; font-size: 11px; min-width: 80px;
            }}
            QPushButton:hover {{ background-color: {COLORS['bg_hover']}; }}
        """

    def get_selected(self) -> str:
        for name, btn in self.buttons.items():
            if btn.isChecked():
                return name
        return self.default