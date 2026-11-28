"""Секция Соединения — главный контейнер (3 колонки)"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QListWidget, QListWidgetItem, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor
from main_screen.theme_config import COLORS
from core.settings_manager import SettingsManager

from parameters.connections.registry import PLATFORM_CATEGORIES
from parameters.connections.icons import create_platform_icon
from parameters.connections.panel import PlatformSettingsPanel

# ============================================================================
# СТИЛЬ СКРОЛЛБАРА
# ============================================================================
SCROLL_STYLE = f"""
    QScrollBar:vertical {{
        background-color: {COLORS['bg_main']};
        width: 8px;
        border-radius: 4px;
    }}
    QScrollBar::handle:vertical {{
        background-color: {COLORS['border']};
        border-radius: 4px;
        min-height: 20px;
    }}
    QScrollBar::handle:vertical:hover {{
        background-color: {COLORS['accent']};
    }}
    QScrollBar::add-line:vertical,
    QScrollBar::sub-line:vertical {{ height: 0px; }}
"""

# ============================================================================
# СЕКЦИЯ "СОЕДИНЕНИЯ"
# ============================================================================
class ConnectionsSection(QWidget):
    """Секция настроек соединений — 3 колонки"""

    connect_requested = pyqtSignal(str, dict)
    disconnect_requested = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"background-color: {COLORS['bg_main']};")

        main_lay = QHBoxLayout(self)
        main_lay.setContentsMargins(10, 10, 10, 10)
        main_lay.setSpacing(10)

        # === СРЕДНЯЯ КОЛОНКА: Список платформ ===
        middle_widget = QWidget()
        middle_widget.setFixedWidth(280)
        middle_widget.setMinimumWidth(280)
        middle_widget.setMaximumWidth(280)
        middle_lay = QVBoxLayout(middle_widget)
        middle_lay.setContentsMargins(0, 0, 0, 0)
        middle_lay.setSpacing(0)

        middle_widget.setStyleSheet(f"""
            QWidget {{
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                background-color: {COLORS['bg_main']};
            }}
        """)

        self.platform_list = QListWidget()
        self.platform_list.setStyleSheet(f"""
            QListWidget {{
                background-color: {COLORS['bg_main']};
                color: {COLORS['text_primary']};
                border: none;
                font-size: 12px;
                padding: 5px;
            }}
            QListWidget::item {{
                padding: 6px 8px;
                border-bottom: 1px solid {COLORS['border']};
            }}
            QListWidget::item:selected {{
                background-color: {COLORS['accent']}30;
            }}
            QListWidget::item:hover {{
                background-color: {COLORS['bg_hover']};
            }}
            {SCROLL_STYLE}
        """)
        self.platform_list.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.platform_items = {}
        CATEGORY_COLOR = '#00BFFF'

        for category_name, platforms in PLATFORM_CATEGORIES.items():
            category_item = QListWidgetItem(category_name)
            category_item.setFlags(Qt.ItemFlag.NoItemFlags)
            category_item.setForeground(QColor(CATEGORY_COLOR))
            font = category_item.font()
            font.setBold(True)
            font.setPointSize(11)
            category_item.setFont(font)
            self.platform_list.addItem(category_item)

            for platform_id, info in platforms.items():
                item = QListWidgetItem()
                item.setData(Qt.ItemDataRole.UserRole, platform_id)
                item.setIcon(create_platform_icon(info['icon'], info['color'], 18))
                item.setText(f"  {info['name']}")
                item.setForeground(QColor(COLORS['text_primary']))
                self.platform_list.addItem(item)
                self.platform_items[platform_id] = {'item': item, 'info': info}

        middle_lay.addWidget(self.platform_list, stretch=1)
        main_lay.addWidget(middle_widget)

        # === ПРАВАЯ КОЛОНКА: Настройки ===
        right_widget = QWidget()
        right_lay = QVBoxLayout(right_widget)
        right_lay.setContentsMargins(0, 0, 0, 0)

        right_widget.setStyleSheet(f"""
            QWidget {{
                border: 1px solid {COLORS['border']};
                border-radius: 4px;
                background-color: {COLORS['bg_main']};
            }}
        """)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll.setStyleSheet(f"QScrollArea {{ background-color: transparent; border: none; }} {SCROLL_STYLE}")
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        panels_widget = QWidget()
        panels_lay = QVBoxLayout(panels_widget)
        panels_lay.setContentsMargins(0, 0, 0, 0)

        self.tab_widgets = {}
        for category_name, platforms in PLATFORM_CATEGORIES.items():
            for platform_id, info in platforms.items():
                panel = PlatformSettingsPanel(platform_id, info)
                panel.connect_requested.connect(self.connect_requested.emit)
                panel.disconnect_requested.connect(self.disconnect_requested.emit)
                panel.setVisible(False)
                panels_lay.addWidget(panel)
                self.tab_widgets[platform_id] = panel

        self.empty_label = QLabel("Выберите платформу слева")
        self.empty_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 13px;")
        self.empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_label.setMinimumHeight(200)
        panels_lay.addWidget(self.empty_label)
        panels_lay.addStretch()

        scroll.setWidget(panels_widget)
        right_lay.addWidget(scroll)
        main_lay.addWidget(right_widget, stretch=1)

        self._load_all_data()

        if self.platform_items:
            first_id = list(self.platform_items.keys())[0]
            self._select_platform(first_id)
            self.platform_list.setCurrentItem(self.platform_items[first_id]['item'])

        self.platform_list.currentItemChanged.connect(self._on_item_changed)

    def _on_item_changed(self, current, previous):
        if current:
            platform_id = current.data(Qt.ItemDataRole.UserRole)
            if platform_id:
                self._select_platform(platform_id)

    def _select_platform(self, platform_id: str):
        self.empty_label.setVisible(False)
        for pid, panel in self.tab_widgets.items():
            panel.setVisible(False)
        if platform_id in self.tab_widgets:
            self.tab_widgets[platform_id].setVisible(True)

    def _load_all_data(self):
        s = SettingsManager()
        connections = s.settings.get("connections", {})
        for platform_id, panel in self.tab_widgets.items():
            config = connections.get(platform_id, {})
            panel.load_data(config)

    def save_data(self):
        for panel in self.tab_widgets.values():
            panel.save_data()