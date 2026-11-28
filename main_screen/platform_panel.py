"""Панель платформ Chat_AG"""

from PyQt6.QtWidgets import QToolButton
from PyQt6.QtCore import Qt, QSize
from main_screen.assets import create_platform_icon
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from main_screen.theme_config import COLORS
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from main_screen.theme_config import COLORS
from main_screen.chat_log import _platform_icon_path


class PlatformPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyleSheet(f"""
            QWidget {{
                background-color: {COLORS['bg_main']};
                border-top: 1px solid {COLORS['border']};
            }}
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(2)

        # Счётчик подключённых платформ (вместо общего # 0)
        self.connected_label = QLabel("# 0")
        self.connected_label.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['text_secondary']};
                font-size: 11px;
                font-weight: bold;
                padding: 0 2px;
            }}
        """)
        layout.addWidget(self.connected_label)

        self.platform_buttons = {}
        self.count_labels = {}
        self.platform_containers = {}
        self.active_platforms = set()

        platforms = [
            ("twitch", "#9146ff"),
            ("youtube", "#ff0000"),
            ("vk", "#0077ff"),
            ("goodgame", "#ff6600"),
            ("kick", "#53fc18"),
            ("trovo", "#7b2cbf"),
            ("rutube", "#0055ff"),
        ]

        for platform_id, color in platforms:
            # Контейнер с зелёной рамкой для иконки + счётчика
            container = QWidget()
            container.setFixedHeight(18)
            container.setStyleSheet(f"""
                QWidget {{
                    border: 1px solid {COLORS['border']};
                    border-radius: 3px;
                    background-color: transparent;
                    padding: 0px;
                }}
            """)

            container_layout = QHBoxLayout(container)
            container_layout.setContentsMargins(1, 0, 1, 0)
            container_layout.setSpacing(1)

            # Иконка платформы (цветной квадрат с символом)
            icon_label = QLabel()
            icon_label.setPixmap(QPixmap(_platform_icon_path(platform_id, 14)))
            icon_label.setFixedSize(14, 14)
            container_layout.addWidget(icon_label)
            self.platform_buttons[platform_id] = icon_label

            # Счётчик (внутри того же контейнера)
            count = QLabel("0")
            count.setStyleSheet(f"""
                QLabel {{
                    color: {COLORS['text_primary']};
                    font-size: 11px;
                    padding: 0 2px;
                }}
            """)
            container_layout.addWidget(count)
            self.count_labels[platform_id] = count

            layout.addWidget(container)
            self.platform_containers[platform_id] = container

        layout.addStretch()

    def increment_counter(self, platform_code: str):
        platform_map = {
            "TW": "twitch", "YO": "youtube", "YT": "youtube",
            "VK": "vk", "GO": "goodgame", "GG": "goodgame",
            "KI": "kick", "KK": "kick", "TR": "trovo", "TV": "trovo",
            "RU": "rutube", "RT": "rutube",
        }
        platform_id = platform_map.get(platform_code, platform_code.lower())

        if platform_id in self.count_labels:
            label = self.count_labels[platform_id]
            current = int(label.text())
            new_value = current + 1
            label.setText(str(new_value))

    def reset_counters(self):
        for label in self.count_labels.values():
            label.setText("0")

    def set_platform_active(self, platform_code: str, active: bool):
        platform_map = {
            "TW": "twitch", "YO": "youtube", "YT": "youtube",
            "VK": "vk", "GO": "goodgame", "GG": "goodgame",
            "KI": "kick", "KK": "kick", "TR": "trovo", "TV": "trovo",
            "RU": "rutube", "RT": "rutube",
        }
        platform_id = platform_map.get(platform_code, platform_code.lower())

        if platform_id in self.platform_containers:
            container = self.platform_containers[platform_id]

            if active:
                self.active_platforms.add(platform_id)
                container.setStyleSheet(f"""
                    QWidget {{
                        border: 1px solid {COLORS['accent']};
                        border-radius: 3px;
                        background-color: {COLORS['accent']}15;
                        padding: 0px 1px;
                    }}
                """)
            else:
                self.active_platforms.discard(platform_id)
                container.setStyleSheet(f"""
                    QWidget {{
                        border: 1px solid {COLORS['border']};
                        border-radius: 3px;
                        background-color: transparent;
                        padding: 0px 1px;
                    }}
                """)

            # Обновляем счётчик подключённых платформ
            self.connected_label.setText(f"# {len(self.active_platforms)}")