"""OBS оверлей — настройки вывода темы в OBS"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox,
    QCheckBox, QLineEdit, QPushButton, QComboBox, QSlider, QSpinBox, QApplication
)
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QDesktopServices
from main_screen.theme_config import COLORS
from core.settings_manager import SettingsManager

GROUP_STYLE = f"""
    QGroupBox {{
        background-color: {COLORS['bg_main']};
        border: 1px solid {COLORS['border']};
        border-radius: 4px;
        margin-top: 12px;
        padding-top: 14px;
        font-size: 13px;
        font-weight: bold;
        color: {COLORS['accent']};
    }}
    QGroupBox::title {{ subcontrol-origin: margin; left: 10px; padding: 0 4px; }}
"""
INPUT_STYLE = f"""
    QLineEdit {{
        background-color: {COLORS['bg_input']};
        color: {COLORS['text_primary']};
        border: 1px solid {COLORS['border']};
        border-radius: 4px;
        padding: 6px 10px;
        font-size: 12px;
    }}
"""
COMBO_STYLE = f"""
    QComboBox {{
        background-color: {COLORS['bg_input']};
        color: {COLORS['text_primary']};
        border: 1px solid {COLORS['border']};
        border-radius: 4px;
        padding: 4px 8px;
        min-height: 24px;
        max-height: 28px;
    }}
    QComboBox QAbstractItemView {{
        background-color: {COLORS['bg_input']};
        color: {COLORS['text_primary']};
        border: 1px solid {COLORS['border']};
        selection-background-color: {COLORS['accent']};
    }}
"""
BTN_STYLE = f"""
    QPushButton {{
        background-color: {COLORS['bg_input']};
        color: {COLORS['text_primary']};
        border: 1px solid {COLORS['border']};
        border-radius: 4px;
        padding: 6px 12px;
        font-size: 12px;
    }}
    QPushButton:hover {{
        background-color: {COLORS['bg_hover']};
        border-color: {COLORS['accent']};
    }}
"""
CHECK_STYLE = f"""
    QCheckBox {{ color: {COLORS['text_primary']}; font-size: 13px; spacing: 8px; }}
