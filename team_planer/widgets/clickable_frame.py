from PySide6.QtWidgets import QFrame
from PySide6.QtCore import Signal, Qt

class ClickableFrame(QFrame):
	"""
	A QFrame subclass that emits a `clicked` signal when pressed with the mouse.

	This widget behaves like a clickable container: you can use it to wrap
	other widgets and detect when the user clicks anywhere inside the frame.

	Atrributes:
		clicked (Signal): Emitted when the frame is pressed with the mouse.
	"""
	clicked = Signal()

	def __init__(self):
		"""
		Initialize the frame and set a pointing-hand cursor.
		"""
		super().__init__()
		self.setCursor(Qt.PointingHandCursor)
	
	def mousePressEvent(self, event) -> None:
		"""
		Handle mouse press events.

		Emits the `clicked` signal before delegating to the base
		QFrame implementation.

		Args:
			event (QMouseEvent): The mouse press event.
		"""
		self.clicked.emit()
		return super().mousePressEvent(event)


if __name__ == "__main__":
	pass