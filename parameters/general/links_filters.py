"""Настройки ссылок и фильтров"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QLineEdit, QGroupBox, QHBoxLayout, QLabel
from parameters.general.visual import GROUP_BOX_STYLE, CHECKBOX_STYLE, INPUT_STYLE
from core.settings_manager import SettingsManager


class LinksFiltersSettings(QWidget):
    """Настройки ссылок и фильтров"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"background-color: transparent;")

        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(10)

        # Загружаем настройки
        s = SettingsManager()
        general = s.settings.get("general", {})

        self.cb_no_collapse = QCheckBox("Не сворачивать ссылки от ников")
        self.cb_no_collapse.setChecked(general.get("no_collapse_links", False))
        self.cb_no_collapse.setStyleSheet(CHECKBOX_STYLE)
        lay.addWidget(self.cb_no_collapse)

        # Ники для ссылок
        nicks_row = QHBoxLayout()
        lbl_nicks = QLabel("Ники для ссылок:")
        lbl_nicks.setFixedWidth(250)
        lbl_nicks.setStyleSheet(f"color: {self._get_color('text_primary')}; font-size: 12px;")
        nicks_row.addWidget(lbl_nicks)

        self.input_nicks = QLineEdit()
        self.input_nicks.setText(general.get("link_nicks", ""))
        self.input_nicks.setPlaceholderText("rutonybot,Moobot,NightBot,StreamElements")
        self.input_nicks.setStyleSheet(INPUT_STYLE)
        nicks_row.addWidget(self.input_nicks, stretch=1)
        lay.addLayout(nicks_row)

        self.cb_profanity = QCheckBox("Фильтр мата")
        self.cb_profanity.setChecked(general.get("profanity_filter", False))
        self.cb_profanity.setStyleSheet(CHECKBOX_STYLE)
        lay.addWidget(self.cb_profanity)

        # Список матных слов
        profanity_row = QHBoxLayout()
        lbl_profanity = QLabel("Список матных слов:")
        lbl_profanity.setFixedWidth(250)
        lbl_profanity.setStyleSheet(f"color: {self._get_color('text_primary')}; font-size: 12px;")
        profanity_row.addWidget(lbl_profanity)

        self.input_profanity = QLineEdit()
        self.input_profanity.setText(general.get("profanity_words", ""))
        self.input_profanity.setPlaceholderText("Через запятую")
        self.input_profanity.setStyleSheet(INPUT_STYLE)
        profanity_row.addWidget(self.input_profanity, stretch=1)
        lay.addLayout(profanity_row)

        # Текст замены
        replace_row = QHBoxLayout()
        lbl_replace = QLabel("Текст замены:")
        lbl_replace.setFixedWidth(250)
        lbl_replace.setStyleSheet(f"color: {self._get_color('text_primary')}; font-size: 12px;")
        replace_row.addWidget(lbl_replace)

        self.input_replace = QLineEdit()
        self.input_replace.setText(general.get("replace_text", "***"))
        self.input_replace.setStyleSheet(INPUT_STYLE)
        replace_row.addWidget(self.input_replace, stretch=1)
        lay.addLayout(replace_row)

        # Текст удаленных сообщений
        deleted_row = QHBoxLayout()
        lbl_deleted = QLabel("Текст удаленных сообщений:")
        lbl_deleted.setFixedWidth(250)
        lbl_deleted.setStyleSheet(f"color: {self._get_color('text_primary')}; font-size: 12px;")
        deleted_row.addWidget(lbl_deleted)

        self.input_deleted = QLineEdit()
        self.input_deleted.setText(general.get("deleted_text", "<сообщение удалено>"))
        self.input_deleted.setStyleSheet(INPUT_STYLE)
        deleted_row.addWidget(self.input_deleted, stretch=1)
        lay.addLayout(deleted_row)

    def _get_color(self, name: str) -> str:
        from main_screen.theme_config import COLORS
        return COLORS.get(name, "#ffffff")

    def save_data(self):
        s = SettingsManager()
        general = s.settings.get("general", {})

        general["no_collapse_links"] = self.cb_no_collapse.isChecked()
        general["link_nicks"] = self.input_nicks.text()
        general["profanity_filter"] = self.cb_profanity.isChecked()
        general["profanity_words"] = self.input_profanity.text()
        general["replace_text"] = self.input_replace.text()
        general["deleted_text"] = self.input_deleted.text()

        s.settings["general"] = general
        s.save()

        def _checkbox_style(self) -> str:
            from main_screen.checkbox_style import checkbox_style
            return checkbox_style()