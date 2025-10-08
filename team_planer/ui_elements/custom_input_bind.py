from PySide6.QtWidgets import QLineEdit
from PySide6.QtCore import Qt, Signal


class CustomLineEdit(QLineEdit):
	"""QLineEdit that emits 'deletePressed' when Delete is pressed."""

	deletePressed = Signal()

	def keyPressEvent(self, event) -> None:
		"""
		Emit 'deletePressed' on Delete key.

		Args:
			event (QKeyEvent): Key press event.
		"""
		if event.key() == Qt.Key_Delete:
			self.deletePressed.emit()
		else:
			super().keyPressEvent(event)


if __name__ == "__main__":
	pass