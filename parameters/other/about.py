"""Панель О программе"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QComboBox, QGroupBox
from PyQt6.QtCore import Qt
from main_screen.theme_config import COLORS


class AboutPanel(QWidget):
    """Информация о программе"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: transparent;")

        lay = QVBoxLayout(self)
        lay.setContentsMargins(20, 30, 20, 20)  # увеличил верхний отступ с 15 до 30
        lay.setSpacing(15)

        # Заголовок
        title = QLabel("ℹ️ О программе")
        title.setStyleSheet(f"font-size: 22px; color: {COLORS['accent']}; font-weight: bold;")
        lay.addWidget(title)

        # Информация о программе
        info_group = QGroupBox("ИНФОРМАЦИЯ")
        info_group.setStyleSheet(self._group_style())
        info_lay = QVBoxLayout(info_group)
        info_lay.setContentsMargins(15, 20, 15, 15)
        info_lay.setSpacing(10)

        rows = [
            ("Название:", "Chat AG"),
            ("Версия:", "1.0.3"),
            ("Автор:", "Auron Gaming"),
            ("Назначение:", "Мультиплатформенный чат-клиент для стримеров"),
            ("Платформы:", "Twitch, YouTube, VK Play, Goodgame, Kick и др."),
            ("Ядро:", "Python 3.14 + PyQt6"),
        ]
        for label, value in rows:
            row = QLabel(f"<b>{label}</b> {value}")
            row.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 13px;")
            row.setAlignment(Qt.AlignmentFlag.AlignLeft)
            info_lay.addWidget(row)

        lay.addWidget(info_group)

        # Блок обновлений
        update_group = QGroupBox("ОБНОВЛЕНИЯ")
        update_group.setStyleSheet(self._group_style())
        update_lay = QVBoxLayout(update_group)
        update_lay.setContentsMargins(15, 20, 15, 15)
        update_lay.setSpacing(10)

        # Текущая версия
        version_row = QHBoxLayout()
        lbl_installed = QLabel("Установлено:")
        lbl_installed.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 12px;")
        version_row.addWidget(lbl_installed)

        lbl_version = QLabel("1.0.3 (Build 1)")
        lbl_version.setStyleSheet(f"color: {COLORS['accent']}; font-size: 12px; font-weight: bold;")
        version_row.addWidget(lbl_version)
        version_row.addStretch()
        update_lay.addLayout(version_row)

        # Канал обновлений
        channel_row = QHBoxLayout()
        lbl_channel = QLabel("Канал обновлений:")
        lbl_channel.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 12px;")
        channel_row.addWidget(lbl_channel)

        self.combo_channel = QComboBox()
        self.combo_channel.addItems(["Стабильный", "Бета", "Ночная сборка"])
        self.combo_channel.setStyleSheet(self._combo_style())
        channel_row.addWidget(self.combo_channel)
        update_lay.addLayout(channel_row)

        # Кнопки
        btn_row = QHBoxLayout()
        btn_check = QPushButton("🔄 Проверить наличие обновлений")
        btn_check.setStyleSheet(self._button_style())
        btn_check.clicked.connect(self._check_updates)
        btn_row.addWidget(btn_check)

        btn_update = QPushButton("⬇️ Обновить")
        btn_update.setStyleSheet(self._button_style())
        btn_update.clicked.connect(self._update)
        btn_row.addWidget(btn_update)

        update_lay.addLayout(btn_row)

        lay.addWidget(update_group)

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
        """

    def _button_style(self) -> str:
        return f"""
            QPushButton {{
                background-color: {COLORS['accent']};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: #238636;
            }}
        """

    def _check_updates(self):
        """Проверить обновления"""
        print("🔄 Проверка обновлений...")
        # Здесь будет реальная проверка через updater
        from core.updater import Updater
        updater = Updater()
        updater.check_for_updates()

    def _update(self):
        """Обновить"""
        print("⬇️ Запуск обновления...")
        # Здесь будет реальное обновление

    def load_data(self, config: dict):
        pass

    def save_data(self) -> dict:
        return {}