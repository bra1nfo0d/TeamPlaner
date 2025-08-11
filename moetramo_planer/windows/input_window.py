import re
from PySide6.QtWidgets import(QWidget, QHBoxLayout, QLabel, QVBoxLayout, QMessageBox,
							   QPushButton, QFrame, QSpacerItem, QSizePolicy, QComboBox)
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QShortcut, QKeySequence
from widgets.custom_input_bind import CustomLineEdit
from widgets.user_input import UserInput
from core.storage_manager import StorageManager
from core.config_manager import ConfigManager

class InputWindow(QWidget):
	def __init__(self, day, date, target_layout, target_spacer):
		super().__init__()

		self.resize(400, 400)
		self.setFixedSize(400, 400)

		self.date = date
		self.target_layout = target_layout
		self.target_spacer = target_spacer

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

		self.frame_layout = QVBoxLayout(self.frame)

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
		forbitten_pattern = r"^[_+]"
		if input_field_text == "":
			return
		if re.match(forbitten_pattern, input_field_text):
			self.show_warning(error_type="wrong_pattern")
			return
		label = self.label_memory[self.label_pointer[0]]
		if self.text_memory[self.label_pointer[0]] and self.text_memory[self.label_pointer[0]][0].startswith("+"):
			pattern = r".*#[\d]+[,.]?[\d]{,2}"
			if re.match(pattern, input_field_text):
				text_amount_list = input_field_text.split("#")
				text = text_amount_list[0]
				str_float = text_amount_list[1]
				save_float = re.sub(r",", r".", str_float)
				if self.text_memory[self.label_pointer[0]]:
					cur_label_text = label.text()
					label.setText(cur_label_text + "\n" + text)
				else:
					label.setText(text)
				self.text_memory[self.label_pointer[0]].append((text, float(save_float)))
				self.input_field.clear()
			else:
				self.show_warning(error_type="calc_error")
		else:
			print(bool(self.label_pointer[0]))
			if self.text_memory[self.label_pointer[0]] and self.text_memory[self.label_pointer[0]][-1] != "_":
				cur_label_text = label.text()
				label.setText(cur_label_text + "\n" + input_field_text)
			else:
				label.setText(input_field_text)
			self.text_memory[self.label_pointer[0]].append(input_field_text)
			self.input_field.clear()
		print(self.text_memory)
	
	def on_delete(self):	# if header is a + header and you delete it you get an error
		if len(self.text_memory[self.label_pointer[0]]) <= 1:
			x = 0
		else:
			x = 1
		try:
			label = self.label_memory[self.label_pointer[0]]
			cur_text = label.text()
			if type(self.text_memory[self.label_pointer[0]][-1]) == tuple:
				del_text = self.text_memory[self.label_pointer[0]].pop()
				del_text = del_text[0]
			else:
				del_text = self.text_memory[self.label_pointer[0]].pop()
			label.setText(cur_text[:len(cur_text)-len(del_text)-x])
		except IndexError:
			pass
		print(self.text_memory)
	
	def on_click(self):		# color does not come back on submit
		display_config = self.config_manager.load_config()["input_types_config"][self.cur_input_type]
		clac_value = self.config_manager.load_config()["calc_value"]
		for i in range(len(self.text_memory)):
			if self.text_memory[i][0].startswith("+"):
				num = 0
				for j in range(1, len(self.text_memory[i])):
					num += self.text_memory[i][j][1]
				if num >= clac_value:
					display_config = ["green", "#ccc"]
				else:
					display_config = ["red", "#ccc"]
		
		user_input = UserInput(text_memory=self.text_memory, layout=self.target_layout, spacer=self.target_spacer, date=self.date, settings=display_config)
		user_input.show_input()
		storage_manager = StorageManager()
		storage_manager.store_user_input(date=self.date, text_memory=self.text_memory, config=display_config)
		self.clear_memory(same_type=True)
		
	def clear_memory(self, same_type):
		if not same_type:
			self.text_memory = []
			for i in range(len(self.label_memory)):
				self.frame_layout.removeWidget(self.label_memory[i])
				self.label_memory[i].deleteLater()
			self.label_memory = []
		elif same_type:
			top_label = self.label_memory[0]
			cur_label = self.label_memory[self.label_pointer[0]]
			cur_headers = self.config_manager.load_config()["input_types_header"][self.cur_input_type]
			self.text_memory = []
			for i in range(len(self.label_memory)):
				if cur_headers[i] != "_":
					self.label_memory[i].setText(cur_headers[i])
				else:
					self.label_memory[i].setText("")
			self.label_pointer = [0, len(cur_headers)]
			top_label.setStyleSheet("""
									  QLabel {
										border: 2px solid yellow;}""")
			cur_label.setStyleSheet("""
									QLabel {
						   				border: 2px solid #ccc;}""")

	def on_value_changed(self, value):
		if self.cur_input_type != value:
			self.cur_input_type = value
			self.clear_memory(same_type=False)
		else:
			if self.label_memory:
				self.clear_memory(same_type=True)
		self.clear_frame()
		headers = self.config_manager.load_config()["input_types_header"][value]
		for i in range(len(headers)):
			self.text_memory.append([])
			if headers[i] == "_":
				label = QLabel()
			elif headers[i].startswith("+"):
				label = QLabel(headers[i][1:])
			else:
				label = QLabel(headers[i])
			self.text_memory[i].append(headers[i])
			label.setAlignment(Qt.AlignCenter)
			label.setStyleSheet("""
								QLabel {
					   				border: 2px solid #ccc;}""")
			self.frame_layout.addWidget(label)
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
	
	def clear_frame(self):
		if self.label_memory:
			for i in range(len(self.label_memory)):
				label = self.label_memory[i]
				self.frame_layout.removeWidget(label)
				label.deleteLater()
			self.label_memory = []
	
	def show_warning(self, error_type):
		if error_type == "calc_error":
			error_text = "Die nutzer Eingabe muss folgende Form haben:\n\"MusterText\"#\"123,45\""
		elif error_type == "wrong_pattern":
			error_text = "Nutzereingabe darf nicht mit folgenden Zeichen beginnen: (_, +)"
		msg = QMessageBox()
		msg.setWindowFlags(msg.windowFlags() | Qt.WindowStaysOnTopHint)
		msg.setIcon(QMessageBox.Warning)
		msg.setWindowTitle("Eingabe Fehler!")
		msg.setText(error_text)
		msg.setStandardButtons(QMessageBox.Ok)
		msg.exec()


if __name__ == "__main__":
	pass