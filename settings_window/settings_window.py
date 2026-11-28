"""Окно настроек Chat_AG — трёхколоночная структура"""

from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem, QWidget,
    QPushButton, QScrollArea, QApplication, QLabel
)
from PyQt6.QtCore import Qt, pyqtSignal
from main_screen.theme_config import COLORS, BUTTON_DEFAULT, BUTTON_ACCENT
from main_screen.custom_title_bar import CustomTitleBar


class SettingsWindow(QMainWindow):
    settings_applied = pyqtSignal()

    SECTIONS = {
        "general": {
            "name": "Общие", "icon": "⚙️", "count": 24,
            "subsections": [
                {"name": "Чат", "icon": "💬"},
                {"name": "Статистика", "icon": "📊"},
                {"name": "Ссылки и фильтры", "icon": "🔗"},
                {"name": "Поведение окна", "icon": "🪟"},
            ]
        },
        "connections": {
            "name": "Соединения", "icon": "🔌", "count": 33,
            "subsections": [
                {"name": "Twitch", "icon": "🟣"},
                {"name": "YouTube", "icon": "🔴"},
                {"name": "VK Play", "icon": "🔵"},
                {"name": "Goodgame", "icon": "🟠"},
                {"name": "Kick", "icon": "🟢"},
                {"name": "Rutube", "icon": "🔵"},
                {"name": "TikTok", "icon": "⚫"},
                {"name": "Telegram", "icon": "🔷"},
                {"name": "Как подключить", "icon": "📖"},
            ]
        },
        "sound": {
            "name": "Звук", "icon": "🔊", "count": 32,
            "subsections": [
                {"name": "Озвучка", "icon": "🗣️"},
                {"name": "Донат", "icon": "💰"},
                {"name": "Подписка", "icon": "⭐"},
                {"name": "Сообщение", "icon": "💬"},
            ]
        },
        "theme": {
            "name": "Тема оформления", "icon": "🎨", "count": 73,
            "subsections": [
                {"name": "Каталог тем", "icon": "🖼️"},
                {"name": "OBS оверлей", "icon": "📺"},
                {"name": "Как подключить", "icon": "📖"},
            ]
        },
        "hotkeys": {
            "name": "Hotkeys", "icon": "⌨️", "count": 6,
            "subsections": [
                {"name": "Основные", "icon": "🔑"},
                {"name": "Быстрые действия", "icon": "⚡"},
            ]
        },
        "other": {
            "name": "Прочее", "icon": "📦", "count": 2,
            "subsections": [
                {"name": "Активация", "icon": "🔑"},
                {"name": "Вид лицевого окна", "icon": "👁️"},
                {"name": "О программе", "icon": "ℹ️"},
            ]
        }
    }

    # Карта: (раздел, подпункт) -> модуль с виджетом
    MODULE_MAP = {
        ("general", "Чат"): "parameters.general.chat",
        ("general", "Статистика"): "parameters.general.statistics",
        ("general", "Ссылки и фильтры"): "parameters.general.links_filters",
        ("general", "Поведение окна"): "parameters.general.window_behavior",
        ("theme", "Каталог тем"): "parameters.theme.themes",
        ("theme", "OBS оверлей"): "parameters.theme.obs_overlay",
        ("hotkeys", "Основные"): "parameters.hotkeys.bindings",
        ("hotkeys", "Быстрые действия"): "parameters.hotkeys.quick_actions",
        ("other", "Активация"): "parameters.other.activation",
        ("other", "Вид лицевого окна"): "parameters.other.window_view",
        ("other", "О программе"): "parameters.other.about",
        ("help", "Как подключить"): "settings_window.help_section",


    }


    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.CustomizeWindowHint)
        self.setWindowTitle("Chat_AG - Настройки")
        self.setMinimumSize(1300, 700)
        self.resize(1300, 700)
        self._drag_pos = None

        central = QWidget()
        central.setStyleSheet(f"background-color: {COLORS['bg_main']};")
        self.setCentralWidget(central)

        main_lay = QVBoxLayout(central)
        main_lay.setContentsMargins(0, 0, 0, 0)
        main_lay.setSpacing(0)

        self.title_bar = CustomTitleBar("Chat_AG - Настройки", self, show_extra_buttons=False)
        main_lay.addWidget(self.title_bar)

        content = QWidget()
        content.setStyleSheet(f"background-color: {COLORS['bg_main']};")
        content_lay = QHBoxLayout(content)
        content_lay.setContentsMargins(10, 10, 10, 10)
        content_lay.setSpacing(10)

        # ЛЕВАЯ: секции
        left_widget = QWidget()
        left_widget.setFixedWidth(200)
        left_lay = QVBoxLayout(left_widget)
        left_lay.setContentsMargins(0, 0, 0, 0)
        left_lay.setSpacing(0)
        left_widget.setStyleSheet(f"""
            QWidget {{
                background-color: {COLORS['bg_main']};
                border: 1px solid {COLORS['accent']};
                border-radius: 4px;
            }}
        """)

        self.sections_list = QListWidget()
        self.sections_list.setStyleSheet(self._list_style())
        for info in self.SECTIONS.values():
            self.sections_list.addItem(QListWidgetItem(f"{info['icon']} {info['name']} ({info['count']})"))
        left_lay.addWidget(self.sections_list)
        content_lay.addWidget(left_widget)

        # СРЕДНЯЯ: подпункты
        middle_widget = QWidget()
        middle_widget.setFixedWidth(200)
        middle_lay = QVBoxLayout(middle_widget)
        middle_lay.setContentsMargins(0, 0, 0, 0)
        middle_lay.setSpacing(0)
        middle_widget.setStyleSheet(f"""
            QWidget {{
                background-color: {COLORS['bg_main']};
                border: 1px solid {COLORS['accent']};
                border-radius: 4px;
            }}
        """)

        self.subsections_list = QListWidget()
        self.subsections_list.setStyleSheet(self._list_style())
        middle_lay.addWidget(self.subsections_list)
        content_lay.addWidget(middle_widget)

        # ПРАВАЯ: контент
        right_widget = QWidget()
        right_lay = QVBoxLayout(right_widget)
        right_lay.setContentsMargins(0, 0, 0, 0)
        right_lay.setSpacing(0)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)
        self.scroll_area.setStyleSheet(f"""
            QScrollArea {{
                background-color: {COLORS['bg_main']};
                border: 1px solid {COLORS['accent']};
                border-radius: 4px;
            }}
            QScrollBar:vertical {{
                background-color: {COLORS['bg_main']};
                width: 10px;
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {COLORS['accent']};
                border-radius: 5px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: #238636;
            }}
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)
        right_lay.addWidget(self.scroll_area)
        content_lay.addWidget(right_widget, stretch=1)

        main_lay.addWidget(content, stretch=1)

        # Кнопки
        btns_widget = QWidget()
        btns_widget.setStyleSheet(f"background-color: {COLORS['bg_main']};")
        buttons_lay = QHBoxLayout(btns_widget)
        buttons_lay.setContentsMargins(10, 10, 10, 10)
        buttons_lay.addStretch()

        btn_cancel = QPushButton("Отмена")
        btn_cancel.setStyleSheet(BUTTON_DEFAULT)
        btn_cancel.setFixedHeight(32)
        btn_cancel.clicked.connect(self.close)
        buttons_lay.addWidget(btn_cancel)

        btn_apply = QPushButton("Применить")
        btn_apply.setStyleSheet(BUTTON_ACCENT)
        btn_apply.setFixedHeight(32)
        btn_apply.clicked.connect(self._apply_settings)
        buttons_lay.addWidget(btn_apply)

        btn_ok = QPushButton("ОК")
        btn_ok.setStyleSheet(BUTTON_ACCENT)
        btn_ok.setFixedHeight(32)
        btn_ok.clicked.connect(self._save_and_close)
        buttons_lay.addWidget(btn_ok)

        main_lay.addWidget(btns_widget)

        # Состояние
        self.current_section_id = None
        self.current_subsection = None
        self.current_section_widget = None

        self.sections_list.currentRowChanged.connect(self._on_section_changed)
        self.subsections_list.currentRowChanged.connect(self._on_subsection_changed)
        self.sections_list.setCurrentRow(0)

        screen = QApplication.primaryScreen()
        if screen:
            g = screen.geometry()
            self.move(max(0, (g.width() - self.width()) // 2),
                      max(0, (g.height() - self.height()) // 2))

    def _list_style(self) -> str:
        return f"""
            QListWidget {{
                background-color: {COLORS['bg_main']};
                color: {COLORS['text_primary']};
                border: none;
                font-size: 12px;
                padding: 5px;
            }}
            QListWidget::item {{
                padding: 10px 12px;
                border: 1px solid {COLORS['accent']};
                border-radius: 4px;
                margin: 2px 0;
            }}
            QListWidget::item:selected {{
                background-color: {COLORS['accent']};
                color: white;
                font-weight: bold;
            }}
            QListWidget::item:hover {{
                background-color: {COLORS['bg_hover']};
            }}
            QScrollBar:vertical {{
                background-color: {COLORS['bg_main']};
                width: 10px;
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {COLORS['accent']};
                border-radius: 5px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: #238636;
            }}
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """

    def _on_section_changed(self, row):
        if row < 0:
            return
        section_ids = list(self.SECTIONS.keys())
        if row >= len(section_ids):
            return
        section_id = section_ids[row]
        self.current_section_id = section_id
        self.subsections_list.clear()
        for sub in self.SECTIONS[section_id]["subsections"]:
            self.subsections_list.addItem(QListWidgetItem(f"{sub['icon']} {sub['name']}"))
        if self.SECTIONS[section_id]["subsections"]:
            self.subsections_list.setCurrentRow(0)

    def _on_subsection_changed(self, row):
        if row < 0 or not self.current_section_id:
            return
        subsections = self.SECTIONS[self.current_section_id]["subsections"]
        if row >= len(subsections):
            return
        self.current_subsection = subsections[row]["name"]
        self._load_subsection_widget(self.current_section_id, self.current_subsection)

    def _find_widget_class(self, module):
        """Найти ГЛАВНЫЙ класс-виджет модуля (не вспомогательный)"""
        from PyQt6.QtWidgets import QWidget as QW
        candidates = []
        for name in dir(module):
            obj = getattr(module, name)
            if (isinstance(obj, type) and issubclass(obj, QW)
                    and obj.__module__ == module.__name__ and obj is not QW):
                candidates.append((name, obj))
        if not candidates:
            return None
        for name, obj in candidates:
            if name.endswith(("Settings", "Section", "Panel", "Gallery")):
                return obj
        return candidates[0][1]

    def _load_subsection_widget(self, section_id, subsection):
        # Удаляем старый виджет
        if self.current_section_widget:
            old = self.scroll_area.widget()
            if old:
                old.setParent(None)
                old.deleteLater()
            self.current_section_widget = None

        try:
            # === Инструкция ===
            if subsection == "Как подключить":
                from settings_window.help_section import HelpSection, THEME_HELP, CONNECTIONS_HELP
                if section_id == "theme":
                    self.current_section_widget = HelpSection("Как подключить тему", "📖", THEME_HELP)
                else:
                    self.current_section_widget = HelpSection("Как подключить платформу", "🔌", CONNECTIONS_HELP)

            # === Соединения: одна платформа ===
            elif section_id == "connections":
                from parameters.connections.registry import PLATFORM_REGISTRY
                from parameters.connections.panel import PlatformSettingsPanel
                from core.settings_manager import SettingsManager

                platform_map = {
                    "Twitch": "twitch", "YouTube": "youtube", "VK Play": "vk_play",
                    "Goodgame": "goodgame", "Kick": "kick", "Rutube": "rutube",
                    "TikTok": "tiktok", "Telegram": "telegram",
                }
                platform_id = platform_map.get(subsection, subsection.lower())
                info = PLATFORM_REGISTRY.get(
                    platform_id,
                    {"name": subsection, "color": "#888888", "icon": "?",
                     "connect_url": "", "token_url": ""}
                )
                panel = PlatformSettingsPanel(platform_id, info)
                panel.connect_requested.connect(self._on_connect_platform)
                panel.disconnect_requested.connect(self._on_disconnect_platform)
                s = SettingsManager()
                panel.load_data(s.settings.get("connections", {}).get(platform_id, {}))
                self.current_section_widget = panel

            # === Звук ===
            elif section_id == "sound":
                if subsection == "Озвучка":
                    from parameters.sound.voice import VoiceSettings
                    self.current_section_widget = VoiceSettings()
                else:
                    from parameters.sound.events import EventSettings
                    cfg = {
                        "Донат": {"name": "Донат", "icon": "💰"},
                        "Подписка": {"name": "Подписка", "icon": "⭐"},
                        "Сообщение": {"name": "Сообщение", "icon": "💬"},
                    }
                    self.current_section_widget = EventSettings(
                        subsection.lower(), cfg.get(subsection, {"name": subsection, "icon": "🔔"})
                    )

            # === Прочее ===
            elif section_id == "other":
                from parameters.other.section import OtherSection
                self.current_section_widget = OtherSection(subsection)
                self.current_section_widget.activation_requested.connect(self._on_activation)
                self.current_section_widget.transparency_changed.connect(self._on_transparency_changed)
                self.current_section_widget.click_through_changed.connect(self._on_click_through_changed)

            # === Общие / Тема / Hotkeys через MODULE_MAP ===
            elif (section_id, subsection) in self.MODULE_MAP:
                import importlib
                module = importlib.import_module(self.MODULE_MAP[(section_id, subsection)])
                cls = self._find_widget_class(module)
                if cls:
                    self.current_section_widget = cls()
                else:
                    self.current_section_widget = QLabel(f"Нет виджета для '{subsection}'")
                    self.current_section_widget.setStyleSheet(
                        f"color: {COLORS['text_secondary']}; font-size: 13px; padding: 20px;")

            else:
                self.current_section_widget = QLabel(f"Раздел '{subsection}' в разработке")
                self.current_section_widget.setStyleSheet(
                    f"color: {COLORS['text_secondary']}; font-size: 13px; padding: 20px;")

        except Exception as e:
            print(f"⚠️ Ошибка загрузки {section_id}/{subsection}: {e}")
            self.current_section_widget = QLabel(f"Ошибка: {e}")
            self.current_section_widget.setStyleSheet("color: red; font-size: 13px; padding: 20px;")

        if self.current_section_widget:
            container = QWidget()
            container.setStyleSheet("background-color: transparent;")
            cl = QVBoxLayout(container)
            cl.setContentsMargins(0, 0, 0, 0)
            cl.setSpacing(0)
            cl.addWidget(self.current_section_widget)
            if not getattr(self.current_section_widget, "stretch_full", False):
                cl.addStretch(1)
            self.scroll_area.setWidget(container)

    def _on_connect_platform(self, platform, config):
        if self.main_window and hasattr(self.main_window, '_start_platform'):
            self.main_window._start_platform(platform, config)

    def _on_disconnect_platform(self, platform):
        if self.main_window and hasattr(self.main_window, '_stop_platform'):
            self.main_window._stop_platform(platform)

    def _on_activation(self, nick, key):
        print(f"🔑 Активация: {nick}, ключ: {key[:4]}...")

    def _on_transparency_changed(self, value):
        if self.main_window:
            self.main_window.setWindowOpacity(1.0 - (value / 100.0))

    def _on_click_through_changed(self, enabled):
        if self.main_window:
            self.main_window.setAttribute(
                Qt.WidgetAttribute.WA_TransparentForMouseEvents, enabled
            )

    def _apply_settings(self):
        if hasattr(self.current_section_widget, 'save_data'):
            try:
                self.current_section_widget.save_data()
                self.settings_applied.emit()
            except Exception as e:
                print(f"⚠️ Ошибка применения: {e}")

    def _save_and_close(self):
        self._apply_settings()
        self.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and event.pos().y() < 40:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
            return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self._drag_pos:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self._drag_pos = None
        super().mouseReleaseEvent(event)

    def closeEvent(self, event):
        event.accept()