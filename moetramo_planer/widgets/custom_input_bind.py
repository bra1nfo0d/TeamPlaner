from PySide6.QtWidgets import QLineEdit
from PySide6.QtCore import Qt, Signal

class CustomLineEdit(QLineEdit):
	deletePressed = Signal()

	def keyPressEvent(self, event):
		if event.key() == Qt.Key_Delete:
			self.deletePressed.emit()
		else:
			super().keyPressEvent(event)