"""Модальное окно редактора темы — 3 колонки как в RutonyChat"""
import os
import json
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QSlider, QCheckBox, QGroupBox, QWidget, QScrollArea,
    QGridLayout, QLineEdit, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QPainter, QColor, QFont
from main_screen.theme_config import COLORS
from core.settings_manager import SettingsManager

THEMES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'themes'))

FONTS = ["Cuprum", "Segoe UI", "Arial", "Roboto", "Georgia", "Verdana"]
APPEAR_EFFECTS = ["none", "fadeIn", "slideInRight", "slideInLeft", "bounce"]
HIDE_EFFECTS = ["none", "fadeOut", "slideOutRight", "zoomOut"]


class ThemeEditorDialog(QDialog):
    """Редактор темы с 3 колонками"""
    settings_saved = pyqtSignal(dict)

    def __init__(self, theme_name: str, parent=None):
        super().__init__(parent)
        self.theme_name = theme_name
        self.setWindowTitle(f"Редактор темы: {theme_name}")
        self.setMinimumSize(1100, 700)
        self.resize(1200, 750)
        # Тёмный стиль + возможность растягивать
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {COLORS['bg_main']};
                border: 2px solid {COLORS['accent']};
            }}
        """)
        self.setSizeGripEnabled(True)  # уголок для растягивания
        self._load()
        self._build()

    # ---------------- данные ----------------
    def _path(self):
        return os.path.join(THEMES_DIR, self.theme_name, 'settings.json')

    def _load(self):
        defaults = {
            "variant": "Default",
            "nickname_font": "Cuprum", "nickname_font_size": 15, "nickname_font_weight": "Regular",
            "text_font": "Cuprum", "text_font_size": 15, "text_font_weight": "Regular",
            "nickname_color": "#FF9900", "reply_color": "#FF9900",
            "text_color": "#C1B078", "link_color": "#67CE00",
            "appear_effect": "slideInRight", "hide_effect": "none",
            "show_time": 10, "hide_messages": False,
            "nickname_shadow": True, "shadow_color": "#B85817", "shadow_size": 3,
            "show_icons": True,
        }
        if os.path.isfile(self._path()):
            try:
                with open(self._path(), encoding='utf-8') as f:
                    self.cfg = {**defaults, **json.load(f)}
                return
            except:
                pass
        self.cfg = defaults

    def _collect(self):
        return {
            "variant": self.combo_variant.currentText(),
            "nickname_font": self.combo_nick_font.currentText(),
            "nickname_font_size": self.spin_nick_size.value(),
            "nickname_font_weight": self.combo_nick_weight.currentText(),
            "text_font": self.combo_text_font.currentText(),
            "text_font_size": self.spin_text_size.value(),
            "text_font_weight": self.combo_text_weight.currentText(),
            "nickname_color": self.line_nick_color.text(),
            "reply_color": self.line_reply_color.text(),
            "text_color": self.line_text_color.text(),
            "link_color": self.line_link_color.text(),
            "appear_effect": self.combo_appear.currentText(),
            "hide_effect": self.combo_hide.currentText(),
            "show_time": self.slider_time.value(),
            "hide_messages": self.chk_hide.isChecked(),
            "nickname_shadow": self.chk_shadow.isChecked(),
            "shadow_color": self.line_shadow_color.text(),
            "shadow_size": self.slider_shadow.value(),
            "show_icons": self.chk_icons.isChecked(),
        }

    # ---------------- UI ----------------
    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # === ЗАГОЛОВОК ===
        header = QWidget()
        header.setStyleSheet(f"background-color: {COLORS['bg_input']}; border-bottom: 1px solid {COLORS['border']};")
        hl = QHBoxLayout(header)
        hl.setContentsMargins(15, 10, 15, 10)
        title_lbl = QLabel(f"⚙️ Редактор темы: {self.theme_name}")
        title_lbl.setStyleSheet(f"color: {COLORS['accent']}; font-size: 16px; font-weight: bold;")
        hl.addWidget(title_lbl)
        hl.addStretch()
        root.addWidget(header)

        # === 3 КОЛОНКИ ===
        body = QWidget()
        body.setStyleSheet("background-color: transparent;")
        body_lay = QHBoxLayout(body)
        body_lay.setContentsMargins(10, 10, 10, 10)
        body_lay.setSpacing(10)

        # --- ЛЕВАЯ: вариант + список параметров ---
        left = self._build_left_panel()
        body_lay.addWidget(left)

        # --- ЦЕНТР: параметры ---
        center = self._build_center_panel()
        body_lay.addWidget(center, stretch=1)

        # --- ПРАВАЯ: превью + тесты ---
        right = self._build_right_panel()
        body_lay.addWidget(right)

        root.addWidget(body, stretch=1)

        # === ФУТЕР ===
        footer = self._build_footer()
        root.addWidget(footer)

    def _build_left_panel(self):
        """Левая колонка: вариант + кнопки + список параметров"""
        w = QWidget()
        w.setFixedWidth(180)
        w.setStyleSheet(f"""
            QWidget {{
                background-color: {COLORS['bg_main']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
            }}
        """)
        lay = QVBoxLayout(w)
        lay.setContentsMargins(10, 10, 10, 10)

        lbl = QLabel("ВАРИАНТ")
        lbl.setStyleSheet(f"color: {COLORS['accent']}; font-size: 11px; font-weight: bold;")
        lay.addWidget(lbl)
        self.combo_variant = QComboBox()
        self.combo_variant.addItems(["Default", "Compact", "Wide"])
        self.combo_variant.setStyleSheet(self._combo_style())
        lay.addWidget(self.combo_variant)

        btn_row = QWidget()
        br = QHBoxLayout(btn_row)
        br.setContentsMargins(0, 5, 0, 0)
        for icon in ["+", "📋", "✏️", "−", "💾"]:
            b = QPushButton(icon)
            b.setFixedSize(30, 26)
            b.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLORS['bg_input']}; color: {COLORS['text_primary']};
                    border: 1px solid {COLORS['border']}; border-radius: 3px; font-size: 12px;
                }}
                QPushButton:hover {{ background-color: {COLORS['bg_hover']}; }}
            """)
            br.addWidget(b)
        lay.addWidget(btn_row)

        lbl2 = QLabel("Все параметры")
        lbl2.setStyleSheet(f"color: {COLORS['accent']}; font-size: 12px; font-weight: bold; padding-top: 10px;")
        lay.addWidget(lbl2)
        lbl3 = QLabel("other")
        lbl3.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 11px;")
        lay.addWidget(lbl3)
        lay.addStretch()
        return w

    def _build_center_panel(self):
        """Центральная колонка: заголовок + URL + поиск + сетка параметров"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet(f"""
            QScrollArea {{ background: transparent; border: none; }}
            QScrollBar:vertical {{
                background-color: {COLORS['bg_main']}; width: 8px; border-radius: 4px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {COLORS['accent']}; border-radius: 4px; min-height: 20px;
            }}
        """)

        cw = QWidget()
        cw.setStyleSheet("background-color: transparent;")
        cl = QVBoxLayout(cw)
        cl.setContentsMargins(10, 10, 10, 10)
        cl.setSpacing(12)

        theme_title = QLabel(self.theme_name)
        theme_title.setStyleSheet(f"color: {COLORS['text_primary']}; font-size: 20px; font-weight: bold;")
        cl.addWidget(theme_title)

        url = QLabel(f"http://localhost:8383/themes/{self.theme_name}/index.html?variant=default")
        url.setStyleSheet(f"""
            color: {COLORS['text_secondary']}; font-size: 11px;
            background-color: {COLORS['bg_input']};
            border: 1px solid {COLORS['border']}; border-radius: 4px; padding: 4px 8px;
        """)
        cl.addWidget(url)

        search_row = QWidget()
        sr = QHBoxLayout(search_row)
        sr.setContentsMargins(0, 5, 0, 5)
        search = QLineEdit()
        search.setPlaceholderText("Поиск по имени, описанию, категории...")
        search.setStyleSheet(f"""
            QLineEdit {{
                background-color: {COLORS['bg_input']}; color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border']}; border-radius: 4px;
                padding: 6px 10px; font-size: 12px;
            }}
        """)
        sr.addWidget(search)
        lang = QComboBox()
        lang.addItems(["Русский", "English"])
        lang.setStyleSheet(self._combo_style())
        sr.addWidget(lang)
        cl.addWidget(search_row)

        # Сетка параметров
        grid = QGridLayout()
        grid.setSpacing(12)
        grid.setContentsMargins(0, 5, 0, 5)
        row = 0

        self.combo_nick_font, self.spin_nick_size, self.combo_nick_weight = \
            self._font_group(grid, row, "ШРИФТ НИКНЕЙМА")
        self.combo_text_font, self.spin_text_size, self.combo_text_weight = \
            self._font_group(grid, row, "ШРИФТ ТЕКСТА", col=1)
        row += 1

        self.btn_nick_color, self.line_nick_color = \
            self._color_group(grid, row, "ЦВЕТ НИКА", self.cfg["nickname_color"])
        self.btn_reply_color, self.line_reply_color = \
            self._color_group(grid, row, "ЦВЕТ ОТВЕТА", self.cfg["reply_color"], col=1)
        row += 1
        self.btn_text_color, self.line_text_color = \
            self._color_group(grid, row, "ЦВЕТ ТЕКСТА", self.cfg["text_color"])
        self.btn_link_color, self.line_link_color = \
            self._color_group(grid, row, "ЦВЕТ ССЫЛОК", self.cfg["link_color"], col=1)
        row += 1

        grp = QGroupBox("ЭФФЕКТ ПОЯВЛЕНИЯ СООБЩЕНИЙ")
        grp.setStyleSheet(self._group_style())
        gl = QVBoxLayout(grp)
        self.combo_appear = QComboBox()
        self.combo_appear.addItems(APPEAR_EFFECTS)
        self.combo_appear.setStyleSheet(self._combo_style())
        gl.addWidget(self.combo_appear)
        grid.addWidget(grp, row, 0)

        grp = QGroupBox("СКРЫВАТЬ СООБЩЕНИЯ")
        grp.setStyleSheet(self._group_style())
        hl2 = QHBoxLayout(grp)
        self.chk_hide = QCheckBox("Выключено")
        self.chk_hide.setStyleSheet(self._checkbox_style())
        hl2.addWidget(self.chk_hide)
        hl2.addStretch()
        grid.addWidget(grp, row, 1)
        row += 1

        grp = QGroupBox("ЭФФЕКТ СКРЫТИЯ СООБЩЕНИЙ")
        grp.setStyleSheet(self._group_style())
        hl = QVBoxLayout(grp)
        self.combo_hide = QComboBox()
        self.combo_hide.addItems(HIDE_EFFECTS)
        self.combo_hide.setStyleSheet(self._combo_style())
        hl.addWidget(self.combo_hide)
        grid.addWidget(grp, row, 0, 1, 2)
        row += 1

        grp = QGroupBox("ВРЕМЯ ПОКАЗА СООБЩЕНИЙ")
        grp.setStyleSheet(self._group_style())
        hl = QHBoxLayout(grp)
        self.slider_time = QSlider(Qt.Orientation.Horizontal)
        self.slider_time.setRange(3, 30)
        self.slider_time.setStyleSheet(self._slider_style())
        hl.addWidget(self.slider_time)
        self.lbl_time = QLabel("10")
        self.lbl_time.setFixedWidth(30)
        self.lbl_time.setStyleSheet(f"color: {COLORS['accent']}; font-size: 13px; font-weight: bold;")
        self.slider_time.valueChanged.connect(lambda v: self.lbl_time.setText(str(v)))
        hl.addWidget(self.lbl_time)
        grid.addWidget(grp, row, 0)

        grp = QGroupBox("ТЕНЬ ДЛЯ НИКА")
        grp.setStyleSheet(self._group_style())
        hl3 = QHBoxLayout(grp)
        self.chk_shadow = QCheckBox("Включено")
        self.chk_shadow.setStyleSheet(self._checkbox_style())
        hl3.addWidget(self.chk_shadow)
        hl3.addStretch()
        grid.addWidget(grp, row, 1)
        row += 1

        grp = QGroupBox("РАЗМЕР ТЕНИ")
        grp.setStyleSheet(self._group_style())
        hl4 = QHBoxLayout(grp)
        self.slider_shadow = QSlider(Qt.Orientation.Horizontal)
        self.slider_shadow.setRange(0, 10)
        self.slider_shadow.setStyleSheet(self._slider_style())
        hl4.addWidget(self.slider_shadow)
        self.lbl_shadow = QLabel("3")
        self.lbl_shadow.setFixedWidth(30)
        self.lbl_shadow.setStyleSheet(f"color: {COLORS['accent']}; font-size: 13px; font-weight: bold;")
        self.slider_shadow.valueChanged.connect(lambda v: self.lbl_shadow.setText(str(v)))
        hl4.addWidget(self.lbl_shadow)
        grid.addWidget(grp, row, 0)

        grp = QGroupBox("ЦВЕТ ТЕНИ")
        grp.setStyleSheet(self._group_style())
        hl5 = QHBoxLayout(grp)
        self.line_shadow_color = QLineEdit(self.cfg["shadow_color"])
        self.line_shadow_color.setStyleSheet(self._line_style())
        hl5.addWidget(self.line_shadow_color)
        grid.addWidget(grp, row, 1)
        row += 1

        grp = QGroupBox("ПОКАЗЫВАТЬ ИКОНКИ САЙТОВ")
        grp.setStyleSheet(self._group_style())
        hl6 = QHBoxLayout(grp)
        self.chk_icons = QCheckBox("Включено")
        self.chk_icons.setStyleSheet(self._checkbox_style())
        hl6.addWidget(self.chk_icons)
        hl6.addStretch()
        grid.addWidget(grp, row, 0)

        cl.addLayout(grid)
        cl.addStretch()
        scroll.setWidget(cw)
        return scroll

    def _build_right_panel(self):
        """Правая колонка: превью + тестовые события"""
        w = QWidget()
        w.setFixedWidth(290)
        w.setStyleSheet(f"""
            QWidget {{
                background-color: {COLORS['bg_main']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
            }}
        """)
        lay = QVBoxLayout(w)
        lay.setContentsMargins(10, 10, 10, 10)

        self.preview = QLabel()
        self.preview.setFixedSize(265, 400)
        self.preview.setMinimumHeight(400)
        self.preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview.setStyleSheet(f"""
            QLabel {{
                background-color: {COLORS['bg_input']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
            }}
        """)
        self._update_preview()
        lay.addWidget(self.preview)

        size_lbl = QLabel("265 x 400")
        size_lbl.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 10px;")
        lay.addWidget(size_lbl)

        test_lbl = QLabel("Тестовые события")
        test_lbl.setStyleSheet(f"color: {COLORS['accent']}; font-size: 13px; font-weight: bold; padding-top: 10px;")
        lay.addWidget(test_lbl)

        for txt in ["Новое сообщение", "Оповещение", "Уведомление"]:
            b = QPushButton(txt)
            b.setStyleSheet(self._test_style())
            b.clicked.connect(lambda _, t=txt: self._test_event(t))
            lay.addWidget(b)

        lay.addStretch()
        return w

    def _build_footer(self):
        """Футер: кнопки Параметры/Отмена/Применить/ОК"""
        w = QWidget()
        w.setStyleSheet(f"background-color: {COLORS['bg_input']}; border-top: 1px solid {COLORS['border']};")
        lay = QHBoxLayout(w)
        lay.setContentsMargins(15, 10, 15, 10)

        btn_params = QPushButton("⚙️ Параметры")
        btn_params.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['bg_input']}; color: {COLORS['text_primary']};
                border: 1px solid {COLORS['accent']}; border-radius: 4px;
                padding: 8px 20px; font-size: 12px; font-weight: bold;
            }}
            QPushButton:hover {{ background-color: {COLORS['accent']}; color: white; }}
        """)
        lay.addWidget(btn_params)
        lay.addStretch()

        btn_cancel = QPushButton("Отмена")
        btn_cancel.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['bg_input']}; color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border']}; border-radius: 4px;
                padding: 8px 20px; font-size: 12px;
            }}
            QPushButton:hover {{ background-color: {COLORS['bg_hover']}; }}
        """)
        btn_cancel.clicked.connect(self.reject)
        lay.addWidget(btn_cancel)

        btn_apply = QPushButton("Применить")
        btn_apply.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['accent']}; color: white;
                border: none; border-radius: 4px;
                padding: 8px 20px; font-size: 12px; font-weight: bold;
            }}
            QPushButton:hover {{ background-color: #238636; }}
        """)
        btn_apply.clicked.connect(self._apply)
        lay.addWidget(btn_apply)

        btn_ok = QPushButton("ОК")
        btn_ok.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['accent']}; color: white;
                border: none; border-radius: 4px;
                padding: 8px 24px; font-size: 12px; font-weight: bold;
            }}
            QPushButton:hover {{ background-color: #238636; }}
        """)
        btn_ok.clicked.connect(self._save_and_close)
        lay.addWidget(btn_ok)
        return w

    def _font_group(self, grid, row, title, col=0):
        grp = QGroupBox(title)
        grp.setStyleSheet(self._group_style())
        gl = QVBoxLayout(grp)
        combo = QComboBox()
        combo.addItems(FONTS)
        combo.setStyleSheet(self._combo_style())
        gl.addWidget(combo)
        rw = QHBoxLayout()
        spin = QSlider(Qt.Orientation.Horizontal)
        spin.setRange(8, 36)
        spin.setStyleSheet(self._slider_style())
        rw.addWidget(spin)
        weight = QComboBox()
        weight.addItems(["Regular", "Bold", "Italic"])
        weight.setStyleSheet(self._combo_style())
        rw.addWidget(weight)
        gl.addLayout(rw)
        grid.addWidget(grp, row, col)
        return combo, spin, weight

    def _color_group(self, grid, row, title, color, col=0):
        grp = QGroupBox(title)
        grp.setStyleSheet(self._group_style())
        hl = QHBoxLayout(grp)
        line = QLineEdit(color)
        line.setStyleSheet(self._line_style())
        hl.addWidget(line)
        grid.addWidget(grp, row, col)
        return None, line

    # ---------------- стили ----------------
    def _group_style(self):
        return f"""
            QGroupBox {{
                color: {COLORS['text_primary']}; font-size: 12px; font-weight: bold;
                border: 1px solid {COLORS['border']}; border-radius: 5px;
                margin-top: 8px; padding-top: 12px;
            }}
            QGroupBox::title {{ subcontrol-origin: margin; left: 10px; padding: 0 5px; }}
        """

    def _combo_style(self):
        return f"""
            QComboBox {{
                background-color: {COLORS['bg_input']}; color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border']}; border-radius: 4px;
                padding: 4px 8px; min-height: 24px; font-size: 12px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {COLORS['bg_input']}; color: {COLORS['text_primary']};
                selection-background-color: {COLORS['accent']};
            }}
        """

    def _line_style(self):
        return f"""
            QLineEdit {{
                background-color: {COLORS['bg_input']}; color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border']}; border-radius: 4px;
                padding: 4px 8px; font-size: 12px;
            }}
        """

    def _slider_style(self):
        return f"""
            QSlider::groove:horizontal {{
                border: 1px solid {COLORS['border']}; height: 6px;
                background: {COLORS['bg_input']}; border-radius: 3px;
            }}
            QSlider::handle:horizontal {{
                background: {COLORS['accent']}; border: 1px solid {COLORS['accent']};
                width: 16px; margin: -5px 0; border-radius: 8px;
            }}
        """

    def _checkbox_style(self):
        return f"""
            QCheckBox {{ color: {COLORS['text_primary']}; font-size: 12px; spacing: 8px; }}
        """

    def _test_style(self):
        return f"""
            QPushButton {{
                background-color: {COLORS['bg_input']}; color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border']}; border-radius: 4px;
                padding: 6px 10px; font-size: 12px;
            }}
            QPushButton:hover {{ background-color: {COLORS['bg_hover']}; border-color: {COLORS['accent']}; }}
        """

    # ---------------- логика ----------------
    def _apply_loaded(self):
        c = self.cfg
        def set_combo(combo, val):
            i = combo.findText(val)
            combo.setCurrentIndex(i if i >= 0 else 0)
        set_combo(self.combo_variant, c["variant"])
        set_combo(self.combo_nick_font, c["nickname_font"])
        self.spin_nick_size.setValue(c["nickname_font_size"])
        set_combo(self.combo_nick_weight, c["nickname_font_weight"])
        set_combo(self.combo_text_font, c["text_font"])
        self.spin_text_size.setValue(c["text_font_size"])
        set_combo(self.combo_text_weight, c["text_font_weight"])
        self.line_nick_color.setText(c["nickname_color"])
        self.line_reply_color.setText(c["reply_color"])
        self.line_text_color.setText(c["text_color"])
        self.line_link_color.setText(c["link_color"])
        self.line_shadow_color.setText(c["shadow_color"])
        set_combo(self.combo_appear, c["appear_effect"])
        set_combo(self.combo_hide, c["hide_effect"])
        self.slider_time.setValue(c["show_time"]); self.lbl_time.setText(str(c["show_time"]))
        self.slider_shadow.setValue(c["shadow_size"]); self.lbl_shadow.setText(str(c["shadow_size"]))
        self.chk_hide.setChecked(c["hide_messages"])
        self.chk_shadow.setChecked(c["nickname_shadow"])
        self.chk_icons.setChecked(c["show_icons"])

    def _update_preview(self):
        """Рисуем 3 сообщения текущими настройками"""
        pm = QPixmap(265, 400)
        pm.fill(QColor("#1a1208"))
        p = QPainter(pm)
        msgs = [("Player123", "Привет всем!"), ("Gamer456", "Как дела?"), ("Streamer", "Го рейд!")]
        y = 20
        for nick, text in msgs:
            p.fillRect(8, y, 249, 60, QColor(20, 14, 8, 220))
            p.setPen(QColor(107, 84, 38))
            p.drawRect(8, y, 249, 60)
            p.fillRect(8, y, 4, 60, QColor(self.line_nick_color.text() if hasattr(self, 'line_nick_color') else "#FF9900"))
            p.setPen(QColor(self.line_nick_color.text() if hasattr(self, 'line_nick_color') else "#FF9900"))
            p.setFont(QFont("Cuprum", 12, QFont.Weight.Bold))
            p.drawText(20, y + 22, nick + ":")
            p.setPen(QColor(self.line_text_color.text() if hasattr(self, 'line_text_color') else "#C1B078"))
            p.setFont(QFont("Cuprum", 11))
            p.drawText(20, y + 45, text)
            y += 75
        p.end()
        self.preview.setPixmap(pm)

    def _test_event(self, event_type):
        print(f"🧪 Тест: {event_type} для темы {self.theme_name}")
        self._update_preview()

    def _apply(self):
        os.makedirs(os.path.dirname(self._path()), exist_ok=True)
        with open(self._path(), 'w', encoding='utf-8') as f:
            json.dump(self._collect(), f, indent=2, ensure_ascii=False)
        print(f"✅ Настройки темы '{self.theme_name}' применены")
        self.settings_saved.emit(self._collect())

    def _save_and_close(self):
        self._apply()
        self.accept()