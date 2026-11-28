"""Настройки озвучки (TTS) — с ползунками и вводом чисел"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox,
    QLineEdit, QPushButton, QComboBox, QSlider, QSpinBox, QGroupBox
)
from PyQt6.QtCore import Qt
from main_screen.theme_config import COLORS
from main_screen.checkbox_style import checkbox_style
from parameters.sound.audio import get_voices, speak


class VoiceSettings(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._updating = False
        self._build_ui()

    def _build_ui(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(15, 15, 15, 10)
        lay.setSpacing(15)

        title_row = QHBoxLayout()
        title_icon = QLabel("🔊")
        title_icon.setStyleSheet(f"font-size: 22px; color: {COLORS['accent']};")
        title_row.addWidget(title_icon)
        title = QLabel("Озвучка")
        title.setStyleSheet(f"font-size: 22px; color: {COLORS['accent']}; font-weight: bold;")
        title_row.addWidget(title)
        title_row.addStretch()
        lay.addLayout(title_row)

        main_group = QGroupBox("ОСНОВНЫЕ НАСТРОЙКИ")
        main_group.setStyleSheet(self._group_style())
        main_lay = QVBoxLayout(main_group)
        main_lay.setContentsMargins(15, 20, 15, 15)
        main_lay.setSpacing(12)

        self.cb_enabled = QCheckBox("Включить озвучку")
        self.cb_enabled.setStyleSheet(self._checkbox_style())
        main_lay.addWidget(self.cb_enabled)

        voice_row = QHBoxLayout()
        lbl = QLabel("Голос:")
        lbl.setFixedWidth(120)
        lbl.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 12px;")
        voice_row.addWidget(lbl)
        self.combo_voice = QComboBox()
        for voice_id, voice_name in get_voices():
            self.combo_voice.addItem(voice_name, voice_id)
        self.combo_voice.setStyleSheet(self._combo_style())
        voice_row.addWidget(self.combo_voice, stretch=1)
        main_lay.addLayout(voice_row)
        lay.addWidget(main_group)

        params_group = QGroupBox("ПАРАМЕТРЫ РЕЧИ")
        params_group.setStyleSheet(self._group_style())
        params_lay = QVBoxLayout(params_group)
        params_lay.setContentsMargins(15, 20, 15, 15)
        params_lay.setSpacing(15)

        speed_lay = QVBoxLayout()
        speed_header = QHBoxLayout()
        lbl_speed = QLabel("Скорость:")
        lbl_speed.setFixedWidth(120)
        lbl_speed.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 12px;")
        speed_header.addWidget(lbl_speed)
        self.spin_speed = QSpinBox()
        self.spin_speed.setRange(50, 300)
        self.spin_speed.setValue(200)
        self.spin_speed.setFixedWidth(80)
        self.spin_speed.setStyleSheet(self._spin_style())
        speed_header.addWidget(self.spin_speed)
        speed_header.addStretch()
        speed_lay.addLayout(speed_header)
        self.slider_speed = QSlider(Qt.Orientation.Horizontal)
        self.slider_speed.setRange(50, 300)
        self.slider_speed.setValue(200)
        self.slider_speed.setStyleSheet(self._slider_style())
        speed_lay.addWidget(self.slider_speed)
        self.slider_speed.valueChanged.connect(self._on_speed_slider)
        self.spin_speed.valueChanged.connect(self._on_speed_spin)
        params_lay.addLayout(speed_lay)

        volume_lay = QVBoxLayout()
        volume_header = QHBoxLayout()
        lbl_volume = QLabel("Громкость:")
        lbl_volume.setFixedWidth(120)
        lbl_volume.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 12px;")
        volume_header.addWidget(lbl_volume)
        self.spin_volume = QSpinBox()
        self.spin_volume.setRange(0, 100)
        self.spin_volume.setValue(100)
        self.spin_volume.setSuffix("%")
        self.spin_volume.setFixedWidth(80)
        self.spin_volume.setStyleSheet(self._spin_style())
        volume_header.addWidget(self.spin_volume)
        volume_header.addStretch()
        volume_lay.addLayout(volume_header)
        self.slider_volume = QSlider(Qt.Orientation.Horizontal)
        self.slider_volume.setRange(0, 100)
        self.slider_volume.setValue(100)
        self.slider_volume.setStyleSheet(self._slider_style())
        volume_lay.addWidget(self.slider_volume)
        self.slider_volume.valueChanged.connect(self._on_volume_slider)
        self.spin_volume.valueChanged.connect(self._on_volume_spin)
        params_lay.addLayout(volume_lay)
        lay.addWidget(params_group)

        template_group = QGroupBox("ШАБЛОН ОЗВУЧКИ")
        template_group.setStyleSheet(self._group_style())
        template_lay = QVBoxLayout(template_group)
        template_lay.setContentsMargins(15, 20, 15, 15)
        template_lay.setSpacing(10)
        lbl_tpl = QLabel("Формат текста:")
        lbl_tpl.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 12px;")
        template_lay.addWidget(lbl_tpl)
        self.input_template = QLineEdit()
        self.input_template.setPlaceholderText("$username: $text")
        self.input_template.setStyleSheet(self._input_style())
        template_lay.addWidget(self.input_template)
        hint = QLabel("Переменные: $username — ник, $message — сообщение, $text — полный текст")
        hint.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 10px; font-style: italic; padding-top: 5px;")
        template_lay.addWidget(hint)
        lay.addWidget(template_group)

        btn_test = QPushButton("🔊 Тест озвучки")
        btn_test.setFixedHeight(40)
        btn_test.setStyleSheet(self._button_style())
        btn_test.clicked.connect(self._on_test)
        lay.addWidget(btn_test)
        lay.addStretch()

    def _on_speed_slider(self, value):
        if not self._updating:
            self._updating = True
            self.spin_speed.setValue(value)
            self._updating = False

    def _on_speed_spin(self, value):
        if not self._updating:
            self._updating = True
            self.slider_speed.setValue(value)
            self._updating = False

    def _on_volume_slider(self, value):
        if not self._updating:
            self._updating = True
            self.spin_volume.setValue(value)
            self._updating = False

    def _on_volume_spin(self, value):
        if not self._updating:
            self._updating = True
            self.slider_volume.setValue(value)
            self._updating = False

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

    def _checkbox_style(self) -> str:
        return checkbox_style(
            text_color=COLORS['text_primary'],
            border_color=COLORS['border'],
            bg_color=COLORS['bg_input'],
            accent_color=COLORS['accent']
        )

    def _combo_style(self) -> str:
        return f"""
            QComboBox {{
                background-color: {COLORS['bg_input']};
                color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                padding: 6px 10px;
                font-size: 12px;
            }}
            QComboBox::drop-down {{ border: none; width: 20px; }}
            QComboBox QAbstractItemView {{
                background-color: {COLORS['bg_input']};
                color: {COLORS['text_primary']};
                border: 1px solid {COLORS['accent']};
                selection-background-color: {COLORS['accent']};
                selection-color: white;
                outline: none;
            }}
            QComboBox QAbstractItemView::item {{
                color: {COLORS['text_primary']};
                padding: 6px 10px;
                min-height: 24px;
            }}
            QComboBox QAbstractItemView::item:selected {{
                background-color: {COLORS['accent']};
                color: white;
            }}
            QComboBox QAbstractItemView::item:hover {{
                background-color: {COLORS['bg_hover']};
            }}
        """

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

    def _input_style(self) -> str:
        return f"""
            QLineEdit {{
                background-color: {COLORS['bg_input']};
                color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                padding: 6px 10px;
                font-size: 12px;
            }}
        """

    def _button_style(self) -> str:
        return f"""
            QPushButton {{
                background-color: {COLORS['accent']};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: bold;
            }}
            QPushButton:hover {{ background-color: #238636; }}
        """

    def _on_test(self):
        text = self.input_template.text() or "Тест озвучки Chat AG"
        text = text.replace("$username", "Тест").replace("$message", "Привет").replace("$text", "Привет")
        speak(text, self.combo_voice.currentData(), rate=self.spin_speed.value(), volume=self.spin_volume.value())

    def load_data(self, config: dict):
        self._updating = True
        self.cb_enabled.setChecked(config.get('enabled', False))
        voice_id = config.get('voice', '')
        if voice_id:
            idx = self.combo_voice.findData(voice_id)
            if idx >= 0:
                self.combo_voice.setCurrentIndex(idx)
        speed = config.get('speed', 200)
        volume = config.get('volume', 100)
        self.spin_speed.setValue(speed)
        self.slider_speed.setValue(speed)
        self.spin_volume.setValue(volume)
        self.slider_volume.setValue(volume)
        self.input_template.setText(config.get('template', '$text'))
        self._updating = False

    def save_data(self) -> dict:
        return {
            'enabled': self.cb_enabled.isChecked(),
            'voice': self.combo_voice.currentData(),
            'speed': self.spin_speed.value(),
            'volume': self.spin_volume.value(),
            'template': self.input_template.text(),
        }