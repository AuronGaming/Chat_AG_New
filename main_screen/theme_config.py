"""Тема оформления Chat_AG — цвета, стили кнопок, общие стили настроек"""
    # ============================================================================
# ЦВЕТА
# ============================================================================
COLORS = {
    'bg_main': '#0d1117',
    'bg_input': '#161b22',
    'bg_hover': '#21262d',
    'accent': '#2ea043',
    'text_primary': '#c9d1d9',
    'text_secondary': '#8b949e',
    'border': '#30363d',
    'error': '#ef4444',
    'success': '#2ea043',
    'warning': '#f59e0b',
    'info': '#3b82f6',
}


# ============================================================================
# СТИЛИ КНОПОК
# ============================================================================
BUTTON_DEFAULT = f"""
    QPushButton {{
        background-color: {COLORS['bg_input']};
        color: {COLORS['text_primary']};
        border: 1px solid {COLORS['border']};
        border-radius: 4px;
        padding: 6px 16px;
        font-size: 12px;
    }}
    QPushButton:hover {{
        background-color: {COLORS['bg_hover']};
    }}
"""
# ============================================================
# СТИЛЬ ЧЕКБОКСА
# ============================================================
from main_screen.checkbox_style import checkbox_style

CHECKBOX_STYLE = checkbox_style(
    text_color=COLORS['text_primary'],
    border_color=COLORS['border'],
    bg_color=COLORS['bg_input'],
    accent_color=COLORS['accent']
)

BUTTON_ACCENT = f"""
    QPushButton {{
        background-color: {COLORS['accent']};
        color: white;
        border: none;
        border-radius: 4px;
        padding: 6px 16px;
        font-size: 12px;
        font-weight: bold;
    }}
    QPushButton:hover {{
        background-color: #238636;
    }}
"""

LIST_STYLE = f"""
    QListWidget {{
        background-color: {COLORS['bg_main']};
        color: {COLORS['text_primary']};
        border: 1px solid {COLORS['border']};
        border-radius: 4px;
        font-size: 12px;
        padding: 5px;
    }}
    QListWidget::item {{
        padding: 8px 12px;
        border-radius: 4px;
        margin: 2px 0;
    }}
    QListWidget::item:selected {{
        background-color: {COLORS['accent']};
        color: white;
    }}
    QListWidget::item:hover {{
        background-color: {COLORS['bg_hover']};
    }}
"""


# ============================================================================
# ОБЩИЕ СТИЛИ ДЛЯ НАСТРОЕК
# ============================================================================

def checkbox_style(font_size=12, bold=False):
    weight = "bold;" if bold else "normal;"
    return f"""
        QCheckBox {{
            color: {COLORS['text_primary']};
            font-size: {font_size}px;
            font-weight: {weight}
            spacing: 8px;
        }}
        QCheckBox::indicator {{
            width: 16px; height: 16px;
            border: 2px solid {COLORS['accent']};
            border-radius: 3px;
            background-color: {COLORS['bg_input']};
        }}
        QCheckBox::indicator:checked {{
            background-color: {COLORS['accent']};
        }}
    """


def input_style():
    return f"""
        QLineEdit {{
            background-color: {COLORS['bg_input']};
            color: {COLORS['text_primary']};
            border: 1px solid {COLORS['border']};
            border-radius: 4px;
            padding: 6px 10px;
            font-size: 12px;
        }}
        QLineEdit:focus {{ border-color: {COLORS['accent']}; }}
    """


def combo_style():
    return f"""
        QComboBox {{
            background-color: {COLORS['bg_input']};
            color: {COLORS['text_primary']};
            border: 1px solid {COLORS['border']};
            border-radius: 4px;
            padding: 6px 10px;
            font-size: 12px;
        }}
        QComboBox::drop-down {{ border: none; width: 20px; }}
        QComboBox QAbstractItemView {{
            background-color: {COLORS['bg_input']};
            color: {COLORS['text_primary']};
            selection-background-color: {COLORS['accent']};
        }}
    """


def spin_style():
    return f"""
        QSpinBox {{
            background-color: {COLORS['bg_input']};
            color: {COLORS['text_primary']};
            border: 1px solid {COLORS['border']};
            border-radius: 4px;
            padding: 6px 10px;
            font-size: 12px;
        }}
        QSpinBox:focus {{ border-color: {COLORS['accent']}; }}
    """


def slider_style():
    return f"""
        QSlider::groove:horizontal {{
            border: 1px solid {COLORS['border']};
            height: 8px;
            background: {COLORS['bg_input']};
            border-radius: 4px;
        }}
        QSlider::handle:horizontal {{
            background: {COLORS['accent']};
            border: 1px solid {COLORS['border']};
            width: 18px;
            margin: -5px 0;
            border-radius: 9px;
        }}
        QSlider::handle:horizontal:hover {{ background: #238636; }}
    """


def green_button_style(height=35):
    return f"""
        QPushButton {{
            background-color: {COLORS['accent']};
            color: white;
            border: none;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
            height: {height}px;
        }}
        QPushButton:hover {{ background-color: #238636; }}
    """


def purple_button_style(height=42):
    return f"""
        QPushButton {{
            background-color: #8B5CF6;
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 13px;
            font-weight: bold;
            height: {height}px;
        }}
        QPushButton:hover {{ background-color: #7C3AED; }}
    """


def red_button_style(height=30):
    return f"""
        QPushButton {{
            background-color: #ef4444;
            color: white;
            border: none;
            border-radius: 4px;
            font-size: 11px;
            font-weight: bold;
            height: {height}px;
        }}
        QPushButton:hover {{ background-color: #dc2626; }}
    """


def browse_button_style():
    return f"""
        QPushButton {{
            background-color: {COLORS['bg_input']};
            color: {COLORS['text_primary']};
            border: 1px solid {COLORS['border']};
            border-radius: 4px;
            font-size: 12px;
        }}
    """


def scroll_style():
    return f"""
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


def list_widget_style():
    return f"""
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
    """


def panel_border_style():
    return f"""
        QWidget {{
            border: 1px solid {COLORS['border']};
            border-radius: 4px;
            background-color: {COLORS['bg_main']};
        }}
    """


def group_box_style():
    return f"""
        QGroupBox {{
            color: {COLORS['accent']};
            font-size: 13px;
            font-weight: bold;
            border: 1px solid {COLORS['border']};
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
# ============================================================
# СТИЛЬ ЧЕКБОКСА
# ============================================================


from main_screen.checkbox_style import checkbox_style

CHECKBOX_STYLE = checkbox_style(
    text_color=COLORS['text_primary'],
    border_color=COLORS['border'],
    bg_color=COLORS['bg_input'],
    accent_color=COLORS['accent']
)