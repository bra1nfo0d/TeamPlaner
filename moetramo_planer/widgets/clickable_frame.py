from PySide6.QtWidgets import QFrame
from PySide6.QtCore import Signal, Qt

class ClickableFrame(QFrame):
	clicked = Signal()

	def __init__(self):
		super().__init__()
		self.setCursor(Qt.PointingHandCursor)
	
	def mousePressEvent(self, event):
		self.clicked.emit()
		return super().mousePressEvent(event)

if __name__ == "__main__":
	pass