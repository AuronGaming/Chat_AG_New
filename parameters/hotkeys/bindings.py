from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class BindingsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        lay = QVBoxLayout(self)
        lay.addWidget(QLabel('Горячие клавиши — в разработке'))
