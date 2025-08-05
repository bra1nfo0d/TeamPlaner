from PySide6.QtWidgets import QLabel, QFrame, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from widgets.clickable_label import ClickableLabel
from widgets.clickable_frame import ClickableFrame
from core.storage_manager import StorageManager


class UserInput:
	def __init__(self, text_memory=None, layout=None, spacer=None, date=None):
		self.date = date
		
		self.layout = layout
		self.spacer = spacer
		self.text_memory = text_memory
		
		self.frame = ClickableFrame()
		self.frame_layout = QVBoxLayout(self.frame)
		self.frame.clicked.connect(lambda: self.click())
		self.frame.setStyleSheet("""
								 QFrame {
					   				border: 2px solid #ccc;
						   			border-radius: 7px;}""")

		for i in range(len(text_memory)):
			label = QLabel()
			label.setText("\n".join(text_memory[i]))
			label.setAlignment(Qt.AlignCenter)
			label.setFont(QFont("Arial", 10))
			label.setStyleSheet("""
								QLabel {
					   				border: 2px solid #ccc;
					   				padding-top: 3px;
					   				padding-bottom: 3px;}""")
			self.frame_layout.addWidget(label)

	def show_input(self):
		padding_layout = QVBoxLayout()
		padding_layout.setContentsMargins(0, 0, 0, 5)
		spacer = self.spacer
		self.layout.removeItem(self.spacer)
		padding_layout.addWidget(self.frame)
		self.layout.addLayout(padding_layout)
		self.layout.addItem(spacer)

	def click(self):
		storage_manager = StorageManager()
		storage_manager.delete_user_input(date=self.date, text_memory=self.text_memory)
		
		self.layout.removeWidget(self.frame)
		self.frame.deleteLater()

if __name__ == "__main__":
	pass