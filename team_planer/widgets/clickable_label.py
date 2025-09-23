from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Signal, Qt

class ClickableLabel(QLabel):
	"""
	A QLabel subclass that emits a `clicked` signal when the label is pressed.

	This makes the label behave like a clickable button while still looking
	like a plain text/image label.

	Attributes:
		clicked (Signal): Emitted when the label is pressed with the mouse.
	"""
	clicked = Signal()

	def __init__(self, text: str = "", parent: object = None):
		"""
		Initialize the clickable label.

		Args:
			text (str, optional): Initial text to display. Defaults to "".
			parent (object, optional): Parent widget. Defaults to None.
		"""
		super().__init__(text, parent)
		self.setCursor(Qt.PointingHandCursor)
	
	def mousePressEvent(self, ev) -> None:
		"""
		Handle mouse press events.

		Emits the `clicked` signal before delegating to the base
		QLabel implementation.

		Args:
			ev (QMouseEvent): The mouse press event.
		"""
		self.clicked.emit()
		super().mousePressEvent(ev)


if __name__ == "__main__":
	pass