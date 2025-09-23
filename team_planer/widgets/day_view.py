from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from core.date_manager import DateManager
from core.config_manager import ConfigManager
from widgets.clickable_label import ClickableLabel
from windows.input_window import InputWindow

class DayView(QWidget):
	"""
	A widget representing a single day in the weekly calendar view.

	The DayView contains:
		- A styled frame with optional highlighting if it matches today's date.
		- A header showing the weekday name and formatted date.
		- A spacer and padding layout for adding user input widgets.

	Attributes:
		config_manager (ConfigManager): Loads application configuration values.
		date_manager (DateManager): Provides formatted date utilities.
		day (str): The weekday name for this day (e.g., "Monday").
		date (str): The formatted date string for this day.
		tday (str): The current date string, used to highlight the frame/header.
		frame (QFrame): The main container frame for this day's content.
		frame_layout (QVBoxLayout): Layout applied inside the frame.
		padding_layout (QVBoxLayout): Extra layout used for spacing.
		spacer (QSpacerItem): Expanding spacer at the bottom of the frame.
	"""

	def __init__(self, day: str, date: str):
		"""
		Initialize a DayView widget.

		Args:
			day (str): The weekday name (e.g., "Monday").
			date (str): The formatted date string (e.g., "18.09.2025").
		"""
		super().__init__()
		self.config_manager = ConfigManager()
		self.date_manager = DateManager()

		self.day = day
		self.date = date
		self.tday = self.date_manager.get_date_str()

		self._setup_frame()
		self._setup_layout()
		self._setup_header()

	def _setup_layout(self) -> None:
		"""
		Configure the layout structure for the day frame.

		Creates the main vertical layout for the frame, applies margins
		and spacing, and sets up the padding layout for additional content.
		"""
		self.frame_layout = QVBoxLayout(self.frame)
		self.frame_layout.setContentsMargins(8, 8, 8, 8)
		self.frame_layout.setSpacing(4)

		main_layout = QVBoxLayout(self)
		main_layout.addWidget(self.frame)

		self.padding_layout = QVBoxLayout()
		self.padding_layout.setContentsMargins(0, 0, 0, 10)

	def _setup_frame(self) -> None:
		"""
		Create and style the main frame for this day.

		Highlights the frame border color differently if this day
		corresponds to the current date (`tday`).
		"""
		self.frame = QFrame(self)
		self.frame.setFrameShape(QFrame.Box)
		self.frame.setLineWidth(2)

		if self.tday == self.date:
			config = self.config_manager.load_config()
			color = config["tday_border_color"]
		else:
			color = "#ccc"

		self.frame.setStyleSheet(f"""
						   border: 1px solid;
						   border-radius: 10px;
						   border-color: {color};
		""")

	def _setup_header(self) -> None:
		"""
		Create and configure the clickable day header label.

		The header displays the weekday and date, styled differently
		if this day matches the current date. Clicking the header
		opens an `InputWindow` for adding user input.
		"""
		label = ClickableLabel(f"{self.day}\n{self.date}")
		label.setAlignment(Qt.AlignCenter)
		label.setFont(QFont("Arial", 10, QFont.Bold))

		if self.tday == self.date:
			config = self.config_manager.load_config()
			color = config["header_color"]
		else:
			color = "#ccc"

		label.setStyleSheet(f"""
					  padding: 4px;
					  border: 2px solid;
					  border-radius: 10px;
					  border-color: {color};
		""")
		
		label.clicked.connect(self._label_clicked)

		self.spacer = QSpacerItem(
			20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
		)

		self.frame_layout.addWidget(label)
		self.frame_layout.addItem(self.spacer)
		self.frame_layout.addLayout(self.padding_layout)
	
	def _label_clicked(self) -> None:
		"""
		Handle clicks on the header label.

		Opens an `InputWindow` for the current day, allowing the user
		to add or manage input content inside the frame layout.
		"""
		input_window = InputWindow(
			self.day,
			self.date,
			self.frame_layout,
			self.spacer
		)
		input_window.show()
	
	def get_elements(self) -> list:
		"""
		Return the key UI elements for this day view.

		Returns:
			list: A list containing:
				- str: The date string of this day.
				- QVBoxLayout: The frame's layout.
				- QSpacerItem: The frame's bottom spacer.
		"""
		return [self.date, self.frame_layout, self.spacer]


if __name__ == "__main__":
	pass