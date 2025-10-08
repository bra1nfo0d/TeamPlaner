from PySide6.QtWidgets import QFrame, QLabel
from PySide6.QtCore import Signal, Qt

class ClickableFrame(QFrame):
	"""QFrame that emits a 'clicked' signal when pressed."""
	clicked = Signal()

	def __init__(self):
		"""Set up frame with pointing-hand cursor."""
		super().__init__()
		self.setCursor(Qt.PointingHandCursor)
	
	def mousePressEvent(self, event) -> None:
		"""
		Emit 'clicked' on mouse press.

		Args:
			event (QMouseEvent): Mouse press event.
		"""
		self.clicked.emit()
		return super().mousePressEvent(event)
	
class ClickableLabel(QLabel):
	"""QLabel that emits a 'clicked' signal when pressed."""
	clicked = Signal()

	def __init__(self, text: str = "", parent: object = None):
		"""
		Args:
			text (str, optional): Label text. Defaults to "".
			parent (object, optional): Parent widget. Default to None.
		"""
		super().__init__(text, parent)
		self.setCursor(Qt.PointingHandCursor)
	
	def mousePressEvent(self, ev) -> None:
		"""
		Emit 'clicked' on mouse press.

		Args:
			ev (QMouseEvent): Mouse press event.
		"""
		self.clicked.emit()
		super().mousePressEvent(ev)


if __name__ == "__main__":
	pass