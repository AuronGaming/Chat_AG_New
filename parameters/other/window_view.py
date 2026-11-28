"""Панель Вид лицевого окна"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QCheckBox, QSlider, QSpinBox, QGroupBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from main_screen.theme_config import COLORS
from main_screen.checkbox_style import checkbox_style


class WindowViewPanel(QWidget):
    transparency_changed = pyqtSignal(int)
    click_through_changed = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: transparent;")
        self._updating = False
        self._build_ui()

    def _build_ui(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(15, 15, 15, 10)
        lay.setSpacing(12)

        title = QLabel("👁️ Вид лицевого окна")
        title.setStyleSheet(f"font-size: 22px; color: {COLORS['accent']}; font-weight: bold;")
        lay.addWidget(title)

        trans_group = QGroupBox("ПРОЗРАЧНОСТЬ")
        trans_group.setStyleSheet(self._group_style())
        trans_lay = QVBoxLayout(trans_group)
        trans_lay.setContentsMargins(15, 20, 15, 15)
        trans_lay.setSpacing(10)

        trans_row = QHBoxLayout()
        lbl_trans = QLabel("Прозрачность:")
        lbl_trans.setFixedWidth(150)
        lbl_trans.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 12px;")
        trans_row.addWidget(lbl_trans)
        self.spin_transparency = QSpinBox()
        self.spin_transparency.setRange(0, 100)
        self.spin_transparency.setValue(0)
        self.spin_transparency.setSuffix("%")
        self.spin_transparency.setFixedWidth(80)
        self.spin_transparency.setStyleSheet(self._spin_style())
        trans_row.addWidget(self.spin_transparency)
        trans_row.addStretch()
        trans_lay.addLayout(trans_row)

        self.slider_transparency = QSlider(Qt.Orientation.Horizontal)
        self.slider_transparency.setRange(0, 100)
        self.slider_transparency.setValue(0)
        self.slider_transparency.setStyleSheet(self._slider_style())
        trans_lay.addWidget(self.slider_transparency)
        self.slider_transparency.valueChanged.connect(self._on_trans_slider)
        self.spin_transparency.valueChanged.connect(self._on_trans_spin)
        lay.addWidget(trans_group)

        click_group = QGroupBox("СКВОЗНЫЕ КЛИКИ")
        click_group.setStyleSheet(self._group_style())
        click_lay = QVBoxLayout(click_group)
        click_lay.setContentsMargins(15, 20, 15, 15)
        click_lay.setSpacing(10)
        self.cb_click_through = QCheckBox("Сквозные клики (не кликабельное окно)")
        self.cb_click_through.setStyleSheet(self._checkbox_style())
        self.cb_click_through.setToolTip("Если включено, клики будут проходить сквозь окно")
        self.cb_click_through.clicked.connect(self._on_click_through)
        click_lay.addWidget(self.cb_click_through)
        hint = QLabel("Полезно для OBS-оверлеев: окно видно, но не перехватывает мышь")
        hint.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 10px; font-style: italic;")
        click_lay.addWidget(hint)
        lay.addWidget(click_group)

        lay.addStretch()

    def _group_style(self) -> str:
        return f"""
            QGroupBox {{
                color: {COLORS['accent']};
                font-size: 13px;
                font-weight: bold;
                border: 1px solid {COLORS['accent']};
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }}
        """

    def _on_trans_slider(self, value):
        if not self._updating:
            self._updating = True
            self.spin_transparency.setValue(value)
            self._updating = False
            self.transparency_changed.emit(value)

    def _on_trans_spin(self, value):
        if not self._updating:
            self._updating = True
            self.slider_transparency.setValue(value)
            self._updating = False
            self.transparency_changed.emit(value)

    def _on_click_through(self, checked):
        self.click_through_changed.emit(checked)

    def _checkbox_style(self) -> str:
        return checkbox_style(
            text_color=COLORS['text_primary'],
            border_color=COLORS['border'],
            bg_color=COLORS['bg_input'],
            accent_color=COLORS['accent']
        )

    def _slider_style(self) -> str:
        return f"""
            QSlider::groove:horizontal {{
                border: 1px solid {COLORS['border']};
                height: 6px;
                background: {COLORS['bg_input']};
                border-radius: 3px;
            }}
            QSlider::handle:horizontal {{
                background: {COLORS['accent']};
                border: 1px solid {COLORS['accent']};
                width: 16px;
                margin: -6px 0;
                border-radius: 8px;
            }}
            QSlider::handle:horizontal:hover {{ background: #238636; }}
            QSlider::sub-page:horizontal {{ background: {COLORS['accent']}; border-radius: 3px; }}
        """

    def _spin_style(self) -> str:
        return f"""
            QSpinBox {{
                background-color: {COLORS['bg_input']};
                color: {COLORS['text_primary']};
                border: 1px solid {COLORS['accent']};
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 12px;
            }}
        """

    def load_data(self, config: dict):
        self._updating = True
        self.spin_transparency.setValue(config.get("transparency", 0))
        self.slider_transparency.setValue(config.get("transparency", 0))
        self.cb_click_through.setChecked(config.get("click_through", False))
        self._updating = False

    def save_data(self) -> dict:
        return {
            "transparency": self.spin_transparency.value(),
            "click_through": self.cb_click_through.isChecked(),
        }