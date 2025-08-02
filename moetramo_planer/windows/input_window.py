from PySide6.QtWidgets import QWidget, QLineEdit, QHBoxLayout, QLabel, QVBoxLayout, QPushButton, QFrame
from PySide6.QtCore import Qt
from widgets.custom_input_bind import CustomLineEdit
from widgets.clickable_label import ClickableLabel
from widgets.user_input import UserInput
from core.storage_manager import StorageManager

class InputWindow(QWidget):
	def __init__(self, day, date, frame_layout, spacer):
		super().__init__()

		self.date = date
		self.frame_layout = frame_layout
		self.spacer = spacer

		# memorys
		self.text_memory = []
		self.label_memory = []

		# window settings
		self.setWindowFlags(Qt.WindowStaysOnTopHint)
		self.setWindowTitle(f"{day} - {date}")

		# display frame
		self.frame = QFrame()
		self.frame.setFrameShape(QFrame.Box)
		self.frame.setLineWidth(2)
		self.frame.setStyleSheet("""padding: 4px; 
							    	border: 1px solid #ccc;
					  		     	border-radius: 10px;
					  		     """)

		# user input field
		self.input_field = CustomLineEdit()
		self.input_field.returnPressed.connect(self.on_return)
		self.input_field.deletePressed.connect(self.on_delete)

		# submit button
		self.button = QPushButton("Submit")
		self.button.clicked.connect(self.on_click)

		# frame layout
		self.f_layout = QVBoxLayout()
		self.f_layout.addWidget(self.frame)

		# horizontal layout
		h_layout = QHBoxLayout()
		h_layout.addLayout(self.f_layout)
		h_layout.addWidget(self.input_field)
		h_layout.addWidget(self.button)

		# vertical layout
		v_layout = QVBoxLayout()
		v_layout.addLayout(h_layout)

		self.setLayout(v_layout)

	# return key event (adds user input)
	def on_return(self):
		text = self.input_field.text()
		label = QLabel(text)
		self.f_layout.addWidget(label)
		self.text_memory.append(text)
		self.label_memory.append(label)
		self.input_field.clear()
	
	# delete key event (deletes user input)
	def on_delete(self):
		label = self.label_memory[-1]
		self.f_layout.removeWidget(label)
		label.deleteLater()
		label = None
		self.label_memory.pop()
		self.text_memory.pop()
	
	# button pressed event (creates the user widget)
	def on_click(self):
		user_input = UserInput(text_memory=self.text_memory, layout=self.frame_layout, spacer=self.spacer, date=self.date)
		user_input.show_input()
		storage_manager = StorageManager()
		storage_manager.store_user_input(date=self.date, text_memory=self.text_memory)
		self.clear_memory()
		
	def clear_memory(self):
		self.text_memory = []
		for i in range(len(self.label_memory)):
			label = self.label_memory.pop()
			self.f_layout.removeWidget(label)
			label.deleteLater()

if __name__ == "__main__":
	pass