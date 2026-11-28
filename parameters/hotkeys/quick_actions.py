from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class QuickActionsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        lay = QVBoxLayout(self)
        lay.addWidget(QLabel('Быстрые действия — в разработке'))
