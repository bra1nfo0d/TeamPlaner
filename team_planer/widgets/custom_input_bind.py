from PySide6.QtWidgets import QLineEdit
from PySide6.QtCore import Qt, Signal

class CustomLineEdit(QLineEdit):
	"""
	A QLineEdit subclass that emits a custom signal when the Delete key is pressed.

	This is useful if you want to handle Delete events separately from the normal
	key event handling, e.g., to trigger deletion of items in a list or database.

	Attributes:
		deletePressed (Signal): Emitted when the Delete key is pressed while
								the line edit is focused.
	"""
	deletePressed = Signal()

	def keyPressEvent(self, event) -> None:
		"""
		Handle key press events.

		Emits the `deletePressed` signal if the Delete key is pressed.
		Otherwise, falls back to the standard QLineEdit behavior.

		Args:
			event (QKeyEvent): The key press event.
		"""
		if event.key() == Qt.Key_Delete:
			self.deletePressed.emit()
		else:
			super().keyPressEvent(event)


if __name__ == "__main__":
	pass