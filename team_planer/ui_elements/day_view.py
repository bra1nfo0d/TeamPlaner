from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from team_planer.core.date_manager import DateManager
from team_planer.core.config_manager import ConfigManager
from team_planer.ui_elements.clickable_widgets import ClickableLabel
from team_planer.windows.input_window import InputWindow

class DayView(QWidget):
	"""Represents a single day in the weekly calender view."""

	def __init__(self, day: str, date: str):
		"""
		Args:
			day (str): Weekday name (e.g. "Monday").
			date (str): Formatted date string (e.g., "18.09.2025").
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
		"""Configure main and padding"""
		self.frame_layout = QVBoxLayout(self.frame)
		self.frame_layout.setContentsMargins(8, 8, 8, 8)
		self.frame_layout.setSpacing(4)

		main_layout = QVBoxLayout(self)
		main_layout.addWidget(self.frame)

		self.padding_layout = QVBoxLayout()
		self.padding_layout.setContentsMargins(0, 0, 0, 10)

	def _setup_frame(self) -> None:
		"""Create and style main frame; highlight if today."""
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
		"""Create clickable header with weekday and date."""
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
		"""Open input window for this day."""
		input_window = InputWindow(
			self.day,
			self.date,
			self.frame_layout,
			self.spacer
		)
		input_window.show()
	
	def get_elements(self) -> list:
		"""
		Returns:
			list: [date (str), frame_layout (QVBoxLayout), spacer (QSpacerItem)]
		"""
		return [self.date, self.frame_layout, self.spacer]


if __name__ == "__main__":
	pass