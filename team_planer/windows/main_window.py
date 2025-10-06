from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QWidget
from PySide6.QtGui import QKeySequence, QShortcut
from team_planer.widgets.day_view import DayView
from team_planer.core.date_manager import DateManager
from team_planer.core.storage_manager import StorageManager
from team_planer.core.config_manager import ConfigManager


class MainWindow(QMainWindow):
	"""
	The main application window for displaying multiple weeks in a calendar view.

	This window displays a configurable number of weeks, each with its weekday
	columns. It supports navigation between past and future weeks using keyboard
	shortcuts, and manages the connection between dates and their corresponding
	UI elements.

	Attributs:
		storage_manager (StorageManager): Handles user data persistence.
		config_manager (ConfigManager): Loads application configuration values.
		date_manager (DateManager): Provides date string utilities.
		cur_week (int): The currently displayed week index (0 = current week).
		weeks_shown (int): Number of weeks displayed at once.
		date_frame_connection (dict): Maps date frames to their connected elements.
		cur_week_widgets (list[DayView]): List of DayView widgets currently displayed.
		widget_layout (QHBoxLayout): The layout holding the week views.
	"""

	def __init__(self, weeks_shown: int, is_main_window: bool = True, start_week: int = 0):
		"""
		Initialize the main window.

		Args:
			weeks (int): The number of weeks to display at once.
		"""
		super().__init__()
		self.storage_manager = StorageManager(self)
		self.config_manager = ConfigManager()
		self.date_manager = DateManager()

		self.is_main_window = is_main_window
		self.cur_week = start_week
		self.weeks_shown = weeks_shown
		self.date_frame_connection = {}
		self.cur_week_widgets = []
		self.window_memory = []

		self._setup_window()
		self._setup_layouts()
		self._setup_shortcuts()
		self._setup_weekdays()
		self._setup_additional_window()
	
	def _setup_window(self) -> None:
		"""
		Configure the window title and other high-level settings.
		"""
		config = self.config_manager.load_config()
		self.setWindowTitle(config["window_title"])

	def _setup_layouts(self) -> None:
		"""
		Initialize the central widget and main horizontal layout.
		"""
		if isinstance(self, QMainWindow):
			central_widget = QWidget()
			self.widget_layout = QHBoxLayout(central_widget)
			self.setCentralWidget(central_widget)
		else:
			layout = QHBoxLayout(self)
			self.widget_layout = layout

	def _setup_shortcuts(self) -> None:
		"""
		Register keyboard shortcuts for navigating weeks.

		- Left Arrow → move to previous week
		- Right Arrow → move to next week
		"""
		shortcut_left = QShortcut(QKeySequence("Left"), self)
		shortcut_left.activated.connect(lambda: self._week_view_change(-1))

		shortcut_right = QShortcut(QKeySequence("Right"), self)
		shortcut_right.activated.connect(lambda: self._week_view_change(1))

	def _setup_additional_window(self):
		"""
    	Initialize and show additional week view windows based on the
    	'window_shown' config value, keeping references for synchronization.
    	"""
		config = self.config_manager.load_config()
		windows = config["window_shown"]

		for d in range(windows):
			if d > 0 and self.is_main_window:
				from team_planer.windows.additonal_display_window import AdditonalWindow
				self.additional_window = AdditonalWindow(self, self.cur_week)
				self.additional_window.showMaximized()
				self.window_memory.append(self.additional_window)
	
	def _setup_weekdays(self) -> None:
		"""
		Populate the window with DayView widgets for the current range of weeks.

		Uses the configured weekday list and the current week index to generate
		all displayed day widgets, and stores their frame connections.
		"""
		config = self.config_manager.load_config()
		days = config["weekday_list"]

		for i in range(self.weeks_shown):
			date_list = self.date_manager.get_date_str_list(week = i + self.cur_week)
			for j in range(len(days)):
				date = date_list[j]
				day_widget = DayView(days[j], date)
				self.widget_layout.addWidget(day_widget)

				day_view_elements = day_widget.get_elements() 
				self.date_frame_connection[day_view_elements[0]] = (
					day_view_elements[1],
					day_view_elements[2]
				)
				self.cur_week_widgets.append(day_widget)
	
	def _week_view_change(self, val: int) -> None:
		"""
		Update the displayed week view and synchronize changes across all windows.

		Applies the given week offset to update the currently visible weeks.
		The change is propagated to all linked windows stored in `window_memory`,
		ensuring synchronized navigation between multiple week views.

		Args:
			val (int): The week offset to apply.
						Negative values move to past weeks,
						positive values move to future weeks.
		"""
		if hasattr(self, "window_memory"):
			for window in self.window_memory:
				if window is not self:
					window._refresh_week_view(val)
		self._refresh_week_view(val)

	def _refresh_week_view(self, val: int):
		"""
    	Refresh the currently displayed week view.

    	Updates the current week index by the given offset, clears all existing
    	day widgets and their connections, then rebuilds the week layout and
    	reloads user data to reflect the updated state.
    
    	Args:
        	val (int): The week offset to apply. Negative values move backward,
                   positive values move forward.
    	"""
		self.cur_week += val

		for widget in self.cur_week_widgets:
			widget.setParent(None)
			widget.deleteLater()

		self.cur_week_widgets.clear()
		self.date_frame_connection.clear()
		
		self._setup_weekdays()
		self.storage_manager.load_user_data(self.date_frame_connection)

	def get_date_frame_connection(self) -> dict:
		"""
		Return the current mapping of date frames to their connected elements.

		Return:
			dict: A dictionary mapping date frame keys to their associated elements.
		"""
		return self.date_frame_connection


if __name__ == "__main__":
	pass