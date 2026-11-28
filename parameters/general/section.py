"""Секция Общие настройки — основной виджет"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox
from parameters.general.chat import ChatSettings
from parameters.general.statistics import StatisticsSettings
from parameters.general.links_filters import LinksFiltersSettings
from parameters.general.window_behavior import WindowBehaviorSettings
from parameters.general.visual import SECTION_TITLE_STYLE, SECTION_SUBTITLE_STYLE, GROUP_BOX_STYLE


class GeneralSection(QWidget):
    """Секция общих настроек"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"background-color: transparent;")

        lay = QVBoxLayout(self)
        lay.setContentsMargins(20, 15, 20, 15)
        lay.setSpacing(15)

        # Заголовок
        title = QLabel("Общие")
        title.setStyleSheet(SECTION_TITLE_STYLE)
        lay.addWidget(title)

        sub = QLabel("Основные параметры окна, чата, модулей и статистики.")
        sub.setStyleSheet(SECTION_SUBTITLE_STYLE)
        lay.addWidget(sub)

        # Чат
        chat_group = QGroupBox("ЧАТ")
        chat_group.setStyleSheet(GROUP_BOX_STYLE)
        chat_lay = QVBoxLayout(chat_group)
        chat_lay.setContentsMargins(10, 15, 10, 10)
        chat_settings = ChatSettings()
        chat_lay.addWidget(chat_settings)
        lay.addWidget(chat_group)

        # Статистика
        stats_group = QGroupBox("СТАТИСТИКА")
        stats_group.setStyleSheet(GROUP_BOX_STYLE)
        stats_lay = QVBoxLayout(stats_group)
        stats_lay.setContentsMargins(10, 15, 10, 10)
        stats_settings = StatisticsSettings()
        stats_lay.addWidget(stats_settings)
        lay.addWidget(stats_group)

        # Ссылки и фильтры
        links_group = QGroupBox("ССЫЛКИ И ФИЛЬТРЫ")
        links_group.setStyleSheet(GROUP_BOX_STYLE)
        links_lay = QVBoxLayout(links_group)
        links_lay.setContentsMargins(10, 15, 10, 10)
        links_settings = LinksFiltersSettings()
        links_lay.addWidget(links_settings)
        lay.addWidget(links_group)

        # Поведение окна
        window_group = QGroupBox("ПОВЕДЕНИЕ ОКНА")
        window_group.setStyleSheet(GROUP_BOX_STYLE)
        window_lay = QVBoxLayout(window_group)
        window_lay.setContentsMargins(10, 15, 10, 10)
        window_settings = WindowBehaviorSettings()
        window_lay.addWidget(window_settings)
        lay.addWidget(window_group)

        lay.addStretch()

        # Сохраняем ссылки на подвиджеты для save_data
        self._chat = chat_settings
        self._stats = stats_settings
        self._links = links_settings
        self._window = window_settings

    def save_data(self):
        self._chat.save_data()
        self._stats.save_data()
        self._links.save_data()
        self._window.save_data()
        print("💾 Общие настройки сохранены")