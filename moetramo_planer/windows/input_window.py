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
		self.storage_manager = StorageManager()

		self.text_memory = []
		self.label_memory = []
		self.label_pointer = [0, 0] # change all the list pointer to tupel
		self.calc = 0.0

		self.setWindowFlags(Qt.WindowStaysOnTopHint)
		self.setWindowTitle(f"{day} - {date}")

		self.frame = QFrame()
		self.frame.setFrameShape(QFrame.Box)
		self.frame.setLineWidth(2)
		self.frame.setStyleSheet("""padding: 4px; 
							    	border: 2px solid #ccc;
					  		     	border-radius: 10px;""")

		self.drop_bar = QComboBox()
		self.drop_bar.addItems(self.config_manager.load_config()["input_types"])
		self.drop_bar.setStyleSheet("background-color: #121212")
		self.drop_bar.currentTextChanged.connect(self.on_value_changed)

		self.input_field = CustomLineEdit()
		self.input_field.setStyleSheet("background-color: #121212")
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

		global first_input_type
		first_input_type = self.config_manager.load_config()["first_input_type"]
		self.on_value_changed(first_input_type)

	def on_return(self):
		entry_type = self.text_memory[self.label_pointer[0]][0]
		entry_text = self.input_field.text()
		label = self.label_memory[self.label_pointer[0]]
		cur_text = label.text()

		if entry_text.startswith("*"):
			self.show_warning(error_code=2)
			return

		if re.match(r"text", entry_type):
			if len(self.text_memory[self.label_pointer[0]]) > 1:
				label.setText(cur_text + "\n" + entry_text)
			else:
				label.setText(entry_text)
			self.text_memory[self.label_pointer[0]].append(entry_text)

		elif re.match(r"calc", entry_type):
			pattern = r".*#\d+(?:[,.]\d{1,2})?$"
			if re.match(pattern, entry_text):
				text_num_list = entry_text.split("#")
				text = text_num_list[0]
				num = text_num_list[1]
				if "," in num:
					num = num.replace(",", ".")
				
				pre_calc_len = len(str(self.calc)) + 1
				
				self.calc += float(num)
				self.calc = round(self.calc, 2)

				calc_str = str(num)

				if re.match(r"\d+\.\d{2}$", calc_str):
					pass
				elif re.match(r"\d+\.\d{1}$", calc_str):
					calc_str = calc_str + "0"
				elif re.match(r"\d+", calc_str):
					calc_str = calc_str + ".00"

				if re.match(r"\d+\.\d{2}$", num):
					disp_num = num.replace(".", ",") + "€"
				elif re.match(r"\d+\.\d{1}$", num):
					disp_num = num.replace(".", ",") + "0€"
				elif re.match(r"\d+$", num):
					disp_num = num + ",00€"

				if len(self.text_memory[self.label_pointer[0]]) > 1:
					label.setText(cur_text + "\n" + text + " -> " + disp_num + "\n" + str(self.calc) + "€")
				else:
					label.setText(text + " -> " + num + "\n" + str(self.calc) + "€")
				self.text_memory[self.label_pointer[0]].append(text + "#" + calc_str)

			else:
				self.show_warning(error_code="E001")
				return

		self.input_field.clear()

		print(self.calc)
		print(self.text_memory)


	def on_delete(self):
		if len(self.text_memory[self.label_pointer[0]]) > 1 and not self.text_memory[self.label_pointer[0]][-1].startswith("*"):
			label = self.label_memory[self.label_pointer[0]]
			cur_text = label.text()
			del_text = self.text_memory[self.label_pointer[0]].pop()
			del_text_len = len(del_text)
			
			if re.match(r"calc", self.text_memory[self.label_pointer[0]][0]):				
				del_text_len += 4
				self.calc -= float(del_text.split("#")[1])
				self.calc = round(self.calc, 2)

			if len(self.text_memory[self.label_pointer[0]]) > 1:
				label.setText(cur_text[:len(cur_text)-del_text_len-1])
			else:
				label.setText(cur_text[:len(cur_text)-del_text_len])
		
		print(self.calc)
		print(self.text_memory)


	def on_click(self):
		for l in self.text_memory:
			if len(l) <= 1:
				self.show_warning(error_code=3)
				return
		settings = self.cur_input_struct[0]
		user_input = UserInput(text_memory=self.text_memory, layout=self.target_layout, spacer=self.target_spacer, date=self.date, settings=settings)
		user_input.show_input()
		self.storage_manager.store_user_input(settings=settings, text_memory=self.text_memory, date=self.date)
		self.on_value_changed(self.cur_input_struct[0][0])

		
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

	def on_value_changed(self, input_struct):
		self.cur_input_struct = self.config_manager.load_config()["input_types"][input_struct]
		self.clear_content()
		label_count = len(self.cur_input_struct) - 1
		self.label_pointer = [0, label_count]
		for i in range(label_count):
			self.text_memory.append([self.cur_input_struct[i+1][1]])
			cur_header = self.cur_input_struct[i+1][0]
			if cur_header == "_":
				label = QLabel()
			else:
				label = QLabel(cur_header)
				self.text_memory[i].append(f"*{cur_header}")
			label.setAlignment(Qt.AlignCenter)
			label.setContentsMargins(5, 2, 5, 2)
			if i == 0:
				label.setStyleSheet("""
							border: 2px solid yellow;
							border-radius: 10px;""")
			else:
				label.setStyleSheet("""
							border: 2px solid #ccc;
							border-radius: 10px;""")
				
			self.frame_layout.addWidget(label)
			self.label_memory.append(label)
	
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
	
	def clear_content(self):
		for label in self.label_memory:
			self.frame_layout.removeWidget(label)
			label.deleteLater()
		self.label_memory = []
		self.text_memory = []
	
	def show_warning(self, error_code):
		if error_code == "E001":
			error_text = "E001"
		elif error_code == 2:
			error_text = "Die Nutzer Eingabe darf nicht mit einem \"*\" beginnnen"
		elif error_code == 3:
			error_text = "Ein Eingabefeld wurde leer gelassen."
		msg = QMessageBox()
		msg.setWindowFlags(msg.windowFlags() | Qt.WindowStaysOnTopHint)
		msg.setIcon(QMessageBox.Warning)
		msg.setWindowTitle("Eingabe Fehler!")
		msg.setText(error_text)
		msg.setStandardButtons(QMessageBox.Ok)
		msg.exec()


if __name__ == "__main__":
	pass