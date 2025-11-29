from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from team_planer.core.date_manager import DateManager
from team_planer.core.config_manager import ConfigManager
from team_planer.ui_elements.clickable_widgets import ClickableLabel
from team_planer.windows.input_window import InputWindow
from team_planer.windows.warning_window import PopupWindow

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

		self._load_config()
		self._setup_frame()
		self._setup_layout()
		self._setup_header()

	def _load_config(self) -> None:
		config = self.config_manager.load_config()

		self.font_size = config["display-window_font-size"]
		self.font_family = config["display-window_font-family"]
		self.font_weight = config["display-window_font-weight"]

		self.content_frame_border_width = config["display-window_content-frame_border-width"]
		self.content_frame_border_radius = config["display-window_content-frame_border-radius"]
		self.content_frame_border_color = config["display-window_content-frame_border-color"]
		self.tday_content_frame_border_color = config["display-window_tday-content-frame_border-color"]

		self.header_frame_border_width = config["display-window_header-frame_border-width"]
		self.header_frame_border_radius = config["display-window_header-frame_border-radius"]
		self.header_frame_border_color = config["display-window_header-frame_border-color"]
		self.tday_header_frame_border_color = config["display-window_tday-header-frame_border-color"]
		self.header_frame_padding = config["display-window_header-frame_padding"]

		self.header_to_content_margin = config["display-window_header-content_margin"]
		self.frame_to_content_margin = config["display-window_frame-content_margin"]
		self.content_to_content_margin = config["display-window_content-content_margin"]

	def _setup_layout(self) -> None:
		"""Configure main and padding"""
		left = self.frame_to_content_margin[0]
		top = self.frame_to_content_margin[1]
		right = self.frame_to_content_margin[2]
		bottom = self.frame_to_content_margin[3]

		self.frame_layout = QVBoxLayout(self.frame)
		self.frame_layout.setContentsMargins(left, top, right, bottom)
		self.frame_layout.setSpacing(self.content_to_content_margin)

		main_layout = QVBoxLayout(self)
		main_layout.addWidget(self.frame)

		self.padding_layout = QVBoxLayout()
		self.padding_layout.setContentsMargins(0, 0, 0, self.header_to_content_margin)

	def _setup_frame(self) -> None:
		"""Create and style main frame; highlight if today."""
		self.frame = QFrame(self)
		self.frame.setFrameShape(QFrame.Box)
#		self.frame.setLineWidth(2)

		if self.tday == self.date:
			color = self.tday_content_frame_border_color
		else:
			color = self.content_frame_border_color

		self.frame.setStyleSheet(f"""
						   border: {self.content_frame_border_width}px solid;
						   border-radius: {self.content_frame_border_radius}px;
						   border-color: {color};
		""")

	def _setup_header(self) -> None:
		"""Create clickable header with weekday and date."""
		family = self.font_family
		size = self.font_size
		weight = QFont.Normal
		if self.font_weight == "Bold":
			weight = QFont.Bold
		elif self.font_weight == "Regular" or self.font_weight == "Normal":
			pass
		else:
			self._show_warning(error_code="E005")
		
		label = ClickableLabel(f"{self.day}\n{self.date}")
		label.setAlignment(Qt.AlignCenter)
		label.setFont(QFont(family, size, weight))

		if self.tday == self.date:
			color = self.tday_header_frame_border_color
		else:
			color = self.header_frame_border_color

		label.setStyleSheet(f"""
					  padding: {self.header_frame_padding}px;
					  border: {self.header_frame_border_width}px solid;
					  border-radius: {self.header_frame_border_radius}px;
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
	
	def _show_warning(self, error_code: str) -> None:
		"""
		Show an error popup.

		Args:
			error_code (str): Error code identifier.
		"""
		error_window = PopupWindow("error", error_code, self)
		error_window.exec()
  

if __name__ == "__main__":
	pass