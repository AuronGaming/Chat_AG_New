"""Кастомный заголовок окна"""

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from main_screen.theme_config import COLORS

class CustomTitleBar(QWidget):
    def __init__(self, title: str, parent=None, show_extra_buttons: bool = True):
        super().__init__(parent)
        self.parent_window = parent
        self.setFixedHeight(40)
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {COLORS['bg_main']};
                border-bottom: 1px solid {COLORS['border']};
            }}
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 5, 0)
        layout.setSpacing(10)

        title_label = QLabel(title)
        title_label.setStyleSheet(f"color: {COLORS['accent']}; font-size: 14px; font-weight: bold;")
        layout.addWidget(title_label)
        layout.addStretch()

        if show_extra_buttons:
            # Кнопка звука
            self.btn_sound = QPushButton("🔊")
            self.btn_sound.setFixedSize(30, 30)
            self.btn_sound.setStyleSheet(self._btn_style())
            self.btn_sound.clicked.connect(self._on_sound_toggle)
            layout.addWidget(self.btn_sound)

            # Кнопка настроек
            self.btn_settings = QPushButton("⚙")
            self.btn_settings.setFixedSize(30, 30)
            self.btn_settings.setStyleSheet(self._btn_style())
            self.btn_settings.clicked.connect(self._on_settings)
            layout.addWidget(self.btn_settings)

        # Кнопки управления окном
        btn_minimize = QPushButton("—")
        btn_minimize.setFixedSize(30, 30)
        btn_minimize.setStyleSheet(self._btn_style())
        btn_minimize.clicked.connect(self._on_minimize)
        layout.addWidget(btn_minimize)

        btn_maximize = QPushButton("□")
        btn_maximize.setFixedSize(30, 30)
        btn_maximize.setStyleSheet(self._btn_style())
        btn_maximize.clicked.connect(self._on_maximize)
        layout.addWidget(btn_maximize)

        btn_close = QPushButton("✕")
        btn_close.setFixedSize(30, 30)
        btn_close.setStyleSheet(self._btn_style_close())
        btn_close.clicked.connect(self._on_close)
        layout.addWidget(btn_close)

        self.sound_enabled = True

    def _on_sound_toggle(self):
        self.sound_enabled = not self.sound_enabled
        self.btn_sound.setText("🔊" if self.sound_enabled else "🔇")
        self.btn_sound.setStyleSheet(self._btn_style() if self.sound_enabled else self._btn_style_muted())
        if self.parent_window and hasattr(self.parent_window, 'toggle_sound'):
            self.parent_window.toggle_sound(self.sound_enabled)

    def _btn_style(self) -> str:
        return f"""
            QPushButton {{ background-color: transparent; color: {COLORS['text_primary']}; border: 1px solid {COLORS['accent']}; border-radius: 4px; font-size:  the 14px; }}
            QPushButton:hover {{ background-color: {COLORS['accent']}30; }}
        """

    def _btn_style_muted(self) -> str:
        return f"""
            QPushButton {{ background-color: transparent; color: {COLORS['text_secondary']}; border: 1px solid {COLORS['border']}; border-radius: 4px; font-size: 14px; }}
            QPushButton:hover {{ background-color: {COLORS['accent']}30; }}
        """

    def _btn_style_close(self) -> str:
        return f"""
            QPushButton {{ background-color: transparent; color: {COLORS['text_primary']}; border: 1px solid {COLORS['accent']}; border-radius: 4px; font-size: 14px; }}
            QPushButton:hover {{ background-color: {COLORS.get('error', '#dc3545')}; color: white; border-color: {COLORS.get('error', '#dc3545')}; }}
        """

    def _on_settings(self):
        if self.parent_window and hasattr(self.parent_window, 'open_settings'):
            self.parent_window.open_settings()

    def _on_minimize(self):
        if self.parent_window: self.parent_window.hide()

    def _on_maximize(self):
        if self.parent_window:
            self.parent_window.showMaximized() if not self.parent_window.isMaximized() else self.parent_window.showNormal()

    def _on_close(self):
        if self.parent_window: self.parent_window.close()