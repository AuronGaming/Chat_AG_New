"""Визуальное оформление секции Звук"""
from main_screen.theme_config import COLORS

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
"""

SLIDER_STYLE = f"""
    QSlider::groove:horizontal {{
        border: 1px solid {COLORS['border']};
        height: 6px;
        background: {COLORS['bg_input']};
        border-radius: 3px;
    }}
    QSlider::handle:horizontal {{
        background: {COLORS['accent']};
        border: 1px solid {COLORS['accent']};
        width: 14px;
        margin: -5px 0;
        border-radius: 7px;
    }}
    QSlider::handle:horizontal:hover {{
        background: {COLORS['accent']};
    }}
"""