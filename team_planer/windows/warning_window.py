from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Qt
from team_planer.core.config_manager import ConfigManager


class PopupWindow(QMessageBox):
	"""Popup window showing error message from config."""

	def __init__(self, popup_type: str, text_code: str, parent: object | None = None):
		"""
		Args:
			error_code (str): Error code used to look up massage text.
			parent (object): Parent widget.
		"""
		super().__init__(parent)
		self.config_manager = ConfigManager()
		self.popup_type = popup_type
		self.text_code = text_code

		self._setup_window()

	def _setup_window(self) -> None:
		"""Configurate window title, text, and icon from config."""
		config = self.config_manager.load_config()
		header_text_list = config[self.text_code]
		header = header_text_list[0]
		text = header_text_list[1]

		self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
		self.setIcon(QMessageBox.Warning)
		self.setWindowTitle(header)
		self.setText(text)
		if self.popup_type == "error":
			self.setStandardButtons(QMessageBox.Ok)
		elif self.popup_type == "accept":
			self.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
		


if __name__ == "__main__":
	import sys
	from PySide6.QtWidgets import QApplication

	app = QApplication(sys.argv)

	text = {999: ["Test Header", "Test Text"]}

	popup = PopupWindow("error", 999, None)
	popup.exec()

	sys.exit(app.exec())