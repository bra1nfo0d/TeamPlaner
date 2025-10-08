from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Qt
from team_planer.core.config_manager import ConfigManager

class ErrorWindow(QMessageBox):
	"""Popup window showing error message from config."""

	def __init__(self, error_code: str, parent: object | None = None):
		"""
		Args:
			error_code (str): Error code used to look up massage text.
			parent (object): Parent widget.
		"""
		super().__init__(parent)
		self.config_manager = ConfigManager()
		self.error_code = error_code

	# TODO: Fix the visibility issues with the error header and text
	def _setup_window(self) -> None:
		"""Configurate window title, text, and icon from config."""
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