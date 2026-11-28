"""Секция Звук — главный виджет"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QLabel
from parameters.sound.voice import VoiceSettings
from parameters.sound.events import EventSettings
from parameters.sound.visual import SECTION_TITLE_STYLE, SECTION_SUBTITLE_STYLE
from core.settings_manager import SettingsManager

# Конфигурация событий
EVENTS = {
    "message": {"name": "Новое сообщение", "icon": "💬"},
    "donate": {"name": "Донат", "icon": "💰"},
    "subscribe": {"name": "Подписка", "icon": "⭐"},
}


class SoundSection(QWidget):
    """Секция настроек звука"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: transparent;")

        lay = QVBoxLayout(self)
        lay.setContentsMargins(20, 15, 20, 15)
        lay.setSpacing(15)

        # Заголовок
        title = QLabel("Звук")
        title.setStyleSheet(SECTION_TITLE_STYLE)
        lay.addWidget(title)

        sub = QLabel("Настройки озвучки и звуковых событий.")
        sub.setStyleSheet(SECTION_SUBTITLE_STYLE)
        lay.addWidget(sub)

        # Вкладки
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(self._tab_style())

        # Вкладка 1: Озвучка
        self.voice_panel = VoiceSettings()
        self.tabs.addTab(self.voice_panel, "🔊 Озвучка")

        # Вкладка 2: События (донат как пример)
        self.donate_panel = EventSettings("donate", EVENTS["donate"])
        self.tabs.addTab(self.donate_panel, "💰 Донат")

        lay.addWidget(self.tabs)
        lay.addStretch()

    def _tab_style(self) -> str:
        from main_screen.theme_config import COLORS
        return f"""
            QTabWidget::pane {{ border: 1px solid {COLORS['border']}; border-radius: 4px; }}
            QTabBar::tab {{ 
                background: {COLORS['bg_input']}; color: {COLORS['text_primary']}; 
                padding: 8px 16px; border-top-left-radius: 4px; border-top-right-radius: 4px; 
            }}
            QTabBar::tab:selected {{ background: {COLORS['accent']}; color: white; }}
        """

    def load_data(self):
        s = SettingsManager()
        config = s.settings
        self.voice_panel.load_data(config.get("tts", {}))
        events_cfg = config.get("events", {})
        self.donate_panel.load_data(events_cfg.get("donate", {}))

    def save_data(self):
        s = SettingsManager()
        s.settings["tts"] = self.voice_panel.save_data()
        if "events" not in s.settings:
            s.settings["events"] = {}
        s.settings["events"]["donate"] = self.donate_panel.save_data()
        s.save()
        print("💾 Настройки звука сохранены")