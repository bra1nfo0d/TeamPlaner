from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt
import sys
from core.window_controller import WindowController
from core.storage_manager import StorageManager

def set_dark_mode(app):
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

    # Links
	palette.setColor(QPalette.Link, QColor(42, 130, 218))

    # Highlights
	palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
	palette.setColor(QPalette.HighlightedText, Qt.black)
	
	app.setPalette(palette)

def main():
	app = QApplication(sys.argv)
	set_dark_mode(app)
	window_controller = WindowController()
	window_controller.start_week_overview()
	storage_manager = StorageManager()
	storage_manager.create_db()
	storage_manager.laod_user_data(window_controller.get_frame_date_map())
	app.exec()

if __name__ == "__main__":
	main()