"""Настройки статистики"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QSpinBox, QGroupBox, QHBoxLayout, QLabel, QCheckBox
from parameters.general.visual import GROUP_BOX_STYLE, CHECKBOX_STYLE, INPUT_STYLE, COMBO_STYLE
from core.settings_manager import SettingsManager


class StatisticsSettings(QWidget):
    """Настройки статистики"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"background-color: transparent;")

        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(10)

        # Загружаем настройки
        s = SettingsManager()
        general = s.settings.get("general", {})

        # Статистика
        stats_row = QHBoxLayout()
        lbl_stats = QLabel("Статистика:")
        lbl_stats.setFixedWidth(250)
        lbl_stats.setStyleSheet(f"color: {self._get_color('text_primary')}; font-size: 12px;")
        stats_row.addWidget(lbl_stats)

        self.combo_stats = QComboBox()
        self.combo_stats.addItems(["Показывать статистику", "Не показывать", "Только при проблемах"])
        self.combo_stats.setCurrentIndex(general.get("stats_mode", 0))
        self.combo_stats.setStyleSheet(COMBO_STYLE)
        stats_row.addWidget(self.combo_stats, stretch=1)
        lay.addLayout(stats_row)

        # Иконки сайтов
        icons_row = QHBoxLayout()
        lbl_icons = QLabel("Иконки сайтов:")
        lbl_icons.setFixedWidth(250)
        lbl_icons.setStyleSheet(f"color: {self._get_color('text_primary')}; font-size: 12px;")
        icons_row.addWidget(lbl_icons)

        self.combo_icons = QComboBox()
        self.combo_icons.addItems(["Отображать всегда", "Отображать только при проблемах", "Не отображать"])
        self.combo_icons.setCurrentIndex(general.get("icons_mode", 1))
        self.combo_icons.setStyleSheet(COMBO_STYLE)
        icons_row.addWidget(self.combo_icons, stretch=1)
        lay.addLayout(icons_row)

        # Суммы агрегаторов
        sums_row = QHBoxLayout()
        lbl_sums = QLabel("Суммы агрегаторов:")
        lbl_sums.setFixedWidth(250)
        lbl_sums.setStyleSheet(f"color: {self._get_color('text_primary')}; font-size: 12px;")
        sums_row.addWidget(lbl_sums)

        self.combo_sums = QComboBox()
        self.combo_sums.addItems(["В счетчике онлайна", "Отдельно", "Не показывать"])
        self.combo_sums.setCurrentIndex(general.get("sums_mode", 0))
        self.combo_sums.setStyleSheet(COMBO_STYLE)
        sums_row.addWidget(self.combo_sums, stretch=1)
        lay.addLayout(sums_row)

        self.cb_likes = QCheckBox("Показывать количество лайков и дизлайков")
        self.cb_likes.setChecked(general.get("likes", False))
        self.cb_likes.setStyleSheet(CHECKBOX_STYLE)
        lay.addWidget(self.cb_likes)

        # Интервал обновления
        interval_row = QHBoxLayout()
        lbl_interval = QLabel("Интервал обновления:")
        lbl_interval.setFixedWidth(250)
        lbl_interval.setStyleSheet(f"color: {self._get_color('text_primary')}; font-size: 12px;")
        interval_row.addWidget(lbl_interval)

        self.spin_interval = QSpinBox()
        self.spin_interval.setRange(1, 60)
        self.spin_interval.setValue(general.get("update_interval", 5))
        self.spin_interval.setSuffix(" минут")
        self.spin_interval.setStyleSheet(INPUT_STYLE)
        interval_row.addWidget(self.spin_interval)
        lay.addLayout(interval_row)

    def _get_color(self, name: str) -> str:
        from main_screen.theme_config import COLORS
        return COLORS.get(name, "#ffffff")

    def save_data(self):
        s = SettingsManager()
        general = s.settings.get("general", {})

        general["stats_mode"] = self.combo_stats.currentIndex()
        general["icons_mode"] = self.combo_icons.currentIndex()
        general["sums_mode"] = self.combo_sums.currentIndex()
        general["likes"] = self.cb_likes.isChecked()
        general["update_interval"] = self.spin_interval.value()

        s.settings["general"] = general
        s.save()