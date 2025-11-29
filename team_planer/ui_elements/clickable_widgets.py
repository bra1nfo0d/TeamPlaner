from PySide6.QtWidgets import QFrame, QLabel
from PySide6.QtCore import Signal, Qt

class ClickableFrame(QFrame):
	clicked = Signal()

	def __init__(self, parent: object = None):
		super().__init__(parent)
		self.setCursor(Qt.PointingHandCursor)
	
	def mousePressEvent(self, event) -> None:
		self.clicked.emit()
		return super().mousePressEvent(event)

	
class ClickableLabel(QLabel):
	clicked = Signal()

	def __init__(self, text: str = "", parent: object = None):
		super().__init__(text, parent)
		self.setCursor(Qt.PointingHandCursor)
	
	def mousePressEvent(self, event) -> None:
		self.clicked.emit()
		super().mousePressEvent(event)


class OutputLable(QLabel):
	outputEmitted = Signal(object)

	def __init__(self, text: str = "", output = None, parent: object = None):
		super().__init__(text, parent)
		self.output_value = output
		self.setCursor(Qt.PointingHandCursor)
	
	def mousePressEvent(self, event):
		if self.output_value is not None:
			self.outputEmitted.emit(self.output_value)
		super().mousePressEvent(event)


if __name__ == "__main__":
	pass