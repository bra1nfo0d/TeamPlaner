from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Signal, Qt

class ClickableLabel(QLabel):
	clicked = Signal()

	def __init__(self, text="", parent=None):
		super().__init__(text, parent)
		self.setCursor(Qt.PointingHandCursor)
	
	def mousePressEvent(self, ev):
		self.clicked.emit()
		super().mousePressEvent(ev)

if __name__ == "__main__":
	pass