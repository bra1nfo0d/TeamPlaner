from PySide6.QtWidgets import QLabel, QFrame, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from widgets.clickable_label import ClickableLabel
from widgets.clickable_frame import ClickableFrame
from core.storage_manager import StorageManager


class UserInput:
	def __init__(self, text_memory=None, layout=None, spacer=None, date=None, settings=False):
		self.date = date
		
		self.layout = layout
		self.spacer = spacer
		self.text_memory = text_memory		

		outer_border_color = settings[0]
		inner_border_color = settings[1]

		self.frame = ClickableFrame()
		self.frame_layout = QVBoxLayout(self.frame)
		self.frame.clicked.connect(lambda: self.click())
		self.frame.setStyleSheet(f"""
								 QFrame {"{"}
					   				border: 2px solid {outer_border_color};
						   			border-radius: 7px;{"}"}""")

		for i in range(len(text_memory)):
			label = QLabel()
			for j in range(len(text_memory[i])):
				cur_text = label.text()
				if type(text_memory[i][j]) == str and text_memory[i][j].startswith("+"):
					text = text_memory[i][j][1:]
				elif type(text_memory[i][j]) == str:
					text = text_memory[i][j]
				elif type(text_memory[i][j]) == tuple or type(text_memory[i][j] == list):
					text = text_memory[i][j][0]
				if text == "_":
					pass
				elif cur_text == "":
					label.setText(text)
				else:
					label.setText(cur_text + "\n" + text)
			label.setAlignment(Qt.AlignCenter)
			label.setFont(QFont("Arial", 10))
			label.setStyleSheet(f"""
								QLabel {"{"}
									border: 2px solid {inner_border_color};
									padding-top: 3px;
									padding-bottom: 3px;{"}"}""")
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