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

		print(text_memory)

		self.config_manager = ConfigManager()

		self.date = date
		self.text_memory = text_memory
		self.setting = settings
		self.layout = layout
		self.spacer = spacer
		self.label_memory = []
		self.income_sum = 0
		self.worker_sum = 0
		self.income_goal_per_worker = 0
		# type(goal) == str: means there is no calc_input to handle
		# type(goal) == int: means it handles a calc logic 
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

		self.income_goal_per_worker = config["input_goal_per_worker"]
		

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
		for idx_block in range(len(self.text_memory)):
			label = QLabel()
			self.label_memory.append(label)
			self.frame_layout.addWidget(label)

			for idx_text in range(1, len(self.text_memory[idx_block])):
				if self.text_memory[idx_block][idx_text].startswith("*"):
					add_text = self.text_memory[idx_block][idx_text][1:]
				else:
					add_text = self.text_memory[idx_block][idx_text]

				cur_text = label.text()

				if re.match(r"text$", self.text_memory[idx_block][0]):
					if idx_text == 1:
						label.setText(add_text)
					else:
						label.setText(cur_text + "\n" + add_text)

				if re.match(r"worker$", self.text_memory[idx_block][0]):
					# counts amount of workers by removing the input_type and header
					self.worker_sum = len(self.text_memory[idx_block]) - 2
					if idx_text == 1:
						label.setText(add_text)
					else:
						label.setText(cur_text + "\n" + add_text)

				elif re.match(r"calc#", self.text_memory[idx_block][0]):
					if self.worker_sum > 0:
						self.goal = self.income_goal_per_worker * self.worker_sum
#					self.goal = int(self.text_memory[idx_block][0].split("#")[1])
					if idx_text == 1:
						label.setText(add_text)
					else:
						text_num = self.text_memory[idx_block][idx_text].split("#")
						add_text = text_num[0]
						str_num = text_num[1]
						if "," in str_num:
							str_num = str_num.replace(",", ".")
						num = float(str_num)
						label.setText(cur_text + "\n" + add_text)
						self.income_sum += num

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
			if self.income_sum >= self.goal:
				outer_color = self.calc_true_color
			elif self.income_sum < self.goal:
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