from PySide6.QtWidgets import QApplication
import sys
from core.window_controller import WindowController
from core.storage_manager import StorageManager

def main():
	app = QApplication(sys.argv)
	window_controller = WindowController()
	window_controller.start_week_overview()
	storage_manager = StorageManager()
	storage_manager.create_db()
	storage_manager.laod_user_data(window_controller.get_frame_date_map())
	app.exec()

if __name__ == "__main__":
	main()