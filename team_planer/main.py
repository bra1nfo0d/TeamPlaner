import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt
from windows.main_window import MainWindow
from core.storage_manager import StorageManager
from core.config_manager import ConfigManager

class App:
	"""
	Main application controller.
	"""

	def __init__(self):
		self.storage_manager = StorageManager()
		self.config_manager = ConfigManager()

		self.app = QApplication(sys.argv)

	def _setup_dark_mode(self) -> None:
		"""
		Apply a dark theme palette to the application.
		"""
		palette = QPalette()
		palette.setColor(QPalette.Window, QColor(53, 53, 53))
		palette.setColor(QPalette.Window, QColor(53, 53, 53))
		palette.setColor(QPalette.WindowText, Qt.white)
		palette.setColor(QPalette.Base, QColor(35, 35, 35))
		palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
		palette.setColor(QPalette.ToolTipBase, Qt.white)
		palette.setColor(QPalette.ToolTipText, Qt.white)
		palette.setColor(QPalette.Text, Qt.white)
		palette.setColor(QPalette.Button, QColor(53, 53, 53))
		palette.setColor(QPalette.ButtonText, Qt.white)
		palette.setColor(QPalette.BrightText, Qt.red)
		palette.setColor(QPalette.Link, QColor(42, 130, 218))
		palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
		palette.setColor(QPalette.HighlightedText, Qt.black)
		self.app.setPalette(palette)

	def run(self) -> None:
		"""
		Starts the application event loop.
		"""
		self._setup_dark_mode()
		config = self.config_manager.load_config()
		self.main_window = MainWindow(config["weeks_shown"])
		self.storage_manager.create_db()
		self.storage_manager.load_user_data(
			self.main_window.get_date_frame_connection()
		)
		self.main_window.showMaximized()
		sys.exit(self.app.exec())


if __name__ == "__main__":
	App().run()