"""


class OBSOverlaySettings(QWidget):
    """Настройки OBS оверлея — тема берётся из каталога тем"""

    def showEvent(self, event):
        """При открытии панели перечитываем тему с диска"""
        super().showEvent(event)
        s = SettingsManager()
        cfg = s.settings.get("obs_overlay", {})
        self.spin_port.setValue(cfg.get("port", 8383))
        self._update_url()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: transparent;")
        self._build_ui()
        self.load_data()

    def _current_theme(self) -> str:
        """Тема, которую выбрал игрок в каталоге тем"""
        s = SettingsManager()
        return (s.settings.get("obs_overlay", {}).get("theme")
                or s.settings.get("theme", {}).get("current")
                or "default")

    def _build_ui(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(20, 15, 20, 15)
        lay.setSpacing(10)

        title = QLabel("OBS оверлей")
        title.setStyleSheet(f"font-size: 20px; color: {COLORS['accent']}; font-weight: bold;")
        lay.addWidget(title)

        # === ОБЩИЕ ===
        g_common = QGroupBox("ОБЩИЕ")
        g_common.setStyleSheet(GROUP_STYLE)
        gc = QVBoxLayout(g_common)
        gc.setSpacing(8)
        self.cb_enabled = QCheckBox("Включить OBS оверлей")
        self.cb_enabled.setStyleSheet(CHECK_STYLE)
        gc.addWidget(self.cb_enabled)
        self.cb_server = QCheckBox("Запускать локальный сервер тем при старте")
        self.cb_server.setStyleSheet(CHECK_STYLE)
        gc.addWidget(self.cb_server)
        lay.addWidget(g_common)

        # === ССЫЛКА ОВЕРЛЕЯ ===
        g_url = QGroupBox("ССЫЛКА ОВЕРЛЕЯ")
        g_url.setStyleSheet(GROUP_STYLE)
        gu = QVBoxLayout(g_url)
        gu.setSpacing(8)
        url_row = QHBoxLayout()
        self.line_url = QLineEdit()
        self.line_url.setReadOnly(True)
        self.line_url.setStyleSheet(INPUT_STYLE)
        url_row.addWidget(self.line_url, stretch=1)
        btn_copy = QPushButton("📋 Копировать")
        btn_copy.setStyleSheet(BTN_STYLE)
        btn_copy.clicked.connect(self._copy_url)
        url_row.addWidget(btn_copy)
        btn_open = QPushButton("🌐 Открыть в браузере")
        btn_open.setStyleSheet(BTN_STYLE)
        btn_open.clicked.connect(self._open_url)
        url_row.addWidget(btn_open)
        gu.addLayout(url_row)
        hint = QLabel("💡 Добавьте эту ссылку в OBS как источник «Браузер» (Browser Source).")
        hint.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 10px; font-style: italic;")
        gu.addWidget(hint)
        lay.addWidget(g_url)

        # === ТЕМА ОВЕРЛЕЯ (берётся из каталога) ===
        g_theme = QGroupBox("ТЕМА ОВЕРЛЕЯ")
        g_theme.setStyleSheet(GROUP_STYLE)
        gt = QVBoxLayout(g_theme)
        gt.setSpacing(8)
        row_t = QHBoxLayout()
        lbl_t = QLabel("Текущая тема:")
        lbl_t.setFixedWidth(140)
        lbl_t.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 12px;")
        row_t.addWidget(lbl_t)
        self.lbl_theme_name = QLabel("default")
        self.lbl_theme_name.setStyleSheet(
            f"color: {COLORS['accent']}; font-size: 14px; font-weight: bold;")
        row_t.addWidget(self.lbl_theme_name)
        row_t.addStretch()
        gt.addLayout(row_t)
        hint2 = QLabel("💡 Тема выбирается в разделе «Каталог тем» и подставляется сюда автоматически.")
        hint2.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 10px; font-style: italic;")
        gt.addWidget(hint2)

        row_p = QHBoxLayout()
        lbl_p = QLabel("Порт сервера:")
        lbl_p.setFixedWidth(140)
        lbl_p.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 12px;")
        row_p.addWidget(lbl_p)
        self.spin_port = QSpinBox()
        self.spin_port.setRange(1024, 65535)
        self.spin_port.setValue(8383)
        self.spin_port.setFixedWidth(120)
        self.spin_port.setStyleSheet(INPUT_STYLE)
        self.spin_port.valueChanged.connect(self._update_url)
        row_p.addWidget(self.spin_port)
        row_p.addStretch()
        gt.addLayout(row_p)
        lay.addWidget(g_theme)

        # === ВИДЖЕТ ЧАТА ===
        g_widget = QGroupBox("ВИДЖЕТ ЧАТА")
        g_widget.setStyleSheet(GROUP_STYLE)
        gw = QVBoxLayout(g_widget)
        gw.setSpacing(8)
        self.cb_no_header = QCheckBox("Отключить шапку в виджете")
        self.cb_no_header.setStyleSheet(CHECK_STYLE)
        gw.addWidget(self.cb_no_header)

        row_m = QHBoxLayout()
        lbl_m = QLabel("Режим отображения:")
        lbl_m.setFixedWidth(140)
        lbl_m.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 12px;")
        row_m.addWidget(lbl_m)
        self.combo_mode = QComboBox()
        self.combo_mode.addItems(["Игровой режим", "Поверх всех окон", "Обычный"])
        self.combo_mode.setStyleSheet(COMBO_STYLE)
        self.combo_mode.setFixedHeight(28)
        row_m.addWidget(self.combo_mode, stretch=1)
        gw.addLayout(row_m)

        row_s = QHBoxLayout()
        lbl_s = QLabel("Размер:")
        lbl_s.setFixedWidth(140)
        lbl_s.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 12px;")
        row_s.addWidget(lbl_s)
        self.slider_size = QSlider(Qt.Orientation.Horizontal)
        self.slider_size.setRange(50, 150)
        self.slider_size.setValue(100)
        self.slider_size.valueChanged.connect(self._on_size_changed)
        row_s.addWidget(self.slider_size, stretch=1)
        self.lbl_size = QLabel("100%")
        self.lbl_size.setFixedWidth(50)
        self.lbl_size.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 12px;")
        row_s.addWidget(self.lbl_size)
        gw.addLayout(row_s)
        lay.addWidget(g_widget)

        lay.addStretch()

    def _update_url(self, *_):
        theme = self._current_theme()
        self.lbl_theme_name.setText(theme)
        self.line_url.setText(f"http://localhost:{self.spin_port.value()}/themes/{theme}/")

    def _on_size_changed(self, value):
        self.lbl_size.setText(f"{value}%")

    def _copy_url(self):
        QApplication.clipboard().setText(self.line_url.text())
        print("📋 URL оверлея скопирован")

    def _open_url(self):
        QDesktopServices.openUrl(QUrl(self.line_url.text()))

    def load_data(self):
        s = SettingsManager()
        cfg = s.settings.get("obs_overlay", {})
        self.cb_enabled.setChecked(cfg.get("enabled", False))
        self.cb_server.setChecked(cfg.get("autostart_server", False))
        self.cb_no_header.setChecked(cfg.get("no_header", False))
        self.spin_port.setValue(cfg.get("port", 8383))
        self.slider_size.setValue(cfg.get("size", 100))
        mode = cfg.get("mode", "Игровой режим")
        idx = self.combo_mode.findText(mode)
        self.combo_mode.setCurrentIndex(idx if idx >= 0 else 0)
        self._update_url()

    def save_data(self):
        s = SettingsManager()
        s.settings["obs_overlay"] = {
            "enabled": self.cb_enabled.isChecked(),
            "autostart_server": self.cb_server.isChecked(),
            "no_header": self.cb_no_header.isChecked(),
            "port": self.spin_port.value(),
            "size": self.slider_size.value(),
            "mode": self.combo_mode.currentText(),
        }
        s.save()
        try:
            from core.overlay_server import start_server, stop_server
            if self.cb_enabled.isChecked() or self.cb_server.isChecked():
                start_server(self.spin_port.value())
            else:
                stop_server()
        except Exception as e:
            print(f"⚠️ Сервер: {e}")
        print("💾 OBS оверлей сохранён")