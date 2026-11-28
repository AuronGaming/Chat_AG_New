"""Настройки звукового события"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox,
    QLineEdit, QPushButton, QComboBox, QSpinBox, QFileDialog
)
from main_screen.theme_config import COLORS, checkbox_style, combo_style, spin_style, input_style, green_button_style, \
    browse_button_style
from parameters.sound.audio import play_sound


class EventSettings(QWidget):
    """Настройки одного события"""

    def __init__(self, event_id: str, info: dict, parent=None):
        super().__init__(parent)
        self.event_id = event_id
        self.info = info
        self._build_ui()

    def _build_ui(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(15, 15, 15, 10)
        lay.setSpacing(12)

        title = QLabel(f"{self.info['icon']} {self.info['name']}")
        title.setStyleSheet(f"font-size: 20px; color: {COLORS['accent']}; font-weight: bold;")
        lay.addWidget(title)

        self.cb_enabled = QCheckBox("Включить звук")
        self.cb_enabled.setStyleSheet(checkbox_style(bold=True))
        lay.addWidget(self.cb_enabled)

        # Звук
        sound_row = QHBoxLayout()
        lbl = QLabel("Звук:")
        lbl.setFixedWidth(120)
        lbl.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 12px;")
        sound_row.addWidget(lbl)

        self.combo_sound = QComboBox()
        self.combo_sound.addItems(["По умолчанию", "Без звука", "Свой файл..."])
        self.combo_sound.setStyleSheet(combo_style())
        self.combo_sound.currentTextChanged.connect(self._on_sound_changed)
        sound_row.addWidget(self.combo_sound, stretch=1)
        lay.addLayout(sound_row)

        # Путь к файлу (скрыт по умолчанию)
        self.file_row = QHBoxLayout()
        lbl_file = QLabel("Файл:")
        lbl_file.setFixedWidth(120)
        lbl_file.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 12px;")
        self.file_row.addWidget(lbl_file)

        self.input_file = QLineEdit()
        self.input_file.setPlaceholderText("C:\\sounds\\alert.wav")
        self.input_file.setStyleSheet(input_style())
        self.file_row.addWidget(self.input_file, stretch=1)

        btn_browse = QPushButton("...")
        btn_browse.setFixedWidth(40)
        btn_browse.setStyleSheet(browse_button_style())
        btn_browse.clicked.connect(self._browse_file)
        self.file_row.addWidget(btn_browse)
        lay.addLayout(self.file_row)

        self.file_row.itemAt(0).widget().setVisible(False)
        self.input_file.setVisible(False)
        btn_browse.setVisible(False)

        # Громкость
        volume_row = QHBoxLayout()
        lbl = QLabel("Громкость:")
        lbl.setFixedWidth(120)
        lbl.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 12px;")
        volume_row.addWidget(lbl)

        self.spin_volume = QSpinBox()
        self.spin_volume.setRange(0, 100)
        self.spin_volume.setValue(100)
        self.spin_volume.setSuffix("%")
        self.spin_volume.setStyleSheet(spin_style())
        volume_row.addWidget(self.spin_volume)
        lay.addLayout(volume_row)

        # Шаблон фразы
        lbl_tpl = QLabel("Шаблон фразы:")
        lbl_tpl.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 12px;")
        lay.addWidget(lbl_tpl)

        self.input_template = QLineEdit()
        self.input_template.setPlaceholderText("$name подписался")
        self.input_template.setStyleSheet(input_style())
        lay.addWidget(self.input_template)

        hint = QLabel("Переменные: $name, $amount, $currency, $text")
        hint.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 10px; font-style: italic;")
        lay.addWidget(hint)

        # Кнопка Тест
        btn_test = QPushButton("🔊 Тест")
        btn_test.setFixedHeight(35)
        btn_test.setStyleSheet(green_button_style(height=35))
        btn_test.clicked.connect(self._on_test)
        lay.addWidget(btn_test)

        lay.addStretch()

    def _on_sound_changed(self, text):
        show = (text == "Свой файл...")
        self.file_row.itemAt(0).widget().setVisible(show)
        self.input_file.setVisible(show)
        for i in range(self.file_row.count()):
            item = self.file_row.itemAt(i)
            if item and item.widget() and isinstance(item.widget(), QPushButton):
                item.widget().setVisible(show)

    def _browse_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Выбрать звук", "",
                                              "Audio Files (*.wav *.mp3 *.ogg)")
        if file:
            self.input_file.setText(file)

    def _on_test(self):
        play_sound(self.input_file.text())

    def load_data(self, config: dict):
        self.cb_enabled.setChecked(config.get("enabled", False))
        self.spin_volume.setValue(config.get("volume", 100))
        self.input_template.setText(config.get("template", ""))

    def save_data(self) -> dict:
        return {
            "enabled": self.cb_enabled.isChecked(),
            "sound": self.combo_sound.currentText(),
            "sound_file": self.input_file.text(),
            "volume": self.spin_volume.value(),
            "template": self.input_template.text(),
        }