from PySide6.QtWidgets import(QWidget, QHBoxLayout, QLabel, QVBoxLayout,
							   QPushButton, QFrame, QSpacerItem, QSizePolicy, QComboBox)
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QShortcut, QKeySequence
from widgets.custom_input_bind import CustomLineEdit
from widgets.user_input import UserInput
from core.storage_manager import StorageManager
from core.config_manager import ConfigManager

class InputWindow(QWidget):
	def __init__(self, day, date, frame_layout, frame_spacer):
		super().__init__()

		self.resize(400, 400)
		self.setFixedSize(400, 400)

		self.date = date
		self.frame_layout = frame_layout
		self.frame_spacer = frame_spacer

		self.config_manager = ConfigManager()

		self.text_memory = []
		self.label_memory = []
		self.label_pointer = [0, 0] # change all the list pointer to tupel

		self.setWindowFlags(Qt.WindowStaysOnTopHint)
		self.setWindowTitle(f"{day} - {date}")

		self.frame = QFrame()
		self.frame.setFrameShape(QFrame.Box)
		self.frame.setLineWidth(2)
		self.frame.setStyleSheet("""padding: 4px; 
							    	border: 1px solid #ccc;
					  		     	border-radius: 10px;
					  		     """)

		self.drop_bar = QComboBox()
		self.drop_bar.addItems(self.config_manager.load_config()["input_types"])
		self.drop_bar.currentTextChanged.connect(self.on_value_changed)

		self.input_field = CustomLineEdit()
		self.input_field.returnPressed.connect(self.on_return)
		self.input_field.deletePressed.connect(self.on_delete)		
		
		self.button = QPushButton("Submit")
		self.button.clicked.connect(self.on_click)

		spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

		self.input_layout = QVBoxLayout(self.frame)

		self.row1 = QVBoxLayout()
		self.row1.addWidget(self.frame)
		self.row1.addItem(spacer)

		self.row2 = QVBoxLayout()
		self.row2.addWidget(self.drop_bar)
		self.row2.addWidget(self.input_field)
		self.row2.addWidget(self.button)
		self.row2.addItem(spacer)

		main_layout = QHBoxLayout(self)
		main_layout.addLayout(self.row1)
		main_layout.addLayout(self.row2)

		self.setLayout(main_layout)

		down_shortcut = QShortcut(Qt.Key_Down, self.input_field)
		down_shortcut.activated.connect(lambda: self.on_arrow_press("down"))
		up_shortcut = QShortcut(Qt.Key_Up, self.input_field)
		up_shortcut.activated.connect(lambda: self.on_arrow_press("up"))

		self.cur_input_type = self.config_manager.load_config()["input_types"][0]
		self.on_value_changed(self.cur_input_type)

	def on_return(self):
		input_field_text = self.input_field.text()
		if input_field_text == "":
			return
		label = self.label_memory[self.label_pointer[0]]
		if self.text_memory[self.label_pointer[0]]:
			cur_label_text = label.text()
			label.setText(cur_label_text + "\n" + input_field_text)
		else:
			label.setText(input_field_text)
		self.text_memory[self.label_pointer[0]].append(input_field_text)
		self.input_field.clear()
		print(self.text_memory)
	
	def on_delete(self):
		if len(self.text_memory[self.label_pointer[0]]) <= 1:
			x = 0
		else:
			x = 1
		try:
			label = self.label_memory[self.label_pointer[0]]
			del_text = self.text_memory[self.label_pointer[0]].pop()
			cur_text = label.text()
			label.setText(cur_text[:len(cur_text)-len(del_text)-x])
		except IndexError:
			pass
	
	def on_click(self):
		user_input = UserInput(text_memory=self.text_memory, layout=self.frame_layout, spacer=self.frame_spacer, date=self.date)
		user_input.show_input()
		storage_manager = StorageManager()
		storage_manager.store_user_input(date=self.date, text_memory=self.text_memory)
		self.clear_memory()
		
	def clear_memory(self):
		cur_headers = self.config_manager.load_config()["input_types_header"][self.cur_input_type]
		self.text_memory = []
		for i in range(len(self.label_memory)):
			if cur_headers[i] != "_":
				self.label_memory[i].setText(cur_headers[i])
			else:
				self.label_memory[i].setText("")
		self.label_pointer = [0, len(cur_headers)]
		# last cur label stays yellow color (change so the label returns to normal color)

	def on_value_changed(self, value):
		self.cur_input_type = value
		self.clear_memory()
		headers = self.config_manager.load_config()["input_types_header"][value]
		for i in range(len(headers)):
			self.text_memory.append([])
			if headers[i] != "_":
				self.text_memory[i].append(headers[i])
				label = QLabel(headers[i])
			else:
				label = QLabel()
			label.setAlignment(Qt.AlignCenter)
			label.setStyleSheet("""
								QLabel {
					   				border: 2px solid #ccc;}""")
			self.input_layout.addWidget(label)
			self.label_memory.append(label)
		first_label = self.label_memory[0]
		first_label.setStyleSheet("""
								  QLabel {
									border: 2px solid yellow;}""")
		self.label_pointer = [0, len(headers)]
		print(self.text_memory)
	
	def on_arrow_press(self, direction):
		lenght = self.label_pointer[1]
		pointer = self.label_pointer[0]

		if direction == "down":
			calc = (pointer+1)%lenght
		elif direction == "up":
			calc = (pointer-1)%lenght

		past_label = self.label_memory[self.label_pointer[0]]
		past_label.setStyleSheet("""
								 QLabel {
						   			border: 2px solid #ccc;}""")
		lenght = self.label_pointer[1]
		pointer = self.label_pointer[0]
		self.label_pointer = [calc, lenght]
		cur_label = self.label_memory[self.label_pointer[0]]
		cur_label.setStyleSheet("""
								 QLabel {
						   			border: 2px solid yellow;}""")


if __name__ == "__main__":
	pass