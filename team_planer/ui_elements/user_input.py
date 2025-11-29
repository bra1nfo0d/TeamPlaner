import re
from PySide6.QtWidgets import QLabel, QVBoxLayout
from PySide6.QtCore import Qt
from team_planer.ui_elements.clickable_widgets import ClickableFrame
from team_planer.core.config_manager import ConfigManager
from team_planer.windows.edit_window import EditWindow


class UserInput:
	"""Creates a clickable frame showing stored user input or calcultions."""

	def __init__(
			self,
			date: str,
			text_memory: list[list[str]],
			settings: list[str],
			layout: object,
			spacer: object
	):
		"""
		Args:
			date (str): Associated date.
			text_memory (list[list[str]]): Stored input data.
			settings (list[str]): Input configuration (color, type info).
			layout (object): Target layout where the frame is added.
			spacer (object): Spacer item from parent layout.
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
		
		self._load_config()
		self._setup_frame()
		self._setup_input_content()
		self._setup_style()
	
	def _load_config(self) -> None:
		config = self.config_manager.load_config()

		self.font_size = config["user-input_font-size"]
		self.font_family = config["user-input_font-family"]
		self.font_weight = config["user-input_font-weight"]

		self.inner_border_width = config["user-input_inner-border-width"]
		self.inner_border_radius = config["user-input_inner-border-radius"]
		self.inner_border_color = config["user-input_inner-border-color"]

		self.outer_border_width = config["user-input_outer-border-width"]
		self.outer_border_radius = config["user-input_outer-border-radius"]
		self.outer_border_color = config["user-input_outer-border-color"]

		self.calc_true_color = config["user-input_calc-true-color"]
		self.calc_false_color = config["user-input_calc-false-color"]
		

	def _setup_frame(self) -> None:
		"""Create clickable frame and connect click signal."""
		self.frame = ClickableFrame()
		self.frame_layout = QVBoxLayout(self.frame)
		self.frame.clicked.connect(lambda: self._click())
		self.frame.setStyleSheet(f"""
			border: {self.outer_border_width}px solid;
			border-radius: {self.outer_border_radius}px;
			border-color: {self.outer_border_color};
		""")

	def _setup_input_content(self) -> None:
		"""Add labels for text or numeric input data."""
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

				label.setStyleSheet(f"""
					font-size: {self.font_size}px;
					border: {self.inner_border_width}px solid;
					border-radius: {self.inner_border_radius}px;
					border-color: {self.inner_border_color};
				""")
				label.setAlignment(Qt.AlignCenter)
		
	def _setup_style(self) -> None:
		"""Apply color styling based on settings and calc results."""
		if isinstance(self.goal, int):
			if self.calc >= self.goal:
				outer_color = self.calc_true_color
			elif self.calc < self.goal:
				outer_color = self.calc_false_color
		elif isinstance(self.goal, str):
			outer_color = self.setting[3]

		self.frame.setStyleSheet(f"""
			border: {self.outer_border_width}px solid;
			border-color: {outer_color};
			border-radius: {self.outer_border_radius}px;
		""")

		inner_color = self.setting[2]
		for label in self.label_memory:
			label.setStyleSheet(f"""
				font-size: {self.font_size}px;
				font-family: {self.font_family};
				font-weight: {self.font_weight};
				border: {self.inner_border_width}px solid;
				border-color: {inner_color};
				border-radius: {self.inner_border_radius}px;
			""")

	def _show_input(self) -> None:
		"""Insert the frame into the layout, keeping spacer order."""
		self.padding_layout = QVBoxLayout()
		self.padding_layout.setContentsMargins(0, 0, 0, 5)
		spacer = self.spacer
		self.layout.removeItem(self.spacer)
		self.padding_layout.addWidget(self.frame)
		self.layout.addLayout(self.padding_layout)
		self.layout.addItem(spacer)

	def _click(self) -> None:
		"""Open edit window for this entry."""
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