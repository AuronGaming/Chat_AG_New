"""Секция Прочее — показывает панель выбранного подпункта"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import pyqtSignal
from main_screen.theme_config import COLORS

from parameters.other.activation import ActivationPanel
from parameters.other.window_view import WindowViewPanel
from parameters.other.about import AboutPanel


class OtherSection(QWidget):
    """Панель для подпункта секции 'Прочее'."""

    activation_requested = pyqtSignal(str, str)
    transparency_changed = pyqtSignal(int)
    click_through_changed = pyqtSignal(bool)

    def __init__(self, subsection: str = "Активация", parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"background-color: {COLORS['bg_main']};")

        lay = QVBoxLayout(self)
        lay.setContentsMargins(15, 15, 15, 15)
        lay.setSpacing(0)

        self.activation_panel = ActivationPanel()
        self.window_view_panel = WindowViewPanel()
        self.about_panel = AboutPanel()

        self.activation_panel.activation_requested.connect(self.activation_requested.emit)
        self.window_view_panel.transparency_changed.connect(self.transparency_changed.emit)
        self.window_view_panel.click_through_changed.connect(self.click_through_changed.emit)

        if subsection == "Активация":
            lay.addWidget(self.activation_panel)
        elif subsection == "О программе":
            lay.addWidget(self.about_panel)
        else:
            lay.addWidget(self.window_view_panel)

        self._load_all_data()

    def _load_all_data(self):
        from core.settings_manager import SettingsManager
        s = SettingsManager()
        other_cfg = s.settings.get("other", {})
        self.activation_panel.load_data(other_cfg)
        self.window_view_panel.load_data(other_cfg)

    def save_data(self):
        from core.settings_manager import SettingsManager
        s = SettingsManager()
        other = s.settings.get("other", {})
        other.update(self.activation_panel.save_data())
        other.update(self.window_view_panel.save_data())
        s.settings["other"] = other
        s.save()
        print("💾 Настройки раздела Прочее сохранены")