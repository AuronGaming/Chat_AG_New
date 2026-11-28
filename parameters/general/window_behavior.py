"""Настройки поведения окна"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QGroupBox
from parameters.general.visual import GROUP_BOX_STYLE, CHECKBOX_STYLE
from core.settings_manager import SettingsManager


class WindowBehaviorSettings(QWidget):
    """Настройки поведения окна"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"background-color: transparent;")

        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(10)

        # Загружаем настройки
        s = SettingsManager()
        general = s.settings.get("general", {})

        self.cb_always_on_top = QCheckBox("Окно поверх всех окон")
        self.cb_always_on_top.setChecked(general.get("always_on_top", False))
        self.cb_always_on_top.setStyleSheet(CHECKBOX_STYLE)
        lay.addWidget(self.cb_always_on_top)

        self.cb_save_history = QCheckBox("Сохранять историю чата")
        self.cb_save_history.setChecked(general.get("save_history", False))
        self.cb_save_history.setStyleSheet(CHECKBOX_STYLE)
        lay.addWidget(self.cb_save_history)

        self.cb_gpu = QCheckBox("GPU-ускорение")
        self.cb_gpu.setChecked(general.get("gpu_acceleration", False))
        self.cb_gpu.setStyleSheet(CHECKBOX_STYLE)
        self.cb_gpu.setToolTip("Использование видеокарты для рендеринга")
        lay.addWidget(self.cb_gpu)

    def save_data(self):
        s = SettingsManager()
        general = s.settings.get("general", {})

        general["always_on_top"] = self.cb_always_on_top.isChecked()
        general["save_history"] = self.cb_save_history.isChecked()
        general["gpu_acceleration"] = self.cb_gpu.isChecked()

        s.settings["general"] = general
        s.save()