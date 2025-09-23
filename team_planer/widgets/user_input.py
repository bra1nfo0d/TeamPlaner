import re
from PySide6.QtWidgets import QLabel, QVBoxLayout
from PySide6.QtCore import Qt
from widgets.clickable_frame import ClickableFrame
from core.config_manager import ConfigManager
from windows.edit_window import EditWindow


class UserInput:
	"""
	Displays the user input on the main window.

	A UserInput object creates a styled frame that shows either text entries
	or calculated numeric entries, based on the configuration. The frame is
	clickable and opens an `EditWindow` for modifying or deleting the entry.

	Attributs:
		config_manager (ConfigManager): Provides access to configuration values.
		date (str): The date associated with this user input.
		text_memory (list[list[str]]): Nested list storing input data and metadata.
		setting (list[str]): Settings for the input type (e.g., colors, validation).
		layout (object): The target PySide layout where this input frame is placed.
		spacer (object): The spacer item used in the target layout.
		label_memory (list[QLabel]): Keeps track of QLabel widgets displaying input.
		calc (float): Running total for numeric ("calc") inputs.
		goal (int | str): Target number for calculations, or "_" if unused.
		frame (ClickableFrame): The clickable frame containing the input display.
		frame_layout (QVBoxLayout): Layout managing labels inside the frame.
		padding_layout (QVBoxLayout): Layout for spacing the frame inside the parent.
	"""

	def __init__(self,
			  date: str,
			  text_memory: list[list[str]],
			  settings: list[str],
			  layout: object,
			  spacer: object,):
		"""
		Initialize a UserInput object.

		Args:
			date (str): The date associated with this input.
			text_memory (list[list[str]]): Stored user input data.
			settings (list[str]): Input configuration (colors, type info).
			layout (object): The layout in which this frame should appear.
			spacer (object): Spacer item from the parent layout.
		"""
		self.config_manager = ConfigManager()

		self.date = date
		self.text_memory = text_memory
		self.setting = settings
		self.layout = layout
		self.spacer = spacer
		self.label_memory = []
		self.calc = 0
		self.goal = "_"
		
		self._setup_frame()
		self._setup_input_content()
		self._setup_style()
	
	def _setup_frame(self) -> None:
		"""
		Create the clickable frame and attach a layout to hold labels.

		Connects the frame's `clicked` signal to open the edit window.
		"""
		self.frame = ClickableFrame()
		self.frame_layout = QVBoxLayout(self.frame)
		self.frame.clicked.connect(lambda: self._click())

	def _setup_input_content(self) -> None:
		"""
		Populate the frame with labels representing stored user input.

		- For text entries: display each line of text.
		- For calc entries: display the text, accumulate totals, and store goals.
		"""
		for i in range(len(self.text_memory)):
			label = QLabel()
			self.label_memory.append(label)
			self.frame_layout.addWidget(label)

			for j in range(1, len(self.text_memory[i])):
				if self.text_memory[i][j].startswith("*"):
					add_text = self.text_memory[i][j][1:]
				else:
					add_text = self.text_memory[i][j]

				cur_text = label.text()

				if re.match(r"text$", self.text_memory[i][0]):
					if j == 1:
						label.setText(add_text)
					else:
						label.setText(cur_text + "\n" + add_text)

				elif re.match(r"calc#", self.text_memory[i][0]):
					self.goal = int(self.text_memory[i][0].split("#")[1])
					if j == 1:
						label.setText(add_text)
					else:
						text_num = self.text_memory[i][j].split("#")
						add_text = text_num[0]
						str_num = text_num[1]
						if "," in str_num:
							str_num = str_num.replace(",", ".")
						num = float(str_num)
						label.setText(cur_text + "\n" + add_text)
						self.calc += num

				label.setAlignment(Qt.AlignCenter)
		
	def _setup_style(self) -> None:
		"""
		Apply styles to the frame and labels.

		- If numeric input: color depends on whether the goal was reached.
		- If text input: colors are taken directly from settings.
		"""
		if isinstance(self.goal, int):
			config = self.config_manager.load_config()
			if self.calc >= self.goal:
				outer_color = config["calc_true_color"]
			elif self.calc < self.goal:
				outer_color = config["calc_false_color"]
		elif isinstance(self.goal, str):
			outer_color = self.setting[3]

		self.frame.setStyleSheet(f"""
						   border: 2px solid;
						   border-color: {outer_color};
		""")

		inner_color = self.setting[2]
		for label in self.label_memory:
			label.setStyleSheet(f"""
					   border: 2px solid;
					   border-color: {inner_color};
		""")

	def _show_input(self) -> None:
		"""
		Insert this UserInput frame into the target layout.

		Removes the existing spacer, adds the frame inside a padding layout,
		and then re-inserts the spacer below it.
		"""
		self.padding_layout = QVBoxLayout()
		self.padding_layout.setContentsMargins(0, 0, 0, 5)
		spacer = self.spacer
		self.layout.removeItem(self.spacer)
		self.padding_layout.addWidget(self.frame)
		self.layout.addLayout(self.padding_layout)
		self.layout.addItem(spacer)

	def _click(self) -> None:
		"""
		Handle clicks on the frame.

		Opens an `EditWindow` that allows the user to modify or delete
		the current UserInput entry.
		"""
		self.edit_window = EditWindow(
			date=self.date,
			text_memory=self.text_memory,
			settings=self.setting,
			user_input=self,
			layout=self.layout,
			spacer=self.spacer,
			padding=self.padding_layout
		)		
		self.edit_window.show()


if __name__ == "__main__":
	pass