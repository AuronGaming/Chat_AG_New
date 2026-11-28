"""Секция Тема оформления — в разработке"""
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from main_screen.theme_config import COLORS

class ThemeSection(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        lay = QVBoxLayout(self)
        title = QLabel("Тема оформления")
        title.setStyleSheet(f"font-size: 22px; color: {COLORS['accent']}; font-weight: bold;")
        lay.addWidget(title)
        desc = QLabel("Раздел в разработке")
        desc.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 14px; padding: 20px;")
        lay.addWidget(desc)
        lay.addStretch()

    def save_data(self):
        pass