from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QWidget
from PySide6.QtGui import QKeySequence, QShortcut, Qt
from team_planer.ui_elements.day_view import DayView
from team_planer.core.date_manager import DateManager
from team_planer.core.storage_manager import StorageManager
from team_planer.core.config_manager import ConfigManager


class MainWindow(QMainWindow):
	"""Main calendar window showing multiple weeks and days."""

	def __init__(self, weeks_shown: int, is_main_window: bool = True, start_week: int = 0):
		"""
		Args:
			weeks (int): Number of weeks displayed at once.
			is_main_window (bool): Whether this is the primary window.
			start_week (int): Starting week offset (0 = current).
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
		"""Set window title from config."""
		config = self.config_manager.load_config()
		self.setWindowTitle(config["window_title"])

	def _setup_layouts(self) -> None:
		"""Initialize central widget and main horizontal layout."""
		if isinstance(self, QMainWindow):
			central_widget = QWidget()
			self.widget_layout = QHBoxLayout(central_widget)
			self.setCentralWidget(central_widget)
		else:
			layout = QHBoxLayout(self)
			self.widget_layout = layout

	def _setup_shortcuts(self) -> None:
		"""Add keyboard shortcuts for week navigation and fullscreen mode."""
		shortcut_left = QShortcut(QKeySequence("Left"), self)
		shortcut_left.activated.connect(lambda: self._week_view_change(-1))

		shortcut_right = QShortcut(QKeySequence("Right"), self)
		shortcut_right.activated.connect(lambda: self._week_view_change(1))

		shortcut_f11 = QShortcut(QKeySequence(Qt.Key_F11), self)
		shortcut_f11.activated.connect(self._toogle_fullscreen)

		shortcut_escape = QShortcut(QKeySequence(Qt.Key_Escape), self)
		shortcut_escape.activated.connect(self._exit_fullscreen)

	def _setup_additional_window(self):
		"""Open additional week display windows from config."""
		config = self.config_manager.load_config()
		windows = config["window_shown"]

		for d in range(windows):
			if d > 0 and self.is_main_window:
				from team_planer.windows.additional_window import AdditionalWindow
				self.additional_window = AdditionalWindow(self, self.cur_week)
				self.additional_window.showMaximized()
				self.window_memory.append(self.additional_window)
	
	def _setup_weekdays(self) -> None:
		"""Build and display all DayView widgets for current weeks."""
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
		Change visible week and sync all open windows.

		Args:
			val (int): Week offset. Negative = past, positive = future.
		"""
		if hasattr(self, "window_memory"):
			for window in self.window_memory:
				if window is not self:
					window._refresh_week_view(val)
		self._refresh_week_view(val)

	def _refresh_week_view(self, val: int):
		"""
		Refresh currently shown week(s) and reload user data.

		Args:
			val (int): Week offset to apply.
		"""
		self.cur_week += val

		for widget in self.cur_week_widgets:
			widget.setParent(None)
			widget.deleteLater()

		self.cur_week_widgets.clear()
		self.date_frame_connection.clear()
		
		self._setup_weekdays()
		self.storage_manager.load_user_data(self.date_frame_connection)

	def _toogle_fullscreen(self):
		"""Toogles between fullscreen mode."""
		if self.isFullScreen():
			self.showMaximized()
		else:
			self.showFullScreen()

	def _exit_fullscreen(self):
		"""Escapes fullscreen mode."""
		if self.isFullScreen():
			self.showMaximized()

	def get_date_frame_connection(self) -> dict:
		"""Return the current date-to-frame connection map."""
		return self.date_frame_connection


if __name__ == "__main__":
	"""Opens the MainWindow without running the hole application"""
	import sys
	from PySide6.QtWidgets import QApplication

	test_app = QApplication(sys.argv)

	test_weeks_shown = 2
	test_is_main_window = True
	test_start_week = 0

	test_main_window = MainWindow(test_weeks_shown, test_is_main_window, test_start_week)
	test_main_window.show()

	sys.exit(test_app.exec())