from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Qt
from team_planer.core.config_manager import ConfigManager

class ErrorWindow(QMessageBox):
	"""
	A popup window for displaying error messages.

	This class extends `QMessageBox` to create a standardized error dialog
	using error codes that map to headers and texts in the application
	configuration.

	Attributes:
		config_manager (ConfigManager): Loads error message texts from config.
		error_code (str): The code identifying which error message to display.
	"""

	def __init__(self, error_code: str, parent: object | None = None):
		"""
		Initialize the error window.

		Args:
			error_code (str): Key used to look up the error message in config.
			parent (object): The parent widget for this dialog.
		"""
		super().__init__(parent)
		self.config_manager = ConfigManager()
		self.error_code = error_code

	# TODO: Fix the visibility issues with the error header and text
	def _setup_window(self) -> None:
		"""
		Configure the QMessageBox window based on the error code.

		Loads the error header and text from the configuration, applies
		styles, sets the warning icon, and adds a standard OK button.
		"""
		config = self.config_manager.load_config()
		error_header_text = config[self.error_code]
		error_header = error_header_text[0]
		error_text = error_header_text[1]

		self.setWindowFlags(self.windowFlags() | Qt.WindowStayOnTopHint)
		self.setIcon(QMessageBox.Warning)
		self.setWindowTitle(error_header)
		self.setText(error_text)
		self.standardButtons(QMessageBox.Ok)


if __name__ == "__main__":
	pass