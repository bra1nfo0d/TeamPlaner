from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt
from widgets.clickable_label import ClickableLabel
from core.storage_manager import StorageManager


class UserInput:
	def __init__(self, text_memory=None, layout=None, spacer=None, date=None):
		self.date = date
		
		self.layout = layout
		self.spacer = spacer
		self.text_memory = text_memory
		
		self.label = ClickableLabel()
		self.label.clicked.connect(lambda: self.click())
		self.label.setText("\n".join(text_memory))
		self.label.setAlignment(Qt.AlignCenter)


	def show_input(self):
		spacer = self.spacer
		self.layout.removeItem(self.spacer)
		self.layout.addWidget(self.label)
		self.layout.addItem(spacer)

	def click(self):
		storage_manager = StorageManager()
		storage_manager.delete_user_input(date=self.date, text_memory=self.text_memory)
		
		self.layout.removeWidget(self.label)
		self.label.deleteLater()

if __name__ == "__main__":
	pass