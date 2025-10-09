import re
from PySide6.QtWidgets import(
	QWidget, QHBoxLayout, QLabel, QVBoxLayout, QPushButton,
	QFrame, QSpacerItem, QSizePolicy, QComboBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QShortcut
from team_planer.windows.warning_window import PopupWindow
from team_planer.ui_elements.custom_input_bind import CustomLineEdit
from team_planer.ui_elements.user_input import UserInput
from team_planer.core.storage_manager import StorageManager
from team_planer.core.config_manager import ConfigManager

class InputWindow(QWidget):
	"""Popup for entering and managing user input from specific day."""

	def __init__(self,
			  day: str,
			  date: str,
			  target_layout: object,
			  target_spacer: object):
		"""
		Args:
			day (str): Weekday name.
			date (str): Formatted date string.
			target_layout (object): Parent DayView layout.
			target_spacer (object): Parent layout spacer.
		"""
		super().__init__()
		self.config_manager = ConfigManager()
		self.storage_manager = StorageManager(self)

		self.day = day
		self.date = date
		self.target_layout = target_layout
		self.target_spacer = target_spacer
		self.text_memory = []
		self.label_memory = []
		self.label_pointer = [0, 0] #TODO: change to tuple
		self.calc = 0.0

		self._setup_window()
		self._setup_layouts()
		self._setup_frame()
		self._setup_drop_bar()
		self._setup_text_input()
		self._setup_submit_button()
		self._setup_spacer()
		self._setup_shortcuts()
		self._setup_input_view([""])

	def _setup_window(self) -> None:
		"""Configure size, title, and always-on-top behavior."""
		self.resize(400, 400)
		self.setFixedSize(400, 400)
		self.setWindowFlags(Qt.WindowStaysOnTopHint)
		self.setWindowTitle(f"{self.day} - {self.date}")

	def _setup_spacer(self) -> None:
		"""Add expanding spacer for layout balance."""
		self.spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
		self.row1.addItem(self.spacer)
		self.row2.addItem(self.spacer)

	def _setup_frame(self) -> None:
		"""Main frame where dynamic labels are placed."""
		self.frame = QFrame()
		self.frame.setLayout(self.frame_layout)
		self.frame.setFrameShape(QFrame.Box)
		self.frame.setLineWidth(2)
		self.frame.setStyleSheet("""
						   padding: 4px;
						   border: 2px solid;
						   border-radius: 10px;
						   border-color: #ccc;
		""")
		self.row1.addWidget(self.frame)

	def _setup_submit_button(self) -> None:
		"""Add submit button."""
		self.submit_button = QPushButton("Submit")
		self.submit_button.clicked.connect(self._on_click)
		self.row2.addWidget(self.submit_button)

	def _setup_text_input(self) -> None:
		"""Add main text input with Enter/Delete signals."""
		self.text_input = CustomLineEdit()
		self.text_input.setStyleSheet("""
								background-color: #121212;
		""")
		self.text_input.returnPressed.connect(self._on_return)
		self.text_input.deletePressed.connect(self._on_delete)
		self.row2.addWidget(self.text_input)

	def _setup_drop_bar(self) -> None:
		"""Add dropdown for selecting input types."""
		self.drop_bar = QComboBox()
		self.drop_bar.addItems(self.config_manager.load_config()["input_types"])
		self.drop_bar.setStyleSheet("""
							  background-color: #121212;
							  """)
		self.drop_bar.currentTextChanged.connect(self._setup_input_view)
		self.row2.addWidget(self.drop_bar)

	def _setup_layouts(self) -> None:
		"""Main layout: two vertical columns in a horizontal layout."""
		self.frame_layout = QVBoxLayout()
		self.row1 = QVBoxLayout()
		self.row2 = QVBoxLayout()

		main_layout = QHBoxLayout(self)
		main_layout.addLayout(self.row1)
		main_layout.addLayout(self.row2)

	def _setup_shortcuts(self) -> None:
		"""Keyboard navigation shortcuts."""
		down_shortcut = QShortcut(Qt.Key_Down, self.text_input)
		down_shortcut.activated.connect(lambda: self._on_arrow_press(1))

		up_shortcut = QShortcut(Qt.Key_Up, self.text_input)
		up_shortcut.activated.connect(lambda: self._on_arrow_press(-1))

	def _setup_input_view(self, input_type: list[str]) -> None:
		"""
		Build label view for selected input type.

		Args:
			input_type (list[str]): Selected input type, defaults to first config type.
		"""
		if input_type == [""]:
			config = self.config_manager.load_config()
			input_type = config["first_input_type"]

		self.cur_input_struct = self.config_manager.load_config()["input_types"][input_type]
		self._clear_content()
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
				color = "yellow"
			else:
				color = "#ccc"
			label.setStyleSheet(f"""
					   border: 2px solid;
					   border-radius: 10px;
					   border-color: {color};
					   """)				
			self.frame_layout.addWidget(label)
			self.label_memory.append(label)

	# TODO: Fix the total show with a calc input
	def _on_return(self) -> None:
		"""Add or calculate entry for the current label."""
		entry_type = self.text_memory[self.label_pointer[0]][0]
		entry_text = self.text_input.text()
		label = self.label_memory[self.label_pointer[0]]
		cur_text = label.text()
		if entry_text.startswith("*"):
			self._show_warning(error_code="E002")
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
					label.setText(cur_text + "\n" + text + " -> " + disp_num)
				else:
					label.setText(text + " -> " + num)
				self.text_memory[self.label_pointer[0]].append(text + "#" + calc_str)
			else:
				self._show_warning(error_code="E001")
				return
		self.text_input.clear()

	def _on_delete(self) -> None:
		"""Delete last entry from the current label."""
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

	def _on_click(self) -> None:
		"""Validate input and save as UserInput."""
		for l in self.text_memory:
			if len(l) <= 1:
				self._show_warning(error_code="E003")
				return
		settings = self.cur_input_struct[0]
		user_input = UserInput(
						 self.date,
						 self.text_memory,
						 settings,
						 self.target_layout,
						 self.target_spacer
						 )
		user_input._show_input()
		self.storage_manager.store_user_input(
										settings=settings,
										text_memory=self.text_memory,
										date=self.date
										)
		self._setup_input_view(self.cur_input_struct[0][0])
		
	def _clear_memory(self, same_type: bool) -> None:
		"""
		Reset labels and text state.

		Args:
			same_type (bool): 	If True, keep current labels/headers and clear values.
								If False, remove labels and reset everything.
		"""
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
						   border: 2px solid;
						   border-color: yellow;
						   }""")
			cur_label.setStyleSheet("""
						   QLabel {
						   border: 2px solid;
						   border-color: #ccc;
						   }""")
	
	def _on_arrow_press(self, val: int) -> None:
		"""Move focus between labels."""
		lenght = self.label_pointer[1]
		pointer = self.label_pointer[0]
		calc = (pointer+val)%lenght
		past_label = self.label_memory[self.label_pointer[0]]
		past_label.setStyleSheet("""
						   QLabel {
						   border: 2px solid;
						   border-color: #ccc;
						   }""")
		lenght = self.label_pointer[1]
		pointer = self.label_pointer[0]
		self.label_pointer = [calc, lenght]
		cur_label = self.label_memory[self.label_pointer[0]]
		cur_label.setStyleSheet("""
						  QLabel {
						  border: 2px solid;
						  border-color: yellow;
						  }""")
	
	def _clear_content(self) -> None:
		"""Remove all labels and reset memory."""
		for label in self.label_memory:
			self.frame_layout.removeWidget(label)
			label.deleteLater()
		self.label_memory = []
		self.text_memory = []
	
	def _show_warning(self, error_code: str) -> None:
		"""
		Show an error popup.

		Args:
			error_code (str): Error code identifier.
		"""
		error_window = PopupWindow("error", error_code, self)
		error_window.exec()


if __name__ == "__main__":
	"""Opens the InputWindow without running the hole application"""
	import sys
	from PySide6.QtWidgets import QApplication

	test_app = QApplication(sys.argv)

	test_day = "Monday"
	test_date = "01.01.2000"
	test_layout, test_spacer = None, None

	test_input_window = InputWindow(test_day, test_date, test_layout, test_spacer)
	test_input_window.show()

	sys.exit(test_app.exec())