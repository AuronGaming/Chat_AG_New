"""Визуальное оформление секции Общие"""
from main_screen.theme_config import COLORS
from main_screen.checkbox_style import checkbox_style
from main_screen.theme_config import COLORS

CHECKBOX_STYLE = checkbox_style(
    text_color=COLORS['text_primary'],
    border_color=COLORS['border'],
    bg_color=COLORS['bg_input'],
    accent_color=COLORS['accent']
)

SECTION_TITLE_STYLE = f"font-size: 22px; color: {COLORS['accent']}; font-weight: bold;"
SECTION_SUBTITLE_STYLE = f"font-size: 12px; color: {COLORS['text_secondary']}; padding-bottom: 10px;"

GROUP_BOX_STYLE = f"""
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

CHECKBOX_STYLE = f"""
    QCheckBox {{
        color: {COLORS['text_primary']};
        font-size: 12px;
        spacing: 8px;
    }}
    QCheckBox::indicator {{
        width: 16px; height: 16px;
        border: 2px solid {COLORS['border']};
        border-radius: 3px;
        background-color: {COLORS['bg_input']};
    }}
    QCheckBox::indicator:checked {{
        background-color: {COLORS['accent']};
        border-color: {COLORS['accent']};
    }}
    QCheckBox::indicator:hover {{
        border-color: {COLORS['accent']};
    }}
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
    QLineEdit:focus {{
        border-color: {COLORS['accent']};
    }}
"""

COMBO_STYLE = f"""
    QComboBox {{
        background-color: {COLORS['bg_input']};
        color: {COLORS['text_primary']};
        border: 1px solid {COLORS['border']};
        border-radius: 4px;
        padding: 6px 10px;
        font-size: 12px;
    }}
    QComboBox::drop-down {{
        border: none;
        width: 20px;
    }}
    QComboBox QAbstractItemView {{
        background-color: {COLORS['bg_input']};
        color: {COLORS['text_primary']};
        selection-background-color: {COLORS['accent']};
        border: 1px solid {COLORS['border']};
    }}
"""