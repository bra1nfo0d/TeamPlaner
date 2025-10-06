from team_planer.windows.main_window import MainWindow
from team_planer.core.config_manager import ConfigManager

# TODO: make the Additional windows also able to change window view
class AdditonalWindow(MainWindow):
	def __init__(self, main_window, start_week: int):
		config_manager = ConfigManager()
		config = config_manager.load_config()
		weeks_shown = config["weeks_shown"]
		super().__init__(weeks_shown, is_main_window=False, start_week=start_week+2)

		self.main_window = main_window

		self.window_memory = main_window.window_memory
		if self.main_window not in self.window_memory:
			self.window_memory.append(self.main_window)