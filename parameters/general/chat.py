"""Настройки чата"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QLineEdit, QHBoxLayout, QLabel
from parameters.general.visual import CHECKBOX_STYLE, INPUT_STYLE
from core.settings_manager import SettingsManager


class ChatSettings(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: transparent;")

        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(10)

        s = SettingsManager()
        general = s.settings.get("general", {})

        self.cb_system_messages = QCheckBox("Показывать системные сообщения")
        self.cb_system_messages.setChecked(general.get("system_messages", True))
        self.cb_system_messages.setStyleSheet(CHECKBOX_STYLE)
        self.cb_system_messages.setToolTip("Системные уведомления будут отображаться в самом чате")
        lay.addWidget(self.cb_system_messages)

        self.cb_send_panel = QCheckBox("Показывать панель отправки сообщений")
        self.cb_send_panel.setChecked(general.get("send_panel", True))
        self.cb_send_panel.setStyleSheet(CHECKBOX_STYLE)
        lay.addWidget(self.cb_send_panel)

        self.cb_avatars = QCheckBox("Аватары")
        self.cb_avatars.setChecked(general.get("avatars", False))
        self.cb_avatars.setStyleSheet(CHECKBOX_STYLE)
        lay.addWidget(self.cb_avatars)

        keywords_row = QHBoxLayout()
        lbl_keywords = QLabel("Подсветка сообщений с ключевыми словами:")
        lbl_keywords.setStyleSheet("color: #c9d1d9; font-size: 12px;")
        keywords_row.addWidget(lbl_keywords)

        self.input_keywords = QLineEdit()
        self.input_keywords.setText(general.get("keywords", ""))
        self.input_keywords.setPlaceholderText("Через запятую")
        self.input_keywords.setStyleSheet(INPUT_STYLE)
        keywords_row.addWidget(self.input_keywords, stretch=1)
        lay.addLayout(keywords_row)

    def save_data(self):
        s = SettingsManager()
        general = s.settings.get("general", {})
        general["system_messages"] = self.cb_system_messages.isChecked()
        general["send_panel"] = self.cb_send_panel.isChecked()
        general["avatars"] = self.cb_avatars.isChecked()
        general["keywords"] = self.input_keywords.text()
        s.settings["general"] = general
        s.save()