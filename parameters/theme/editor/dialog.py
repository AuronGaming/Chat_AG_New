"""Редактор темы POE — тёмный стиль программы"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QSlider, QCheckBox, QGroupBox, QWidget, QScrollArea, QLineEdit
)
from PyQt6.QtCore import Qt, pyqtSignal
from main_screen.theme_config import COLORS
import os, json

THEMES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'themes'))
FONTS = ["Fontin", "Cuprum", "Segoe UI", "Arial", "Roboto", "Georgia"]
APPEAR = ["none", "fadeIn", "slideInRight", "slideInLeft", "bounce"]
HIDE = ["none", "fadeOut", "slideOutRight", "zoomOut"]

_bg = COLORS.get('bg_primary', '#010409')
_bg2 = COLORS.get('bg_secondary', '#0D1117')
_bg3 = COLORS.get('bg_input', '#161B22')
_tx = COLORS.get('text_primary', '#C9D1D9')
_bd = COLORS.get('border', '#30363D')
_ac = COLORS.get('accent', '#00BFFF')

DARK = (
    "QDialog { background-color: %s; color: %s; }" % (_bg2, _tx) +
    "QLabel { color: %s; font-size: 13px; background: transparent; }" % _tx +
    "QGroupBox { color: %s; font-weight: bold; border: 1px solid %s; border-radius: 5px; margin-top: 12px; padding-top: 14px; background: %s; }" % (_ac, _bd, _bg) +
    "QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 4px; }" +
    "QComboBox, QLineEdit { background: %s; color: %s; border: 1px solid %s; border-radius: 4px; padding: 5px 8px; font-size: 12px; }" % (_bg3, _tx, _bd) +
    "QComboBox QAbstractItemView { background: %s; color: %s; selection-background-color: %s; }" % (_bg3, _tx, _ac) +
    "QPushButton { background: %s; color: %s; border: 1px solid %s; border-radius: 4px; padding: 7px 16px; font-size: 12px; }" % (_bg3, _tx, _bd) +
    "QPushButton:hover { border-color: %s; }" % _ac +
    "QCheckBox { color: %s; font-size: 12px; background: transparent; }" % _tx +
    "QSlider::groove:horizontal { background: %s; height: 4px; border-radius: 2px; }" % _bd +
    "QSlider::handle:horizontal { background: %s; width: 14px; margin: -5px 0; border-radius: 7px; }" % _ac +
    "QScrollArea { border: none; background: transparent; }"
)


class ThemeEditorDialog(QDialog):
    settings_saved = pyqtSignal(dict)

    def __init__(self, theme_name, parent=None):
        super().__init__(parent)
        self.theme_name = theme_name
        self.setWindowTitle("Редактор темы: " + str(theme_name))
        self.setMinimumSize(560, 520)
        self.setStyleSheet(DARK)
        self._load()
        self._build()

    def _path(self):
        return os.path.join(THEMES_DIR, self.theme_name, 'settings.json')

    def _load(self):
        d = {"nickname_font": "Fontin", "text_font": "Fontin", "nickname_color": "#C4A000",
             "text_color": "#D4C5A0", "appear_effect": "fadeIn", "hide_effect": "fadeOut",
             "show_time": 12, "nickname_shadow": True}
        if os.path.isfile(self._path()):
            try:
                with open(self._path(), encoding='utf-8') as f:
                    d.update(json.load(f))
            except Exception:
                pass
        self.cfg = d

    def _build(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(16, 16, 16, 12)
        lay.setSpacing(12)
        t = QLabel("⚙️ Редактор темы: " + str(self.theme_name))
        t.setStyleSheet("color:" + _ac + "; font-size:17px; font-weight:bold; background:transparent;")
        lay.addWidget(t)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        w = QWidget()
        wl = QVBoxLayout(w)
        wl.setSpacing(12)

        g1 = QGroupBox("ШРИФТЫ")
        l1 = QVBoxLayout(g1)
        for lbl, key in [("Шрифт ника:", "nickname_font"), ("Шрифт текста:", "text_font")]:
            r = QHBoxLayout()
            r.addWidget(QLabel(lbl))
            c = QComboBox()
            c.addItems(FONTS)
            c.setCurrentText(self.cfg[key])
            setattr(self, "combo_" + key, c)
            r.addWidget(c)
            l1.addLayout(r)
        wl.addWidget(g1)

        g2 = QGroupBox("ЦВЕТА")
        l2 = QVBoxLayout(g2)
        for lbl, key in [("Цвет ника:", "nickname_color"), ("Цвет текста:", "text_color")]:
            r = QHBoxLayout()
            r.addWidget(QLabel(lbl))
            e = QLineEdit(self.cfg[key])
            setattr(self, "line_" + key, e)
            r.addWidget(e)
            l2.addLayout(r)
        wl.addWidget(g2)

        g3 = QGroupBox("ЭФФЕКТЫ")
        l3 = QVBoxLayout(g3)
        for lbl, key, items in [("Появление:", "appear_effect", APPEAR), ("Скрытие:", "hide_effect", HIDE)]:
            r = QHBoxLayout()
            r.addWidget(QLabel(lbl))
            c = QComboBox()
            c.addItems(items)
            c.setCurrentText(self.cfg[key])
            setattr(self, "combo_" + key, c)
            r.addWidget(c)
            l3.addLayout(r)
        wl.addWidget(g3)

        g4 = QGroupBox("ВРЕМЯ ПОКАЗА (сек)")
        l4 = QHBoxLayout(g4)
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(3, 30)
        self.slider.setValue(self.cfg["show_time"])
        self.lbl_time = QLabel(str(self.cfg["show_time"]))
        self.slider.valueChanged.connect(lambda v: self.lbl_time.setText(str(v)))
        l4.addWidget(self.slider)
        l4.addWidget(self.lbl_time)
        wl.addWidget(g4)

        self.chk = QCheckBox("Тень для ника")
        self.chk.setChecked(self.cfg["nickname_shadow"])
        wl.addWidget(self.chk)
        wl.addStretch()
        scroll.setWidget(w)
        lay.addWidget(scroll)

        br = QHBoxLayout()
        br.addStretch()
        bc = QPushButton("Отмена")
        bc.clicked.connect(self.reject)
        br.addWidget(bc)
        bo = QPushButton("ОК")
        bo.setStyleSheet("background:" + _ac + "; color:white; border:none; padding:8px 22px; border-radius:4px; font-weight:bold;")
        bo.clicked.connect(self._save)
        br.addWidget(bo)
        lay.addLayout(br)

    def _collect(self):
        return {
            "nickname_font": self.combo_nickname_font.currentText(),
            "text_font": self.combo_text_font.currentText(),
            "nickname_color": self.line_nickname_color.text(),
            "text_color": self.line_text_color.text(),
            "appear_effect": self.combo_appear_effect.currentText(),
            "hide_effect": self.combo_hide_effect.currentText(),
            "show_time": self.slider.value(),
            "nickname_shadow": self.chk.isChecked(),
        }

    def _save(self):
        os.makedirs(os.path.dirname(self._path()), exist_ok=True)
        with open(self._path(), 'w', encoding='utf-8') as f:
            json.dump(self._collect(), f, indent=2, ensure_ascii=False)
        self.settings_saved.emit(self._collect())
        self.accept()
